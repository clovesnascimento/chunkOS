#include "../kernel/nmm.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void print_usage(const char* prog) {
    printf("Uso: %s [opções] <modelo>\n", prog);
    printf("Opções:\n");
    printf("  --ram-limit <MB>   Limite de RAM (default: 1536)\n");
    printf("  --prefetch <N>     Lookahead do prefetch (default: 2)\n");
    printf("  --policy <policy>  Política de evicção: lru|lfu|importance\n");
    printf("  --list             Lista modelos disponíveis\n");
    printf("  --unload <model>   Descarrega modelo\n");
}

void list_models(void) {
    printf("Modelos disponíveis:\n");
    printf("  📦 llama-3-8b      (8B parâmetros, ~16GB)\n");
    printf("  📦 mixtral-8x7b    (47B parâmetros, ~32GB)\n");
    printf("  📦 gemma-2b        (2B parâmetros, ~4GB)\n");
    printf("  📦 phi-2           (2.7B parâmetros, ~5.4GB)\n");
}

int main(int argc, char** argv) {
    const char* model = NULL;
    int ram_limit_mb = 1536;
    int prefetch_lookahead = 2;
    const char* policy = "importance";
    int list_only = 0;
    
    // Parse arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--list") == 0) {
            list_only = 1;
        } else if (strcmp(argv[i], "--ram-limit") == 0 && i+1 < argc) {
            ram_limit_mb = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--prefetch") == 0 && i+1 < argc) {
            prefetch_lookahead = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--policy") == 0 && i+1 < argc) {
            policy = argv[++i];
        } else if (argv[i][0] != '-') {
            model = argv[i];
        } else {
            print_usage(argv[0]);
            return 1;
        }
    }
    
    if (list_only) {
        list_models();
        return 0;
    }
    
    if (!model) {
        fprintf(stderr, "Erro: Nenhum modelo especificado\n");
        print_usage(argv[0]);
        return 1;
    }
    
    printf("╔════════════════════════════════════════════╗\n");
    printf("║     CHUNK OS - Model Loader               ║\n");
    printf("╠════════════════════════════════════════════╣\n");
    printf("║ Modelo: %-32s ║\n", model);
    printf("║ RAM Limit: %d MB%29s ║\n", ram_limit_mb, "");
    printf("║ Prefetch: %d%33s ║\n", prefetch_lookahead, "");
    printf("║ Policy: %-33s ║\n", policy);
    printf("╚════════════════════════════════════════════╝\n");
    
    // Inicializa NMM
    chunk_nmm_context_t* ctx = nmm_init();
    if (!ctx) {
        fprintf(stderr, "Erro ao inicializar NMM\n");
        return 1;
    }
    
    // Configura limites
    nmm_set_ram_limit(ctx, (size_t)ram_limit_mb * 1024 * 1024);
    
    // Configura política de evicção
    if (strcmp(policy, "lru") == 0) {
        nmm_set_eviction_policy(ctx, CHUNK_EVICT_LRU);
    } else if (strcmp(policy, "lfu") == 0) {
        nmm_set_eviction_policy(ctx, CHUNK_EVICT_LFU);
    } else {
        nmm_set_eviction_policy(ctx, CHUNK_EVICT_IMPORTANCE);
    }
    
    // Carrega modelo
    printf("\n🔄 Carregando modelo %s...\n", model);
    if (nmm_load_model(ctx, model) != 0) {
        fprintf(stderr, "Erro ao carregar modelo\n");
        nmm_shutdown(ctx);
        return 1;
    }
    
    printf("✅ Modelo %s carregado com sucesso!\n", model);
    printf("   Memória RAM utilizada: 0 / %d MB (carregamento preguiçoso)\n", ram_limit_mb);
    
    nmm_shutdown(ctx);
    return 0;
}
