#ifndef NMM_H
#define NMM_H

#include "../include/chunk_types.h"
#include "../include/chunk_constants.h"

// API Principal do Neural Memory Manager
chunk_nmm_context_t* nmm_init(void);
int nmm_shutdown(chunk_nmm_context_t* ctx);

// Gerenciamento de modelos
int nmm_load_model(chunk_nmm_context_t* ctx, const char* model_path);
int nmm_unload_model(chunk_nmm_context_t* ctx);

// Operações de memória
void* nmm_get_weights(chunk_nmm_context_t* ctx, 
                      chunk_layer_t layer, 
                      uint32_t offset,
                      uint32_t size);

void nmm_release_weights(chunk_nmm_context_t* ctx, 
                         chunk_layer_t layer, 
                         uint32_t offset);

// Controle de fluxo de camadas
void nmm_advance_layer(chunk_nmm_context_t* ctx, chunk_layer_t new_layer);
chunk_layer_t nmm_get_current_layer(chunk_nmm_context_t* ctx);

// Cache KV
int nmm_kv_store(chunk_nmm_context_t* ctx, 
                 chunk_token_t token, 
                 void* keys, 
                 void* values,
                 uint32_t size);

void* nmm_kv_retrieve(chunk_nmm_context_t* ctx,
                      chunk_token_t token,
                      uint32_t* size);

// Compressão KV
void nmm_kv_compress(chunk_nmm_context_t* ctx, 
                     chunk_kv_compression_t method,
                     float sparsity_ratio);

// Estatísticas
chunk_stats_t nmm_get_stats(chunk_nmm_context_t* ctx);
void nmm_reset_stats(chunk_nmm_context_t* ctx);

// Configuração
void nmm_set_ram_limit(chunk_nmm_context_t* ctx, size_t limit_bytes);
void nmm_set_eviction_policy(chunk_nmm_context_t* ctx, 
                             chunk_eviction_policy_t policy);

#endif
