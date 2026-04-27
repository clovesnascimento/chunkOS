#ifndef NMM_H
#define NMM_H

#include <stdint.h>
#include <stddef.h>

#define CHUNK_WEIGHT_PAGE_SIZE (256 * 1024)
#define CHUNK_KV_PAGE_SIZE (64 * 1024)
#define CHUNK_ACTIVE_LAYERS 3
#define CHUNK_PREFETCH_LOOKAHEAD 2
#define CHUNK_DEFAULT_RAM_LIMIT_MB 1536

typedef struct {
    uint32_t layer_id;
    uint32_t page_index;
    uint64_t flash_offset;
    void* ram_address;
    uint8_t is_locked;
    uint64_t last_access_time;
    uint32_t access_count;
    float importance_score;
} chunk_weight_page_t;

typedef struct {
    uint64_t total_page_faults;
    uint64_t total_prefetches;
    double cache_hit_rate;
    size_t ram_used_bytes;
} chunk_stats_t;

typedef struct chunk_nmm_context chunk_nmm_context_t;

chunk_nmm_context_t* nmm_init(void);
int nmm_load_model(chunk_nmm_context_t* ctx, const char* model_path);
void* nmm_get_weights(chunk_nmm_context_t* ctx, uint32_t layer, uint32_t offset, uint32_t size);
void nmm_advance_layer(chunk_nmm_context_t* ctx, uint32_t new_layer);
chunk_stats_t nmm_get_stats(chunk_nmm_context_t* ctx);
void nmm_shutdown(chunk_nmm_context_t* ctx);

#endif
