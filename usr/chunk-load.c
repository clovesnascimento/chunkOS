#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../kernel/nmm.h"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Uso: %s <modelo> [--ram-limit MB] [--prefetch N]\n", argv[0]);
        return 1;
    }
    
    char* model_name = argv[1];
    size_t ram_limit = CHUNK_DEFAULT_RAM_LIMIT_MB;
    int prefetch = CHUNK_PREFETCH_LOOKAHEAD;
    
    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--ram-limit") == 0 && i + 1 < argc) {
            ram_limit = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--prefetch") == 0 && i + 1 < argc) {
            prefetch = atoi(argv[++i]);
        }
    }
    
    printf("🔧 CHUNK Model Loader\n");
    printf("Modelo: %s\n", model_name);
    printf("RAM Limit: %zu MB\n", ram_limit);
    printf("Prefetch Lookahead: %d layers\n", prefetch);
    
    chunk_nmm_context_t* ctx = nmm_init();
    if (!ctx) return 1;
    
    nmm_set_ram_limit(ctx, ram_limit * 1024 * 1024);
    
    if (nmm_load_model(ctx, model_name) == 0) {
        printf("✅ Modelo %s carregado (lazy loading ativado)\n", model_name);
    } else {
        printf("❌ Falha ao carregar modelo\n");
    }
    
    nmm_shutdown(ctx);
    return 0;
}
