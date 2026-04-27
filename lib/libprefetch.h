#ifndef LIBPREFETCH_H
#define LIBPREFETCH_H

#include "../include/chunk_types.h"

// API de Prefetch Preditivo
int prefetch_init(uint32_t max_layers);
int prefetch_shutdown(void);

// Registra transição observada
void prefetch_observe_transition(chunk_layer_t from, chunk_layer_t to);

// Prediz próximas camadas
int prefetch_predict(chunk_layer_t current, 
                     chunk_layer_t* predicted, 
                     int count,
                     float* confidence);

// Ajusta hiperparâmetros
void prefetch_set_lookahead(int layers);
void prefetch_set_threshold(float confidence);

// Estatísticas de acerto
double prefetch_get_hit_rate(void);
uint64_t prefetch_get_total_predictions(void);

#endif
