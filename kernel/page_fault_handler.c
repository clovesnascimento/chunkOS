#include "../include/chunk_types.h"
#include "nmm.h"
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

// Protótipo interno (implementado no nmm.c ou nmm.h)
extern int handle_page_fault(chunk_nmm_context_t* ctx, chunk_layer_t layer, uint32_t page_idx);

// Contexto global para o handler de page fault
static chunk_nmm_context_t* fault_handler_ctx = NULL;
static void* fault_virtual_region = NULL;
static uint64_t fault_virtual_size = 0;

// Mapeia endereço virtual para (layer, page, offset)
static int virtual_to_chunk(void* fault_addr,
                            chunk_layer_t* layer,
                            uint32_t* page_idx,
                            uint32_t* offset) {
    uint64_t addr = (uint64_t)fault_addr;
    uint64_t base = (uint64_t)fault_virtual_region;
    uint64_t relative = addr - base;
    
    if (relative >= fault_virtual_size) return -1;
    
    // Layout: [layer:4bytes][page:4bytes][offset:4bytes]
    *layer = (relative >> 32) & 0xFFFFFFFF;
    *page_idx = (relative >> 20) & 0xFFF;
    *offset = relative & 0xFFFFF;
    
    return 0;
}

// Signal handler para SIGSEGV
static void chunk_page_fault_handler(int sig, siginfo_t* info, void* context) {
    (void)sig; (void)context;
    void* fault_addr = info->si_addr;
    
    chunk_layer_t layer;
    uint32_t page_idx, offset;
    
    if (virtual_to_chunk(fault_addr, &layer, &page_idx, &offset) == 0) {
        // É um page fault gerenciado pelo CHUNK
        if (fault_handler_ctx) {
            // Tenta resolver o page fault
            int resolved = handle_page_fault(fault_handler_ctx, layer, page_idx);
            if (resolved == 0) {
                // Page fault resolvido, retorna
                return;
            }
        }
    }
    
    // Page fault não resolvido - erro fatal
    fprintf(stderr, "CHUNK: Page fault não tratado em %p\n", fault_addr);
    exit(1);
}

// Registra região de memória virtual para a NPU
int chunk_register_virtual_region(chunk_nmm_context_t* ctx,
                                  void* base,
                                  uint64_t size) {
    fault_handler_ctx = ctx;
    fault_virtual_region = base;
    fault_virtual_size = size;
    
    // Registra handler de SIGSEGV
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_sigaction = chunk_page_fault_handler;
    sa.sa_flags = SA_SIGINFO;
    sigaction(SIGSEGV, &sa, NULL);
    
    return 0;
}

// Cria região de memória virtual para mapeamento de modelo
void* chunk_create_virtual_region(uint64_t model_size) {
    void* region = mmap(NULL, model_size,
                        PROT_READ | PROT_WRITE,
                        MAP_ANONYMOUS | MAP_PRIVATE | MAP_NORESERVE,
                        -1, 0);
    
    if (region == MAP_FAILED) return NULL;
    
    // Protege a região para gerar SIGSEGV no acesso
    mprotect(region, model_size, PROT_NONE);
    
    return region;
}
