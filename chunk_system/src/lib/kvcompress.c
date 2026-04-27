#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct {
    float* keys;
    float* values;
    float* attention_scores;
    uint32_t length;
    uint32_t compressed_length;
} kv_cache_t;

kv_cache_t* kv_hybrid_compress(kv_cache_t* src, uint32_t window_size, float sparsity) {
    if (src->length <= window_size) return src;
    
    uint32_t old_tokens = src->length - window_size;
    uint32_t kept_old = (uint32_t)(old_tokens * sparsity);
    uint32_t new_size = window_size + kept_old;
    
    kv_cache_t* compressed = malloc(sizeof(kv_cache_t));
    compressed->keys = malloc(new_size * sizeof(float));
    compressed->values = malloc(new_size * sizeof(float));
    compressed->attention_scores = malloc(new_size * sizeof(float));
    compressed->length = src->length;
    compressed->compressed_length = new_size;
    
    // Copia janela recente
    uint32_t window_start = src->length - window_size;
    for (uint32_t i = 0; i < window_size; i++) {
        compressed->keys[i] = src->keys[window_start + i];
        compressed->values[i] = src->values[window_start + i];
        compressed->attention_scores[i] = src->attention_scores[window_start + i];
    }
    
    printf("[KVCompress] Comprimido de %u para %u tokens (%.1f%%)\n",
           src->length, new_size, (float)new_size / src->length * 100);
    
    return compressed;
}

void kv_cache_free(kv_cache_t* cache) {
    if (cache) {
        free(cache->keys);
        free(cache->values);
        free(cache->attention_scores);
        free(cache);
    }
}
