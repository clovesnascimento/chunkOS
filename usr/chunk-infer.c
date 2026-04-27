#include "../kernel/nmm.h"
#include "../lib/libkvcompress.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Simula uma LLM simplificada para demonstração
typedef struct {
    chunk_nmm_context_t* nmm;
    uint32_t vocab_size;
    uint32_t max_length;
} llm_engine_t;

llm_engine_t* llm_init(const char* model_name) {
    llm_engine_t* engine = calloc(1, sizeof(llm_engine_t));
    engine->nmm = nmm_init();
    engine->vocab_size = 32000;
    engine->max_length = 2048;
    
    if (nmm_load_model(engine->nmm, model_name) != 0) {
        fprintf(stderr, "Erro ao carregar modelo %s\n", model_name);
        nmm_shutdown(engine->nmm);
        free(engine);
        return NULL;
    }
    
    return engine;
}

// Geração simulada
void llm_generate(llm_engine_t* engine, const char* prompt) {
    printf("\n🔮 CHUNK Inference Engine v%s\n", CHUNK_VERSION);
    printf("📝 Prompt: %s\n", prompt);
    printf("⚙️  Processando");
    fflush(stdout);
    
    // Simula processamento
    for (int i = 0; i < 5; i++) {
        printf(".");
        fflush(stdout);
        usleep(200000);
    }
    
    // Geração simulada
    printf("\n🤖 Resposta: ");
    const char* dummy_responses[] = {
        "Olá! Eu sou o CHUNK rodando com memória paginada por camadas.",
        "Minha RAM está usando apenas %.1f MB de %d MB.",
        "Taxa de acerto do prefetcher: %.1f%%",
        "Page faults tratados: %llu"
    };
    
    chunk_stats_t stats = nmm_get_stats(engine->nmm);
    
    printf("%s\n", dummy_responses[0]);
    printf(dummy_responses[1], 
           (double)engine->nmm->ram_used_bytes / (1024*1024),
           CHUNK_DEFAULT_RAM_LIMIT_MB);
    printf("\n");
    printf(dummy_responses[2], stats.cache_hit_rate * 100);
    printf("\n");
    printf(dummy_responses[3], stats.total_page_faults);
    printf("\n");
}

int main(int argc, char** argv) {
    const char* model = "llama-3-8b";
    const char* prompt = "Explique o CHUNK OS";
    
    if (argc > 1) model = argv[1];
    if (argc > 2) prompt = argv[2];
    
    printf("╔════════════════════════════════════════════╗\n");
    printf("║     CHUNK OS - Neural Memory Manager      ║\n");
    printf("║   Executando %s com memória paginada    ║\n", model);
    printf("╚════════════════════════════════════════════╝\n\n");
    
    llm_engine_t* engine = llm_init(model);
    if (!engine) return 1;
    
    llm_generate(engine, prompt);
    
    // Mostra estatísticas finais
    chunk_stats_t final_stats = nmm_get_stats(engine->nmm);
    printf("\n📊 Estatísticas finais:\n");
    printf("   Page faults: %llu\n", final_stats.total_page_faults);
    printf("   Cache hit rate: %.1f%%\n", final_stats.cache_hit_rate * 100);
    printf("   RAM usada: %.1f MB / %d MB\n",
           (double)engine->nmm->ram_used_bytes / (1024*1024),
           CHUNK_DEFAULT_RAM_LIMIT_MB);
    
    nmm_shutdown(engine->nmm);
    free(engine);
    
    return 0;
}
