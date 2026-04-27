#include "libprefetch.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static uint32_t** markov_table = NULL;
static uint32_t* transition_totals = NULL;
static uint32_t num_layers = 0;
static uint64_t total_preds = 0;
static uint64_t total_hits = 0;

int prefetch_init(uint32_t layers) {
    num_layers = layers;
    markov_table = malloc(layers * sizeof(uint32_t*));
    transition_totals = calloc(layers, sizeof(uint32_t));
    
    for (uint32_t i = 0; i < layers; i++) {
        markov_table[i] = calloc(layers, sizeof(uint32_t));
        // Inicializa com probabilidade linear (camada i -> i+1)
        if (i < layers - 1) {
            markov_table[i][i+1] = 1;
            transition_totals[i] = 1;
        }
    }
    return 0;
}

void prefetch_observe_transition(chunk_layer_t from, chunk_layer_t to) {
    if (from < num_layers && to < num_layers) {
        markov_table[from][to]++;
        transition_totals[from]++;
    }
}

int prefetch_predict(chunk_layer_t current, 
                     chunk_layer_t* predicted, 
                     int count,
                     float* confidence) {
    if (current >= num_layers) return 0;
    
    total_preds++;
    
    int found = 0;
    uint32_t total = transition_totals[current];
    
    if (total == 0) {
        // Fallback: sequência linear
        for (int i = 0; i < count; i++) {
            predicted[i] = (current + 1 + i) % num_layers;
            confidence[i] = 0.5f;
        }
        return count;
    }
    
    // Encontra as 'count' transições mais prováveis
    // Simplificação: pega as próximas na sequência com maior peso
    for (int i = 0; i < count; i++) {
        uint32_t best_next = (current + 1 + i) % num_layers;
        uint32_t max_val = markov_table[current][best_next];
        
        for (uint32_t l = 0; l < num_layers; l++) {
            if (markov_table[current][l] > max_val) {
                max_val = markov_table[current][l];
                best_next = l;
            }
        }
        
        predicted[i] = best_next;
        confidence[i] = (float)max_val / total;
        found++;
    }
    
    return found;
}

double prefetch_get_hit_rate(void) {
    if (total_preds == 0) return 1.0;
    return (double)total_hits / total_preds;
}

int prefetch_shutdown(void) {
    for (uint32_t i = 0; i < num_layers; i++) {
        free(markov_table[i]);
    }
    free(markov_table);
    free(transition_totals);
    return 0;
}
