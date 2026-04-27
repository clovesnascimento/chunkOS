#include "libkvcompress.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define MAX_KV_TOKENS 16384

typedef struct {
    chunk_token_t token;
    void* k;
    void* v;
    size_t size;
    float importance;
    uint64_t timestamp;
} kv_entry_t;

static kv_entry_t cache[MAX_KV_TOKENS];
static int cache_count = 0;
static chunk_kv_compression_t current_method = CHUNK_KV_COMPRESS_HYBRID;
static float current_ratio = 0.1f;
static int current_window = 1024;

int kv_compress_init(chunk_kv_compression_t method, float ratio) {
    current_method = method;
    current_ratio = ratio;
    memset(cache, 0, sizeof(cache));
    cache_count = 0;
    return 0;
}

int kv_cache_add(chunk_token_t token, void* k, void* v, size_t size) {
    if (cache_count >= MAX_KV_TOKENS) {
        kv_apply_compression();
    }
    
    kv_entry_t* entry = &cache[cache_count++];
    entry->token = token;
    entry->k = malloc(size);
    entry->v = malloc(size);
    memcpy(entry->k, k, size);
    memcpy(entry->v, v, size);
    entry->size = size;
    entry->importance = 1.0f; // Default
    static uint64_t time_counter = 0;
    entry->timestamp = time_counter++;
    
    return 0;
}

int kv_apply_compression(void) {
    if (current_method == CHUNK_KV_COMPRESS_NONE) return 0;
    
    printf("[KV] Aplicando compressão: %d (ratio: %.2f)\n", 
           current_method, current_ratio);
    
    // Simulação: remove tokens menos importantes ou fora da janela
    int kept = 0;
    for (int i = 0; i < cache_count; i++) {
        int is_recent = (cache_count - i) < current_window;
        int is_important = cache[i].importance > (1.0f - current_ratio);
        
        if (is_recent || is_important) {
            if (kept != i) {
                cache[kept] = cache[i];
            }
            kept++;
        } else {
            free(cache[i].k);
            free(cache[i].v);
        }
    }
    
    cache_count = kept;
    return 0;
}

double kv_get_compression_ratio(void) {
    return (double)cache_count / MAX_KV_TOKENS;
}

size_t kv_get_memory_usage(void) {
    size_t total = 0;
    for (int i = 0; i < cache_count; i++) {
        total += cache[i].size * 2;
    }
    return total;
}
