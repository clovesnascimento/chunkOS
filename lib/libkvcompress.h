#ifndef LIBKVCOMPRESS_H
#define LIBKVCOMPRESS_H

#include <stdint.h>
#include <stddef.h>

typedef struct {
    float* keys;
    float* values;
    float* attention_scores;
    uint32_t original_length;
    uint32_t compressed_length;
    float compression_ratio;
} kv_context_t;

// Compressão Top-K: mantém apenas os K tokens mais importantes
kv_context_t* kv_compress_topk(kv_context_t* ctx, uint32_t k);

// Compressão com janela: mantém W tokens recentes + resto esparso
kv_context_t* kv_compress_window(kv_context_t* ctx, uint32_t window_size, float sparsity);

// Compressão híbrida (recomendada)
kv_context_t* kv_compress_hybrid(kv_context_t* ctx, 
                                 uint32_t window_size, 
                                 float sparsity_ratio);

// Utilitários
void kv_context_free(kv_context_t* ctx);
float kv_calculate_importance(kv_context_t* ctx, uint32_t token_idx);

#endif
