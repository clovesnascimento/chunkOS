#include "nmm.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>

struct chunk_nmm_context {
    chunk_weight_page_t* weight_pages;
    uint32_t page_count;
    uint32_t current_layer;
    uint64_t page_fault_count;
    uint64_t prefetch_hits;
    size_t ram_used_bytes;
    size_t ram_limit_bytes;
    void* virtual_region;
    pthread_t prefetch_thread;
    volatile int prefetch_running;
};

static void* prefetch_worker(void* arg) {
    chunk_nmm_context_t* ctx = (chunk_nmm_context_t*)arg;
    while (ctx->prefetch_running) {
        uint32_t next_layer = ctx->current_layer + 1;
        for (int i = 0; i < CHUNK_PREFETCH_LOOKAHEAD; i++) {
            uint32_t layer_to_load = next_layer + i;
            for (uint32_t p = 0; p < ctx->page_count; p++) {
                if (ctx->weight_pages[p].layer_id == layer_to_load && 
                    !ctx->weight_pages[p].ram_address) {
                    // Simulação de pré-carga
                    ctx->prefetch_hits++;
                    break;
                }
            }
        }
        usleep(10000);
    }
    return NULL;
}

chunk_nmm_context_t* nmm_init(void) {
    chunk_nmm_context_t* ctx = calloc(1, sizeof(chunk_nmm_context_t));
    if (!ctx) return NULL;
    
    ctx->weight_pages = malloc(1024 * sizeof(chunk_weight_page_t));
    ctx->ram_limit_bytes = CHUNK_DEFAULT_RAM_LIMIT_MB * 1024 * 1024;
    ctx->prefetch_running = 1;
    
    pthread_create(&ctx->prefetch_thread, NULL, prefetch_worker, ctx);
    
    printf("[NMM] Inicializado com sucesso\n");
    return ctx;
}

int nmm_load_model(chunk_nmm_context_t* ctx, const char* model_path) {
    printf("[NMM] Carregando modelo: %s\n", model_path);
    ctx->page_count = 32 * 1024;  // Simulação: 32 camadas * 1024 páginas
    return 0;
}

void* nmm_get_weights(chunk_nmm_context_t* ctx, uint32_t layer, uint32_t offset, uint32_t size) {
    // Simulação: retorna memória alocada
    void* ptr = mmap(NULL, size, PROT_READ | PROT_WRITE, 
                     MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (ptr != MAP_FAILED) {
        ctx->ram_used_bytes += size;
        printf("[NMM] Carregou layer %d, offset %d (%u bytes)\n", layer, offset, size);
    }
    return ptr == MAP_FAILED ? NULL : ptr;
}

void nmm_advance_layer(chunk_nmm_context_t* ctx, uint32_t new_layer) {
    ctx->current_layer = new_layer;
    printf("[NMM] Avançou para layer %d\n", new_layer);
}

chunk_stats_t nmm_get_stats(chunk_nmm_context_t* ctx) {
    chunk_stats_t stats = {
        .total_page_faults = ctx->page_fault_count,
        .total_prefetches = ctx->prefetch_hits,
        .cache_hit_rate = (double)ctx->prefetch_hits / (ctx->page_fault_count + ctx->prefetch_hits + 1),
        .ram_used_bytes = ctx->ram_used_bytes
    };
    return stats;
}

void nmm_shutdown(chunk_nmm_context_t* ctx) {
    ctx->prefetch_running = 0;
    pthread_join(ctx->prefetch_thread, NULL);
    free(ctx->weight_pages);
    free(ctx);
    printf("[NMM] Encerrado\n");
}
