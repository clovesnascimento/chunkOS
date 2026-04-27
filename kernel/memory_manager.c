#include "../include/chunk_types.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/mman.h>

// Algoritmos de evicção implementados
typedef enum {
    EVICT_LRU,
    EVICT_LFU,
    EVICT_MFU,
    EVICT_FIFO,
    EVICT_IMPORTANCE
} evict_algorithm_t;

static evict_algorithm_t current_algorithm = EVICT_IMPORTANCE;

// LRU - Least Recently Used
static chunk_weight_page_t* evict_lru(chunk_nmm_context_t* ctx) {
    chunk_weight_page_t* oldest = NULL;
    uint64_t oldest_time = (uint64_t)-1;
    
    for (int i = 0; i < 1024; i++) {
        chunk_weight_page_t* page = &ctx->weight_pages[i];
        if (page->ram_address && !page->is_locked) {
            if (page->last_access_time < oldest_time) {
                oldest_time = page->last_access_time;
                oldest = page;
            }
        }
    }
    return oldest;
}

// LFU - Least Frequently Used
static chunk_weight_page_t* evict_lfu(chunk_nmm_context_t* ctx) {
    chunk_weight_page_t* least_used = NULL;
    uint32_t min_access = (uint32_t)-1;
    
    for (int i = 0; i < 1024; i++) {
        chunk_weight_page_t* page = &ctx->weight_pages[i];
        if (page->ram_address && !page->is_locked) {
            if (page->access_count < min_access) {
                min_access = page->access_count;
                least_used = page;
            }
        }
    }
    return least_used;
}

// FIFO - First In First Out
static chunk_weight_page_t* evict_fifo(chunk_nmm_context_t* ctx) {
    static int cursor = 0;
    int start = cursor;
    
    for (int i = 0; i < 1024; i++) {
        int idx = (start + i) % 1024;
        chunk_weight_page_t* page = &ctx->weight_pages[idx];
        if (page->ram_address && !page->is_locked) {
            cursor = (idx + 1) % 1024;
            return page;
        }
    }
    return NULL;
}

// API pública de evicção
chunk_weight_page_t* select_victim_page(chunk_nmm_context_t* ctx) {
    switch (current_algorithm) {
        case EVICT_LRU:
            return evict_lru(ctx);
        case EVICT_LFU:
            return evict_lfu(ctx);
        case EVICT_FIFO:
            return evict_fifo(ctx);
        default:
            return evict_lru(ctx);
    }
}

void set_eviction_algorithm(chunk_eviction_policy_t policy) {
    switch (policy) {
        case CHUNK_EVICT_LRU:
            current_algorithm = EVICT_LRU;
            break;
        case CHUNK_EVICT_LFU:
            current_algorithm = EVICT_LFU;
            break;
        case CHUNK_EVICT_IMPORTANCE:
            current_algorithm = EVICT_LRU; // Simplificação
            break;
        default:
            current_algorithm = EVICT_LRU;
            break;
    }
}

// Gerenciamento de memória do sistema
void* chunk_alloc_aligned(size_t size, size_t alignment) {
    void* ptr = NULL;
    if (posix_memalign(&ptr, alignment, size) != 0) return NULL;
    return ptr;
}

void chunk_free_aligned(void* ptr) {
    free(ptr);
}

// Monitoramento de memória
size_t chunk_get_ram_usage(chunk_nmm_context_t* ctx) {
    return ctx->ram_used_bytes;
}

size_t chunk_get_ram_limit(chunk_nmm_context_t* ctx) {
    return ctx->ram_limit_bytes;
}

double chunk_get_memory_pressure(chunk_nmm_context_t* ctx) {
    if (ctx->ram_limit_bytes == 0) return 0.0;
    return (double)ctx->ram_used_bytes / ctx->ram_limit_bytes;
}
