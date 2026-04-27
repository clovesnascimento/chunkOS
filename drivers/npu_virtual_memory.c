#include "npu_virtual_memory.h"
#include "../kernel/nmm.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <signal.h>
#include <unistd.h>

static chunk_nmm_context_t* global_ctx = NULL;
static void* global_virtual_base = NULL;
static uint64_t global_virtual_size = 0;
static uint32_t page_size = 4096;
static int auto_prefetch = 1;

// Forward declaration if not in nmm.h
// int handle_page_fault(chunk_nmm_context_t* ctx, chunk_layer_t layer, uint32_t page_idx);

// Registra handler de page fault (simulado)
int npu_register_virtual_region(chunk_nmm_context_t* ctx,
                                void* base,
                                uint64_t size) {
    global_ctx = ctx;
    global_virtual_base = base;
    global_virtual_size = size;
    
    printf("[NPU] Região virtual registrada: %p - %p (%lu bytes)\n",
           base, (char*)base + size, size);
    
    return 0;
}

void* npu_create_virtual_region(uint64_t model_size) {
    void* region = mmap(NULL, model_size,
                        PROT_READ | PROT_WRITE,
                        MAP_ANONYMOUS | MAP_PRIVATE | MAP_NORESERVE,
                        -1, 0);
    
    if (region == MAP_FAILED) {
        perror("npu_create_virtual_region");
        return NULL;
    }
    
    // Protege para gerar page faults
    mprotect(region, model_size, PROT_NONE);
    
    global_virtual_base = region;
    global_virtual_size = model_size;
    
    return region;
}

int npu_map_model_to_virtual(chunk_nmm_context_t* ctx,
                             const char* model_name,
                             void* virtual_base) {
    printf("[NPU] Mapeando modelo %s para região virtual %p\n",
           model_name, virtual_base);
    
    // Simulação: carrega metadados do modelo
    // Em uma implementação real, leríamos o meta_path
    
    // Registra região
    return npu_register_virtual_region(ctx, virtual_base, 1024 * 1024 * 1024); // 1GB default
}

void npu_set_page_size(uint32_t size) {
    page_size = size;
    printf("[NPU] Page size set to %u bytes\n", size);
}

void npu_set_auto_prefetch(int enabled) {
    auto_prefetch = enabled;
    printf("[NPU] Auto-prefetch %s\n", enabled ? "enabled" : "disabled");
}
