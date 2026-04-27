#include "libkvcompress.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Quickselect para encontrar top-k
static void quickselect(float* arr, uint32_t* idx, int left, int right, int k) {
    if (left >= right) return;
    
    float pivot = arr[left];
    uint32_t pivot_idx = idx[left];
    int i = left, j = right;
    
    while (i < j) {
        while (i < j && arr[j] <= pivot) j--;
        if (i < j) {
            arr[i] = arr[j];
            idx[i] = idx[j];
            i++;
        }
        while (i < j && arr[i] >= pivot) i++;
        if (i < j) {
            arr[j] = arr[i];
            idx[j] = idx[i];
            j--;
        }
    }
    arr[i] = pivot;
    idx[i] = pivot_idx;
    
    if (i == k) return;
    if (i < k) quickselect(arr, idx, i + 1, right, k);
    else quickselect(arr, idx, left, i - 1, k);
}

// Calcula importância de cada token
float kv_calculate_importance(kv_context_t* ctx, uint32_t token_idx) {
    float attention = ctx->attention_scores[token_idx];
    float recency = exp(-(float)token_idx / (ctx->original_length > 0 ? ctx->original_length : 1));
    return attention * (1.0f + recency);
}

// Compressão Top-K
kv_context_t* kv_compress_topk(kv_context_t* ctx, uint32_t k) {
    if (k >= ctx->original_length) return ctx;
    
    // Cria array de índices e calcula importâncias
    uint32_t* indices = malloc(ctx->original_length * sizeof(uint32_t));
    float* scores = malloc(ctx->original_length * sizeof(float));
    
    for (uint32_t i = 0; i < ctx->original_length; i++) {
        indices[i] = i;
        scores[i] = kv_calculate_importance(ctx, i);
    }
    
    // Seleciona top-k
    quickselect(scores, indices, 0, ctx->original_length - 1, k);
    
    // Cria contexto comprimido
    kv_context_t* compressed = malloc(sizeof(kv_context_t));
    compressed->keys = malloc(k * sizeof(float));
    compressed->values = malloc(k * sizeof(float));
    compressed->attention_scores = malloc(k * sizeof(float));
    compressed->original_length = ctx->original_length;
    compressed->compressed_length = k;
    compressed->compression_ratio = (float)k / ctx->original_length;
    
    for (uint32_t i = 0; i < k; i++) {
        uint32_t orig_idx = indices[i];
        compressed->keys[i] = ctx->keys[orig_idx];
        compressed->values[i] = ctx->values[orig_idx];
        compressed->attention_scores[i] = ctx->attention_scores[orig_idx];
    }
    
    free(indices);
    free(scores);
    
    return compressed;
}

// Compressão híbrida simplificada
kv_context_t* kv_compress_hybrid(kv_context_t* ctx, 
                                 uint32_t window_size, 
                                 float sparsity_ratio) {
    if (ctx->original_length <= window_size) return ctx;
    
    uint32_t sparse_size = (ctx->original_length - window_size) * sparsity_ratio;
    uint32_t total = window_size + sparse_size;
    
    // Cria contexto com janela completa + Top-K do resto
    kv_context_t* result = malloc(sizeof(kv_context_t));
    result->keys = malloc(total * sizeof(float));
    result->values = malloc(total * sizeof(float));
    result->attention_scores = malloc(total * sizeof(float));
    result->original_length = ctx->original_length;
    result->compressed_length = total;
    result->compression_ratio = (float)total / ctx->original_length;
    
    // Copia janela recente
    for (uint32_t i = 0; i < window_size; i++) {
        uint32_t orig_idx = ctx->original_length - window_size + i;
        result->keys[i] = ctx->keys[orig_idx];
        result->values[i] = ctx->values[orig_idx];
        result->attention_scores[i] = ctx->attention_scores[orig_idx];
    }
    
    // Comprime parte antiga com Top-K
    kv_context_t* old_part = malloc(sizeof(kv_context_t));
    old_part->original_length = ctx->original_length - window_size;
    old_part->keys = ctx->keys;
    old_part->values = ctx->values;
    old_part->attention_scores = ctx->attention_scores;
    
    kv_context_t* compressed_old = kv_compress_topk(old_part, sparse_size);
    
    // Copia parte comprimida
    for (uint32_t i = 0; i < sparse_size; i++) {
        result->keys[window_size + i] = compressed_old->keys[i];
        result->values[window_size + i] = compressed_old->values[i];
        result->attention_scores[window_size + i] = compressed_old->attention_scores[i];
    }
    
    kv_context_free(compressed_old);
    free(old_part);
    
    return result;
}

void kv_context_free(kv_context_t* ctx) {
    if (!ctx) return;
    free(ctx->keys);
    free(ctx->values);
    free(ctx->attention_scores);
    free(ctx);
}
