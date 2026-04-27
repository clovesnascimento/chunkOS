#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "../kernel/nmm.h"

void clear_screen() {
    printf("\033[H\033[J");
}

int main() {
    printf("📊 CHUNK System Monitor\n");
    
    // Em uma implementação real, leríamos de /proc/chunk ou via IPC
    // Aqui simulamos a leitura de estatísticas globais
    
    while (1) {
        clear_screen();
        printf("========================================\n");
        printf("   CHUNK OS - Monitor de Recursos      \n");
        printf("========================================\n\n");
        
        // Simulação de valores
        static float ram_usage = 1120.0f;
        ram_usage += (rand() % 10 - 5);
        
        printf("RAM Usage:      %.2f MB / 1536 MB\n", ram_usage);
        printf("Page Faults/s:  %d\n", rand() % 5);
        printf("Prefetch Hits:  %d%%\n", 70 + rand() % 10);
        printf("DMA Throughput: %d MB/s\n", 45 + rand() % 20);
        
        printf("\nCamadas Ativas:\n");
        int current = rand() % 32;
        printf("[");
        for (int i = 0; i < 32; i++) {
            if (i == current) printf("H");
            else if (abs(i - current) < 3) printf("A");
            else printf(".");
        }
        printf("]\n");
        printf("(H=Head, A=Active, .=Paged-out)\n");
        
        printf("\nConfiguração:\n");
        printf("Policy: Importance-based\n");
        printf("KV Cache: Hybrid (10%% sparsity)\n");
        
        printf("\nPresse Ctrl+C para sair\n");
        
        usleep(1000000);
    }
    
    return 0;
}
