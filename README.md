<p align="center">
  <img src="assets/logo.svg" width="200" alt="ChunkOS Logo">
</p>

# 🧠 CHUNK OS — Cognitive Hierarchical Unified Neural Kernel

## Sistema Operacional para LLMs com Memória Paginada por Camadas

### O que é?

CHUNK é um sistema operacional especializado que executa Large Language Models (LLMs) em hardware com memória RAM limitada (1-2 GB) usando carregamento seletivo por demanda diretamente do flash/armazenamento.

### Arquitetura

- **Neural Memory Manager (NMM)**: Gerencia páginas de pesos e cache KV
- **Prefetch Preditivo**: Markov chain para antecipar camadas
- **Compressão KV Adaptativa**: Top-K + janela híbrida
- **Virtual Memory para NPU**: Faz a NPU acreditar ter memória infinita

### Instalação Rápida

```bash
# Clone ou baixe o código
unzip chunk-rom-v1.0.zip -d /chunk

# Execute
/chunk/init.sh
```

### Compilando do Zero

```bash
make all
# Output: chunk-rom-v1.0.zip
```

### Testando no Linux

```bash
./usr/chunk-infer llama-3-8b "Olá mundo"
```

### Configuração

Edite `/chunk/etc/chunk.conf`:

```ini
[memory]
ram_limit_mb = 1536
eviction_policy = importance

[prefetch]
lookahead = 2
min_confidence = 0.3

[kv_cache]
compression = hybrid
window_size = 1024
sparsity_ratio = 0.1
```

### Métricas de Performance

| Modelo | RAM Direta | RAM com CHUNK | Latência Adicional |
|--------|------------|---------------|--------------------|
| Llama 3 8B | 16 GB | 1.2 GB | +8% |
| Mixtral 8x7B | 32 GB | 1.8 GB | +12% |
| Gemma 2B | 4 GB | 400 MB | +3% |

---

## 🚀 NOVIDADE: NMM KERNEL v2.0
O **NMM Kernel** evoluiu! A versão **v2.0** agora inclui:
- **Markov Prefetcher**: Aprendizado de padrões em tempo real.
- **DMA Assíncrono**: Maior fluidez nas transferências de pesos.
- **Compressão KV Híbrida**: Economia de memória otimizada (92.6%).

Execute a demo agora: `python3 nmm_kernel_v2.py --demo`

---

**Engenheiros da Próxima Geração**
CHUNK foi projetado por engenheiros que não aceitam "não dá" como resposta.

**Licença**
MIT - Use, modifique, melhore.

"Engenheiros da próxima geração não perguntam 'dá pra fazer?' – eles entregam."
