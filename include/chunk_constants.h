#ifndef CHUNK_CONSTANTS_H
#define CHUNK_CONSTANTS_H

// Constantes de sistema
#define CHUNK_VERSION "1.0.0"
#define CHUNK_MAGIC 0x4348554E4B // "CHUNK" em hex

// Caminhos do sistema de arquivos
#define CHUNK_WEIGHT_PATH "/chunk/models/weights"
#define CHUNK_META_PATH "/chunk/models/registry"
#define CHUNK_PROC_PATH "/proc/chunk"

// Limiares de desempenho
#define CHUNK_MIN_CONFIDENCE 0.3f
#define CHUNK_MAX_LAYERS 1024
#define CHUNK_MAX_PAGES_PER_LAYER 65536

// Timeouts (microsegundos)
#define CHUNK_PREFETCH_POLL_US 100
#define CHUNK_DMA_TIMEOUT_US 10000

// Flags de página
#define CHUNK_PAGE_FLAG_LOCKED  0x01
#define CHUNK_PAGE_FLAG_DIRTY   0x02
#define CHUNK_PAGE_FLAG_PREFETCH 0x04

// Algoritmos de evicção
typedef enum {
    CHUNK_EVICT_LRU,
    CHUNK_EVICT_LFU,
    CHUNK_EVICT_IMPORTANCE,
    CHUNK_EVICT_DISTANCE_AWARE
} chunk_eviction_policy_t;

// Modos de compressão KV
typedef enum {
    CHUNK_KV_COMPRESS_NONE,
    CHUNK_KV_COMPRESS_TOP_K,
    CHUNK_KV_COMPRESS_WINDOW,
    CHUNK_KV_COMPRESS_HYBRID
} chunk_kv_compression_t;

#endif
