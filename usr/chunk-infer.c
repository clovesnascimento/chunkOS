#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "../kernel/nmm.h"
#include "../lib/libkvcompress.h"
#include "../lib/libprefetch.h"

void print_banner() {
    printf("    ██████╗██╗  ██╗██╗   ██╗███╗   ██╗██╗  ██╗\n");
    printf("   ██╔════╝██║  ██║██║   ██║████╗  ██║██║ ██╔╝\n");
    printf("   ██║     ███████║██║   ██║██╔██╗ ██║█████╔╝ \n");
    printf("   ██║     ██╔══██║██║   ██║██║╚██╗██║██╔═██╗ \n");
    printf("   ╚██████╗██║  ██║╚██████╔╝██║ ╚████║██║  ██╗\n");
    printf("    ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝\n\n");
    printf("   CHUNK OS v1.0.0 — Cognitive Inference Engine\n");
    printf("   CNGSM — Cloves Nascimento\n\n");
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Uso: %s <modelo> <prompt>\n", argv[0]);
        return 1;
    }
    
    char* model_name = argv[1];
    char* prompt = argv[2];
    
    print_banner();
    
    printf("[Sistema] Inicializando NMM...\n");
    chunk_nmm_context_t* ctx = nmm_init();
    if (!ctx) {
        fprintf(stderr, "Erro ao inicializar NMM\n");
        return 1;
    }
    
    printf("[Sistema] Carregando modelo: %s\n", model_name);
    if (nmm_load_model(ctx, model_name) != 0) {
        fprintf(stderr, "Erro ao carregar modelo %s\n", model_name);
        return 1;
    }
    
    printf("[Inferência] Prompt: \"%s\"\n", prompt);
    printf("[Inferência] Gerando tokens...\n\n");
    
    // Simulação de loop de inferência por camadas
    for (int t = 0; t < 10; t++) {
        for (uint32_t l = 0; l < 32; l++) {
            // Simula acesso a pesos (causa page faults e prefetch)
            nmm_advance_layer(ctx, l);
            usleep(10000); // Simula processamento
        }
        printf("Token %d: [OK]\n", t);
    }
    
    printf("\n[Sistema] Inferência concluída.\n");
    
    chunk_stats_t stats = nmm_get_stats(ctx);
    printf("------------------------------------\n");
    printf("Estatísticas de Memória Neural:\n");
    printf("Page Faults: %lu\n", stats.total_page_faults);
    printf("Prefetch Hits: %lu\n", stats.total_prefetches);
    printf("RAM Used: %zu MB\n", ctx->ram_used_bytes / (1024 * 1024));
    printf("------------------------------------\n");
    
    nmm_shutdown(ctx);
    return 0;
}
