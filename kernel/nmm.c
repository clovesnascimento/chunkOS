#include "nmm.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>

// Matriz de transição para predição de camadas (Markov)
static uint32_t transition_matrix[CHUNK_MAX_LAYERS][CHUNK_MAX_LAYERS];
static uint32_t last_layer = 0;
static pthread_t prefetch_thread;
static volatile int prefetch_running = 1;

// Protótipos internos
static void* prefetch_worker(void* arg);
static int handle_page_fault(chunk_nmm_context_t* ctx, chunk_layer_t layer, uint32_t page_idx);
static uint64_t get_time_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000 + ts.tv_nsec / 1000;
}

// Aloca e inicializa contexto NMM
chunk_nmm_context_t* nmm_init(void) {
    chunk_nmm_context_t* ctx = calloc(1, sizeof(chunk_nmm_context_t));
    if (!ctx) return NULL;
    
    ctx->weight_pages = malloc(1024 * sizeof(chunk_weight_page_t));
    ctx->kv_pages = malloc(65536 * sizeof(chunk_kv_page_t));
    ctx->ram_limit_bytes = CHUNK_DEFAULT_RAM_LIMIT_MB * 1024 * 1024;
    ctx->ram_used_bytes = 0;
    ctx->page_fault_count = 0;
    ctx->prefetch_hits = 0;
    
    // Inicializa matriz de transição
    memset(transition_matrix, 0, sizeof(transition_matrix));
    
    // Inicia thread de prefetch
    pthread_create(&prefetch_thread, NULL, prefetch_worker, ctx);
    
    return ctx;
}

// Função para calcular importância de uma página
static float calculate_importance(chunk_weight_page_t* page, 
                                  chunk_layer_t current_layer) {
    if (!page->ram_address) return 0.0f;
    
    float recency = 1.0f / (get_time_us() - page->last_access_time + 1);
    float frequency = (float)page->access_count / 1000.0f;
    float distance = abs((int)page->layer_id - (int)current_layer) + 1;
    
    // Importância = (frequência + recência) / distância
    return (frequency + recency) / distance;
}

// Função de evicção baseada em importância
static int evict_page(chunk_nmm_context_t* ctx, chunk_layer_t current_layer) {
    int victim_idx = -1;
    float min_importance = 1e9f;
    
    for (int i = 0; i < 1024; i++) {
        chunk_weight_page_t* page = &ctx->weight_pages[i];
        if (!page->ram_address || page->is_locked) continue;
        
        float importance = calculate_importance(page, current_layer);
        if (importance < min_importance) {
            min_importance = importance;
            victim_idx = i;
        }
    }
    
    if (victim_idx >= 0) {
        chunk_weight_page_t* page = &ctx->weight_pages[victim_idx];
        // Libera a página da RAM
        munmap(page->ram_address, CHUNK_WEIGHT_PAGE_SIZE);
        page->ram_address = NULL;
        ctx->ram_used_bytes -= CHUNK_WEIGHT_PAGE_SIZE;
        return 0;
    }
    return -1;
}

// Page fault handler
static int handle_page_fault(chunk_nmm_context_t* ctx, 
                             chunk_layer_t layer, 
                             uint32_t page_idx) {
    ctx->page_fault_count++;
    
    // Encontra ou cria página
    chunk_weight_page_t* page = NULL;
    for (int i = 0; i < 1024; i++) {
        if (ctx->weight_pages[i].layer_id == layer && 
            ctx->weight_pages[i].page_index == page_idx) {
            page = &ctx->weight_pages[i];
            break;
        }
    }
    
    if (!page) return -1;
    
    // Verifica espaço na RAM
    while (ctx->ram_used_bytes + CHUNK_WEIGHT_PAGE_SIZE > ctx->ram_limit_bytes) {
        if (evict_page(ctx, ctx->current_layer) != 0) {
            fprintf(stderr, "Erro: Não foi possível evictar páginas\n");
            return -1;
        }
    }
    
    // Aloca RAM e carrega do flash
    page->ram_address = mmap(NULL, CHUNK_WEIGHT_PAGE_SIZE,
                             PROT_READ | PROT_WRITE,
                             MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    
    if (page->ram_address == MAP_FAILED) return -1;
    
    // DMA read from flash (simulado)
    int fd = open("/dev/chunk_flash", O_RDONLY);
    if (fd >= 0) {
        pread(fd, page->ram_address, CHUNK_WEIGHT_PAGE_SIZE, page->flash_offset);
        close(fd);
    }
    
    page->is_locked = 1;
    page->last_access_time = get_time_us();
    page->access_count++;
    
    ctx->ram_used_bytes += CHUNK_WEIGHT_PAGE_SIZE;
    
    return 0;
}

// Thread de prefetch
static void* prefetch_worker(void* arg) {
    chunk_nmm_context_t* ctx = (chunk_nmm_context_t*)arg;
    
    while (prefetch_running) {
        // Prediz próximas camadas baseado na matriz de transição
        uint32_t next_layer = ctx->current_layer + 1;
        uint32_t max_count = 0;
        
        for (int i = 0; i < CHUNK_MAX_LAYERS; i++) {
            if (transition_matrix[ctx->current_layer][i] > max_count) {
                max_count = transition_matrix[ctx->current_layer][i];
                next_layer = i;
            }
        }
        
        // Pré-carrega páginas da próxima camada
        for (int offset = 0; offset < CHUNK_PREFETCH_LOOKAHEAD; offset++) {
            uint32_t layer_to_load = next_layer + offset;
            if (layer_to_load >= CHUNK_MAX_LAYERS) break;
            
            // Encontra página da camada
            for (int i = 0; i < 1024; i++) {
                chunk_weight_page_t* page = &ctx->weight_pages[i];
                if (page->layer_id == layer_to_load && !page->ram_address) {
                    // Tenta carregar sem causar page fault
                    if (ctx->ram_used_bytes + CHUNK_WEIGHT_PAGE_SIZE <= 
                        ctx->ram_limit_bytes) {
                        handle_page_fault(ctx, layer_to_load, page->page_index);
                        ctx->prefetch_hits++;
                    }
                    break;
                }
            }
        }
        
        usleep(CHUNK_PREFETCH_POLL_US);
    }
    
    return NULL;
}

int nmm_load_model(chunk_nmm_context_t* ctx, const char* model_path) {
    // Carrega metadados do modelo
    char meta_path[256];
    snprintf(meta_path, sizeof(meta_path), "%s/%s.meta", 
             CHUNK_META_PATH, model_path);
    
    FILE* f = fopen(meta_path, "r");
    if (!f) return -1;
    
    // Lê informações do modelo
    uint32_t layer_count;
    fscanf(f, "layers: %u\n", &layer_count);
    
    for (uint32_t l = 0; l < layer_count; l++) {
        uint32_t pages_in_layer;
        fscanf(f, "layer %u pages: %u\n", &pages_in_layer);
        
        for (uint32_t p = 0; p < pages_in_layer; p++) {
            // Registra página
            chunk_weight_page_t* page = &ctx->weight_pages[l*1024 + p];
            page->layer_id = l;
            page->page_index = p;
            page->flash_offset = l * pages_in_layer * CHUNK_WEIGHT_PAGE_SIZE + 
                                  p * CHUNK_WEIGHT_PAGE_SIZE;
            page->ram_address = NULL;
            page->is_locked = 0;
        }
    }
    
    fclose(f);
    return 0;
}

void nmm_advance_layer(chunk_nmm_context_t* ctx, chunk_layer_t new_layer) {
    // Atualiza matriz de transição
    if (ctx->current_layer != new_layer) {
        transition_matrix[ctx->current_layer][new_layer]++;
    }
    
    // Libera páginas antigas (a mais de 2 camadas de distância)
    for (int i = 0; i < 1024; i++) {
        chunk_weight_page_t* page = &ctx->weight_pages[i];
        if (page->ram_address && !page->is_locked) {
            int distance = abs((int)page->layer_id - (int)new_layer);
            if (distance > CHUNK_ACTIVE_LAYERS) {
                munmap(page->ram_address, CHUNK_WEIGHT_PAGE_SIZE);
                page->ram_address = NULL;
                ctx->ram_used_bytes -= CHUNK_WEIGHT_PAGE_SIZE;
            }
        }
    }
    
    ctx->current_layer = new_layer;
}

chunk_stats_t nmm_get_stats(chunk_nmm_context_t* ctx) {
    chunk_stats_t stats;
    memset(&stats, 0, sizeof(stats));
    stats.total_page_faults = ctx->page_fault_count;
    stats.total_prefetches = ctx->prefetch_hits + ctx->prefetch_misses;
    stats.cache_hit_rate = (double)ctx->prefetch_hits / 
                           (ctx->prefetch_hits + ctx->page_fault_count + 1);
    return stats;
}

void nmm_set_ram_limit(chunk_nmm_context_t* ctx, size_t limit_bytes) {
    ctx->ram_limit_bytes = limit_bytes;
}

void nmm_set_eviction_policy(chunk_nmm_context_t* ctx, chunk_eviction_policy_t policy) {
    // Política configurada no NMM
}

int nmm_shutdown(chunk_nmm_context_t* ctx) {
    prefetch_running = 0;
    pthread_join(prefetch_thread, NULL);
    free(ctx->weight_pages);
    free(ctx->kv_pages);
    free(ctx);
    return 0;
}
