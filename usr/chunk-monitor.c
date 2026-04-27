#include "../kernel/nmm.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>

static volatile int running = 1;

void signal_handler(int sig) {
    if (sig == SIGINT || sig == SIGTERM) {
        running = 0;
    }
}

void print_bar(double percentage, int width, const char* color) {
    int filled = (int)(percentage * width);
    printf("%s[", color);
    for (int i = 0; i < width; i++) {
        printf(i < filled ? "█" : "░");
    }
    printf("\033[0m] %.1f%%", percentage * 100);
}

int main(int argc, char** argv) {
    (void)argc; (void)argv;
    signal(SIGINT, signal_handler);
    
    printf("\n╔══════════════════════════════════════════════════════════════╗\n");
    printf("║              CHUNK OS - System Monitor                       ║\n");
    printf("║                    Pressione Ctrl+C para sair                 ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n\n");
    
    // Simulação de monitoramento (em produção, leria de /proc/chunk)
    uint64_t page_faults = 0;
    uint64_t prefetch_hits = 0;
    double ram_usage = 0;
    
    while (running) {
        printf("\033[H\033[J"); // Clear screen
        
        printf("╔══════════════════════════════════════════════════════════════╗\n");
        printf("║                    📊 ESTATÍSTICAS DO SISTEMA                 ║\n");
        printf("╠══════════════════════════════════════════════════════════════╣\n");
        
        // Memória
        printf("║ 💾 MEMÓRIA                                                    ║\n");
        printf("║    RAM Usage:    ");
        print_bar(ram_usage, 30, "\033[32m");
        printf(" %5.1f MB / 1536 MB\n", ram_usage * 1536);
        
        // Page Faults
        printf("║ ⚡ PAGE FAULTS                                                ║\n");
        printf("║    Total:        %12llu                                       ║\n", (unsigned long long)page_faults);
        
        // Prefetch
        printf("║ 🚀 PREFETCH                                                   ║\n");
        printf("║    Hits:         %12llu                                       ║\n", (unsigned long long)prefetch_hits);
        printf("║    Hit Rate:     %12.1f%%                                     ║\n",
               prefetch_hits + page_faults > 0 ? 
               100.0 * prefetch_hits / (prefetch_hits + page_faults) : 0);
        
        // DMA
        printf("║ 💿 DMA                                                       ║\n");
        printf("║    Transfers:    %12llu                                       ║\n", 
               (unsigned long long)(prefetch_hits + page_faults) / 10);
        printf("║    Throughput:   %12.1f MB/s                                  ║\n", 
               (prefetch_hits + page_faults) * 0.256);
        
        printf("╚══════════════════════════════════════════════════════════════╝\n");
        printf("\n  🔄 Atualizando a cada 1 segundo... (Ctrl+C para sair)\n");
        
        // Simula atualização das métricas
        page_faults += rand() % 5;
        prefetch_hits += rand() % 15;
        ram_usage = (ram_usage + (rand() % 100) / 1000.0);
        if (ram_usage > 0.95) ram_usage = 0.95;
        
        sleep(1);
    }
    
    printf("\n👋 Monitor encerrado.\n");
    return 0;
}
