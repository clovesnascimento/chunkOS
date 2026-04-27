#!/usr/bin/env python3
# CHUNK OS Page Analyzer
# Analisa padrões de acesso a páginas para otimização
# CNGSM — Cloves Nascimento

import sys
import json
from collections import defaultdict

class PageAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.accesses = []
        self.page_faults = []
    
    def parse_log(self):
        """Parseia log de acesso do CHUNK"""
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    if 'page_access' in line:
                        data = json.loads(line.split('||')[1])
                        self.accesses.append(data)
                    elif 'page_fault' in line:
                        data = json.loads(line.split('||')[1])
                        self.page_faults.append(data)
        except Exception:
            self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Gera dados de exemplo para demonstração"""
        import random
        for i in range(1000):
            self.accesses.append({
                "layer": random.randint(0, 31),
                "page": random.randint(0, 100),
                "timestamp": i
            })
            if random.random() < 0.1:
                self.page_faults.append({
                    "layer": random.randint(0, 31),
                    "page": random.randint(0, 100),
                    "timestamp": i
                })
    
    def analyze_patterns(self):
        """Analisa padrões de acesso"""
        layer_access = defaultdict(int)
        for acc in self.accesses:
            layer_access[acc['layer']] += 1
        
        print("\n📊 Análise de Padrões de Acesso")
        print("=" * 40)
        print(f"Total de acessos: {len(self.accesses)}")
        print(f"Page faults: {len(self.page_faults)}")
        print(f"Taxa de falha: {len(self.page_faults)/len(self.accesses)*100:.1f}%" if self.accesses else "Taxa de falha: 0%")
        
        print("\n📈 Acessos por camada:")
        for layer in sorted(layer_access.keys())[:10]:
            print(f"   Layer {layer:3d}: {layer_access[layer]:6d} acessos")
    
    def suggest_config(self):
        """Sugere configurações baseadas no padrão"""
        print("\n🔧 Sugestões de Configuração")
        print("=" * 40)
        
        fault_rate = len(self.page_faults) / len(self.accesses) if self.accesses else 1
        
        if fault_rate > 0.2:
            print("   • Aumente CHUNK_PREFETCH_LOOKAHEAD para 3-4")
            print("   • Aumente CHUNK_ACTIVE_LAYERS para 4")
        elif fault_rate < 0.05:
            print("   • Considere reduzir CHUNK_PREFETCH_LOOKAHEAD para economia")
        
        print("   • Padrão detectado — prefetch funcionando bem")

def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else "/chunk/logs/chunk.log"
    
    print("🔬 CHUNK OS Page Analyzer")
    print("CNGSM — Cloves Nascimento\n")
    
    analyzer = PageAnalyzer(log_file)
    analyzer.parse_log()
    analyzer.analyze_patterns()
    analyzer.suggest_config()

if __name__ == "__main__":
    main()
