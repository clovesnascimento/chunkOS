#ifndef LIBKVCOMPRESS_H
#define LIBKVCOMPRESS_H

#include "../include/chunk_types.h"
#include "../include/chunk_constants.h"

// API de compressão de KV Cache
int kv_compress_init(chunk_kv_compression_t method, float ratio);
int kv_compress_shutdown(void);

// Adiciona tokens ao cache
int kv_cache_add(chunk_token_t token, void* k, void* v, size_t size);

// Recupera tokens do cache
int kv_cache_get(chunk_token_t token, void** k, void** v, size_t* size);

// Aplica algoritmos de compressão
int kv_apply_compression(void);

// Estratégias específicas
int kv_compress_topk(int k);
int kv_compress_window(int window_size);
int kv_compress_hybrid(int window_size, float sparsity);

// Estatísticas de compressão
double kv_get_compression_ratio(void);
size_t kv_get_memory_usage(void);

#endif
