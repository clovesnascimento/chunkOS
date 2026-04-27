#ifndef LIBPREFETCH_H
#define LIBPREFETCH_H

#include "../include/chunk_types.h"
#include <pthread.h>

// Estrutura de preditor Markov
typedef struct {
    uint32_t transition_matrix[256][256];
    uint32_t order;
    uint32_t last_states[4];
} markov_predictor_t;

// Inicializa preditor
markov_predictor_t* prefetch_predictor_init(uint32_t order);

// Atualiza preditor com transição observada
void prefetch_predictor_update(markov_predictor_t* pred,
                               uint32_t from_layer,
                               uint32_t to_layer);

// Prediz próximas N camadas
uint32_t* prefetch_predict_next(markov_predictor_t* pred,
                                uint32_t current_layer,
                                uint32_t count);

// Calcula confiança da predição
float prefetch_get_confidence(markov_predictor_t* pred,
                              uint32_t from_layer,
                              uint32_t to_layer);

// Libera preditor
void prefetch_predictor_free(markov_predictor_t* pred);

// API de prefetch adaptativo
typedef struct {
    markov_predictor_t* predictor;
    chunk_nmm_context_t* nmm_ctx;
    int is_running;
    pthread_t thread;
} adaptive_prefetcher_t;

adaptive_prefetcher_t* prefetch_adaptive_init(chunk_nmm_context_t* ctx);
void prefetch_adaptive_destroy(adaptive_prefetcher_t* prefetcher);

#endif
