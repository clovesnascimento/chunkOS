#ifndef CHUNK_TYPES_H
#define CHUNK_TYPES_H

#include <stdint.h>
#include <stddef.h>

// Tipos fundamentais do CHUNK OS
typedef uint64_t chunk_addr_t;
typedef uint32_t chunk_layer_t;
typedef uint64_t chunk_token_t;

// Página de pesos - 256KB
#define CHUNK_WEIGHT_PAGE_SIZE (256 * 1024)

// Página KV - 64KB  
#define CHUNK_KV_PAGE_SIZE (64 * 1024)

// Máximo de camadas ativas simultâneas
#define CHUNK_ACTIVE_LAYERS 3

// Lookahead do prefetch
#define CHUNK_PREFETCH_LOOKAHEAD 2

// Limite de RAM (default 1.5GB)
#define CHUNK_DEFAULT_RAM_LIMIT_MB 1536

// Estrutura de página de pesos
typedef struct {
    chunk_layer_t layer_id;
    uint32_t page_index;
    uint64_t flash_offset;
    void* ram_address;
    uint8_t is_locked;
    uint64_t last_access_time;
    uint32_t access_count;
    float importance_score;
} chunk_weight_page_t;

// Estrutura de página KV cache
typedef struct {
    chunk_token_t token_id;
    uint32_t kv_hash;
    float attention_score;
    uint8_t is_in_ram;
    void* ram_address;
    uint32_t size_bytes;
} chunk_kv_page_t;

// Contexto do NMM (Neural Memory Manager)
typedef struct {
    chunk_weight_page_t* weight_pages;
    uint32_t weight_page_count;
    chunk_kv_page_t* kv_pages;
    uint32_t kv_page_count;
    chunk_layer_t current_layer;
    uint64_t page_fault_count;
    uint64_t prefetch_hits;
    uint64_t prefetch_misses;
    size_t ram_used_bytes;
    size_t ram_limit_bytes;
    void* virtual_region;
    uint64_t virtual_size;
} chunk_nmm_context_t;

// Estatísticas do sistema
typedef struct {
    uint64_t total_pages_loaded;
    uint64_t total_page_faults;
    uint64_t total_prefetches;
    double avg_page_fault_latency_us;
    double kv_compression_ratio;
    double cache_hit_rate;
} chunk_stats_t;

#endif
