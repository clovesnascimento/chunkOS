#include "flash_dma.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <pthread.h>

#define MAX_DMA_CHANNELS 4
#define DMA_PAGE_SIZE (256 * 1024)

static dma_channel_t channels[MAX_DMA_CHANNELS];
static uint64_t total_bytes = 0;
static uint64_t transaction_count = 0;
static pthread_mutex_t dma_mutex = PTHREAD_MUTEX_INITIALIZER;

// Simulação de DMA worker thread
static void* dma_worker(void* arg) {
    dma_channel_t* channel = (dma_channel_t*)arg;
    int fd = open("/dev/chunk_flash", O_RDONLY);
    
    if (fd < 0) {
        // Simulação: cria arquivo dummy se não existir
        fd = open("/tmp/chunk_flash_dummy", O_RDONLY | O_CREAT, 0644);
    }
    
    while (1) {
        if (channel->is_busy && channel->src_addr) {
            // Simula DMA read
            pread(fd, channel->dst_addr, channel->size,
                  (off_t)(uint64_t)channel->src_addr);
            
            pthread_mutex_lock(&dma_mutex);
            total_bytes += channel->size;
            transaction_count++;
            pthread_mutex_unlock(&dma_mutex);
            
            channel->is_busy = 0;
            
            if (channel->callback) {
                channel->callback(channel->callback_arg);
            }
        }
        usleep(10); // Polling
    }
    
    if (fd >= 0) close(fd);
    return NULL;
}

int dma_init(void) {
    memset(channels, 0, sizeof(channels));
    
    for (int i = 0; i < MAX_DMA_CHANNELS; i++) {
        channels[i].channel_id = i;
        pthread_t thread;
        pthread_create(&thread, NULL, dma_worker, &channels[i]);
        pthread_detach(thread);
    }
    
    printf("[DMA] Inicializado com %d canais\n", MAX_DMA_CHANNELS);
    return 0;
}

dma_channel_t* dma_get_channel(int channel_id) {
    if (channel_id < 0 || channel_id >= MAX_DMA_CHANNELS) {
        return NULL;
    }
    return &channels[channel_id];
}

int dma_async_read(dma_channel_t* channel,
                   uint64_t flash_offset,
                   void* ram_addr,
                   size_t size,
                   void (*callback)(void*),
                   void* arg) {
    if (!channel || channel->is_busy) return -1;
    
    channel->src_addr = (void*)(uint64_t)flash_offset;
    channel->dst_addr = ram_addr;
    channel->size = size;
    channel->callback = callback;
    channel->callback_arg = arg;
    channel->is_busy = 1;
    
    return 0;
}

int dma_sync_read(dma_channel_t* channel,
                  uint64_t flash_offset,
                  void* ram_addr,
                  size_t size) {
    if (!channel) return -1;
    
    // Espera canal ficar livre
    while (channel->is_busy) {
        usleep(100);
    }
    
    channel->src_addr = (void*)(uint64_t)flash_offset;
    channel->dst_addr = ram_addr;
    channel->size = size;
    channel->callback = NULL;
    channel->is_busy = 1;
    
    // Espera conclusão
    while (channel->is_busy) {
        usleep(100);
    }
    
    return 0;
}

int dma_wait_completion(dma_channel_t* channel, int timeout_us) {
    int elapsed = 0;
    while (channel->is_busy && elapsed < timeout_us) {
        usleep(100);
        elapsed += 100;
    }
    return channel->is_busy ? -1 : 0;
}

uint64_t dma_get_total_bytes_transferred(void) {
    pthread_mutex_lock(&dma_mutex);
    uint64_t bytes = total_bytes;
    pthread_mutex_unlock(&dma_mutex);
    return bytes;
}

uint64_t dma_get_transaction_count(void) {
    pthread_mutex_lock(&dma_mutex);
    uint64_t count = transaction_count;
    pthread_mutex_unlock(&dma_mutex);
    return count;
}
