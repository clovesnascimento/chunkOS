#ifndef NPU_VIRTUAL_MEMORY_H
#define NPU_VIRTUAL_MEMORY_H

#include "../include/chunk_types.h"

// Registra região de memória virtual para NPU
int npu_register_virtual_region(chunk_nmm_context_t* ctx,
                                void* base,
                                uint64_t size);

// Cria região de memória virtual para mapeamento
void* npu_create_virtual_region(uint64_t model_size);

// Mapeia modelo para espaço virtual da NPU
int npu_map_model_to_virtual(chunk_nmm_context_t* ctx,
                             const char* model_name,
                             void* virtual_base);

// Configura tamanho da página virtual
void npu_set_page_size(uint32_t page_size);

// Habilita/desabilita prefetch automático
void npu_set_auto_prefetch(int enabled);

#endif
