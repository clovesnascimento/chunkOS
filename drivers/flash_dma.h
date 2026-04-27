#ifndef FLASH_DMA_H
#define FLASH_DMA_H

#include <stdint.h>
#include <stddef.h>

// Estrutura de canal DMA
typedef struct {
    int channel_id;
    int is_busy;
    void* src_addr;
    void* dst_addr;
    size_t size;
    void (*callback)(void*);
    void* callback_arg;
} dma_channel_t;

// Inicializa subsistema DMA
int dma_init(void);

// Obtém canal DMA disponível
dma_channel_t* dma_get_channel(int channel_id);

// Transferência assíncrona
int dma_async_read(dma_channel_t* channel,
                   uint64_t flash_offset,
                   void* ram_addr,
                   size_t size,
                   void (*callback)(void*),
                   void* arg);

// Transferência síncrona
int dma_sync_read(dma_channel_t* channel,
                  uint64_t flash_offset,
                  void* ram_addr,
                  size_t size);

// Espera conclusão de transferência
int dma_wait_completion(dma_channel_t* channel, int timeout_us);

// Estatísticas DMA
uint64_t dma_get_total_bytes_transferred(void);
uint64_t dma_get_transaction_count(void);

#endif
