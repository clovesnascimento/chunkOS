#include "libprefetch.h"
#include "../kernel/nmm.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

// Protótipo interno (implementado no nmm.c)
extern void nmm_prefetch_layer(chunk_nmm_context_t* ctx, uint32_t layer);

markov_predictor_t* prefetch_predictor_init(uint32_t order) {
    markov_predictor_t* pred = malloc(sizeof(markov_predictor_t));
    if (!pred) return NULL;
    
    pred->order = order;
    memset(pred->transition_matrix, 0, sizeof(pred->transition_matrix));
    memset(pred->last_states, 0, sizeof(pred->last_states));
    
    return pred;
}

void prefetch_predictor_update(markov_predictor_t* pred,
                               uint32_t from_layer,
                               uint32_t to_layer) {
    pred->transition_matrix[from_layer % 256][to_layer % 256]++;
    
    // Atualiza histórico
    for (int i = pred->order - 1; i > 0; i--) {
        pred->last_states[i] = pred->last_states[i - 1];
    }
    pred->last_states[0] = from_layer;
}

uint32_t* prefetch_predict_next(markov_predictor_t* pred,
                                uint32_t current_layer,
                                uint32_t count) {
    uint32_t* predictions = malloc(count * sizeof(uint32_t));
    if (!predictions) return NULL;
    
    uint32_t current = current_layer;
    
    for (uint32_t i = 0; i < count; i++) {
        uint32_t best_next = current + 1;
        uint32_t max_count = 0;
        
        // Busca próxima camada mais provável
        for (int next = 0; next < 256; next++) {
            uint32_t trans = pred->transition_matrix[current % 256][next];
            if (trans > max_count) {
                max_count = trans;
                best_next = next;
            }
        }
        
        predictions[i] = best_next;
        current = best_next;
    }
    
    return predictions;
}

float prefetch_get_confidence(markov_predictor_t* pred,
                              uint32_t from_layer,
                              uint32_t to_layer) {
    uint32_t total = 0;
    uint32_t target = pred->transition_matrix[from_layer % 256][to_layer % 256];
    
    for (int i = 0; i < 256; i++) {
        total += pred->transition_matrix[from_layer % 256][i];
    }
    
    if (total == 0) return 0.0f;
    return (float)target / total;
}

void prefetch_predictor_free(markov_predictor_t* pred) {
    free(pred);
}

// Thread de prefetch adaptativo
static void* prefetch_adaptive_worker(void* arg) {
    adaptive_prefetcher_t* prefetcher = (adaptive_prefetcher_t*)arg;
    
    while (prefetcher->is_running) {
        chunk_layer_t current = nmm_get_current_layer(prefetcher->nmm_ctx);
        
        // Prediz próximas 3 camadas
        uint32_t* next_layers = prefetch_predict_next(prefetcher->predictor,
                                                       current,
                                                       3);
        
        if (next_layers) {
            for (int i = 0; i < 3; i++) {
                float confidence = prefetch_get_confidence(prefetcher->predictor,
                                                           current + i,
                                                           next_layers[i]);
                
                if (confidence > 0.4f) {
                    // Pré-carrega camada predita (simulado)
                    // Em um sistema real, chamaria a função de prefetch do kernel
                }
            }
            free(next_layers);
        }
        
        usleep(1000); // 1ms polling
    }
    
    return NULL;
}

adaptive_prefetcher_t* prefetch_adaptive_init(chunk_nmm_context_t* ctx) {
    adaptive_prefetcher_t* prefetcher = malloc(sizeof(adaptive_prefetcher_t));
    prefetcher->predictor = prefetch_predictor_init(2);
    prefetcher->nmm_ctx = ctx;
    prefetcher->is_running = 1;
    
    pthread_create(&prefetcher->thread, NULL,
                   prefetch_adaptive_worker, prefetcher);
    
    return prefetcher;
}

void prefetch_adaptive_destroy(adaptive_prefetcher_t* prefetcher) {
    prefetcher->is_running = 0;
    pthread_join(prefetcher->thread, NULL);
    prefetch_predictor_free(prefetcher->predictor);
    free(prefetcher);
}
