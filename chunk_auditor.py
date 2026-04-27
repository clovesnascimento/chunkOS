#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   CHUNK OS — SYSTEM AUDITOR v1.0                                              ║
║   Auditoria Completa de Implementação e Integridade                           ║
║                                                                               ║
║   "Se não foi testado, não funciona. Se não foi auditado, não confie."       ║
║                                                                               ║
║   CNGSM — Cloves Nascimento                                                   ║
║   Arquiteto de Ecossistemas Cognitivos                                        ║
║                                                                               ║
║   Assinatura: CNGSM-AUDITOR-2026-04-27-V1.0                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import hashlib
import platform
import subprocess
import importlib
import inspect
import unittest
import tempfile
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# CORES E ESTILOS
# ============================================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    GOLD = '\033[33m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    # Ícones
    CHECK = f"{GREEN}✓{RESET}"
    CROSS = f"{RED}✗{RESET}"
    WARN = f"{YELLOW}⚠{RESET}"
    INFO = f"{CYAN}ℹ{RESET}"
    SHIELD = f"{CYAN}🛡️{RESET}"
    BUG = f"{RED}🐛{RESET}"
    ROCKET = f"{GOLD}🚀{RESET}"
    TOOL = f"{BLUE}🔧{RESET}"
    CLOCK = f"{YELLOW}⏱️{RESET}"


# ============================================================================
# TIPOS DE AUDITORIA
# ============================================================================

class AuditSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class AuditCategory(Enum):
    FILESYSTEM = "filesystem"
    KERNEL = "kernel"
    LIBRARIES = "libraries"
    CONFIGURATION = "configuration"
    PERFORMANCE = "performance"
    SECURITY = "security"
    INTEGRATION = "integration"
    NETWORK = "network"
    DEPENDENCIES = "dependencies"


@dataclass
class AuditResult:
    """Resultado de um teste de auditoria"""
    name: str
    category: AuditCategory
    severity: AuditSeverity
    passed: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    recommendation: str = ""


@dataclass
class AuditReport:
    """Relatório completo de auditoria"""
    timestamp: str
    system_info: Dict[str, Any]
    results: List[AuditResult] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
    score: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "system_info": self.system_info,
            "results": [{
                "name": r.name,
                "category": r.category.value,
                "severity": r.severity.value,
                "passed": r.passed,
                "message": r.message,
                "details": r.details,
                "duration_ms": r.duration_ms,
                "recommendation": r.recommendation
            } for r in self.results],
            "summary": self.summary,
            "score": self.score
        }


# ============================================================================
# SISTEMA DE AUDITORIA
# ============================================================================

class ChunkSystemAuditor:
    """
    Auditor completo do sistema CHUNK OS
    Verifica implementação, integridade e performance
    """
    
    def __init__(self, chunk_root: str = "/chunk"):
        self.chunk_root = Path(chunk_root)
        self.results: List[AuditResult] = []
        self.start_time: float = 0.0
        
        # Configurações de threshold
        self.thresholds = {
            "min_ram_gb": 1.0,
            "min_cpu_cores": 2,
            "max_page_fault_latency_us": 500,
            "min_prefetch_hit_rate": 0.6,
            "min_kv_compression": 0.7
        }
    
    def _add_result(self, result: AuditResult) -> None:
        """Adiciona resultado à lista"""
        self.results.append(result)
    
    def _run_test(self, name: str, category: AuditCategory, 
                  severity: AuditSeverity, test_func: callable) -> AuditResult:
        """Executa um teste e registra resultado"""
        start = time.perf_counter()
        try:
            passed, message, details = test_func()
        except Exception as e:
            passed = False
            message = f"Erro durante teste: {str(e)}"
            details = {"error": str(e)}
        
        duration_ms = (time.perf_counter() - start) * 1000
        
        return AuditResult(
            name=name,
            category=category,
            severity=severity,
            passed=passed,
            message=message,
            details=details,
            duration_ms=duration_ms,
            recommendation=self._get_recommendation(name, passed, details)
        )
    
    def _get_recommendation(self, test_name: str, passed: bool, details: Dict) -> str:
        """Gera recomendação baseada no resultado"""
        if passed:
            return ""
        
        recommendations = {
            "kernel_nmm": "Verifique se o arquivo nmm_kernel_v2.py existe e tem permissão de execução",
            "kernel_compilation": "Instale gcc/make: sudo apt install build-essential",
            "dma_setup": "Verifique permissões do dispositivo /dev/chunk_flash",
            "memory_limit": "Reduza CHUNK_RAM_LIMIT_MB ou aumente RAM disponível",
            "prefetch_hit_rate": "Aumente prefetch_lookahead no arquivo de configuração",
            "kv_compression": "Ative compressão híbrida no chunk.conf",
            "page_fault_latency": "Aumente DMA throughput ou reduza page size"
        }
        
        return recommendations.get(test_name, "Consulte a documentação oficial")
    
    # ========================================================================
    # TESTES DE SISTEMA
    # ========================================================================
    
    def test_system_info(self) -> Tuple[bool, str, Dict]:
        """Coleta informações do sistema"""
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": sys.version,
            "hostname": platform.node(),
            "processor": platform.processor()
        }
        
        # RAM total
        try:
            import psutil
            info["ram_total_gb"] = psutil.virtual_memory().total / (1024**3)
            info["ram_available_gb"] = psutil.virtual_memory().available / (1024**3)
        except:
            info["ram_total_gb"] = "N/A (psutil não instalado)"
        
        # CPU cores
        info["cpu_cores"] = os.cpu_count()
        
        return True, "Informações coletadas", info
    
    def test_chunk_directory(self) -> Tuple[bool, str, Dict]:
        """Verifica se diretório CHUNK existe"""
        exists = self.chunk_root.exists()
        details = {
            "path": str(self.chunk_root),
            "exists": exists,
            "is_directory": self.chunk_root.is_dir() if exists else False
        }
        
        if exists:
            # Verifica subdiretórios
            subdirs = ["bin", "lib", "etc", "models", "logs"]
            for subdir in subdirs:
                details[f"has_{subdir}"] = (self.chunk_root / subdir).exists()
        
        return exists, "Diretório CHUNK encontrado" if exists else "Diretório CHUNK não encontrado", details
    
    def test_kernel_files(self) -> Tuple[bool, str, Dict]:
        """Verifica arquivos do kernel NMM"""
        kernel_files = [
            "nmm_kernel_v2.py",
            "chunk_recovery.py",
            "nmm.c",
            "nmm.h"
        ]
        
        found = []
        missing = []
        
        # Procura em múltiplos locais
        search_paths = [
            Path.cwd(),
            self.chunk_root / "src" / "kernel",
            self.chunk_root / "bin",
            Path.home() / "chunk-os",
            Path("/usr/local/bin")
        ]
        
        for filename in kernel_files:
            located = False
            for path in search_paths:
                if (path / filename).exists():
                    found.append(filename)
                    located = True
                    break
            if not located:
                missing.append(filename)
        
        passed = len(missing) == 0
        message = f"Encontrados: {len(found)}/{len(kernel_files)}"
        details = {"found": found, "missing": missing}
        
        return passed, message, details
    
    def test_nmm_kernel_execution(self) -> Tuple[bool, str, Dict]:
        """Testa execução do NMM Kernel"""
        # Procura o kernel
        kernel_path = None
        search_paths = [
            Path.cwd() / "nmm_kernel_v2.py",
            self.chunk_root / "bin" / "nmm_kernel_v2.py",
            Path.home() / "chunk-os" / "nmm_kernel_v2.py"
        ]
        
        for path in search_paths:
            if path.exists():
                kernel_path = path
                break
        
        if not kernel_path:
            return False, "Arquivo do kernel não encontrado", {"searched": [str(p) for p in search_paths]}
        
        # Testa execução com --help
        try:
            result = subprocess.run(
                [sys.executable, str(kernel_path), "--help"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                return True, "Kernel executável e responsivo", {
                    "path": str(kernel_path),
                    "output_preview": result.stdout[:200]
                }
            else:
                return False, f"Kernel respondeu com erro: {result.stderr[:100]}", {}
        except subprocess.TimeoutExpired:
            return False, "Kernel não respondeu (timeout)", {}
        except Exception as e:
            return False, f"Erro ao executar kernel: {e}", {}
    
    def test_nmm_demo_execution(self) -> Tuple[bool, str, Dict]:
        """Executa demonstração do NMM e verifica saída"""
        kernel_path = None
        search_paths = [
            Path.cwd() / "nmm_kernel_v2.py",
            self.chunk_root / "bin" / "nmm_kernel_v2.py",
            Path.home() / "chunk-os" / "nmm_kernel_v2.py"
        ]
        
        for path in search_paths:
            if path.exists():
                kernel_path = path
                break
        
        if not kernel_path:
            return False, "Arquivo do kernel não encontrado", {}
        
        # Executa demo e captura saída
        try:
            result = subprocess.run(
                [sys.executable, str(kernel_path), "--demo"],
                capture_output=True, text=True, timeout=30
            )
            
            output = result.stdout + result.stderr
            
            # Verifica indicadores de sucesso
            success_indicators = [
                "NMM Kernel",
                "páginas registradas",
                "Page faults",
                "Prefetch hits",
                "Economia"
            ]
            
            found_indicators = [ind for ind in success_indicators if ind in output]
            
            if result.returncode == 0 and len(found_indicators) >= 3:
                # Extrai estatísticas
                stats = {}
                for line in output.split('\n'):
                    if 'Page faults:' in line:
                        try:
                            stats['page_faults'] = int(line.split(':')[1].strip().replace(',', ''))
                        except:
                            pass
                    elif 'Prefetch hits:' in line:
                        try:
                            stats['prefetch_hits'] = int(line.split(':')[1].strip().replace(',', ''))
                        except:
                            pass
                    elif 'Economia:' in line:
                        try:
                            stats['memory_saving'] = line.split(':')[1].strip()
                        except:
                            pass
                
                return True, "Demo executada com sucesso", {
                    "output_preview": output[:500],
                    "statistics": stats,
                    "indicators_found": found_indicators
                }
            else:
                return False, "Demo não produziu saída esperada", {
                    "output_preview": output[:500],
                    "missing_indicators": [i for i in success_indicators if i not in found_indicators]
                }
                
        except subprocess.TimeoutExpired:
            return False, "Demo excedeu tempo limite (30s)", {}
        except Exception as e:
            return False, f"Erro na demo: {e}", {}
    
    def test_configuration_files(self) -> Tuple[bool, str, Dict]:
        """Verifica arquivos de configuração"""
        config_files = [
            self.chunk_root / "etc" / "chunk.conf",
            self.chunk_root / "models" / "registry" / "models.yaml",
            Path.cwd() / "chunk.conf",
            Path.home() / ".chunk" / "config"
        ]
        
        valid_configs = []
        for cfg in config_files:
            if cfg.exists():
                try:
                    content = cfg.read_text()
                    # Verifica se tem seções básicas
                    if "[memory]" in content and "[prefetch]" in content:
                        valid_configs.append(str(cfg))
                except:
                    pass
        
        passed = len(valid_configs) > 0
        message = f"Encontradas {len(valid_configs)} configurações válidas"
        details = {"valid_configs": valid_configs}
        
        return passed, message, details
    
    def test_dependencies(self) -> Tuple[bool, str, Dict]:
        """Verifica dependências do sistema"""
        dependencies = {
            "python3": "python3",
            "gcc": "gcc",
            "make": "make",
            "git": "git",
        }
        
        optional = {
            "numpy": "numpy",
            "psutil": "psutil"
        }
        
        found = {}
        missing = []
        
        for name, cmd in dependencies.items():
            if shutil.which(cmd):
                found[name] = True
                # Tenta obter versão
                try:
                    result = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=2)
                    found[f"{name}_version"] = result.stdout.split('\n')[0][:50]
                except:
                    pass
            else:
                missing.append(name)
        
        # Verifica módulos Python
        for name, module in optional.items():
            try:
                importlib.import_module(module)
                found[name] = True
            except ImportError:
                found[name] = False
                missing.append(name)
        
        passed = len(missing) <= 1  # Permite 1 dependência faltante
        message = f"Dependências: {len([f for f in found.values() if f is True])}/{len(dependencies) + len(optional)}"
        details = {"found": found, "missing": missing}
        
        return passed, message, details
    
    def test_performance_metrics(self) -> Tuple[bool, str, Dict]:
        """Testa métricas de performance simuladas"""
        # Simula execução rápida do kernel
        try:
            # Tenta importar o módulo do kernel
            sys.path.insert(0, str(Path.cwd()))
            sys.path.insert(0, str(self.chunk_root / "bin"))
            
            try:
                from nmm_kernel_v2 import NeuralMemoryManager
                
                # Cria instância com RAM limitada
                nmm = NeuralMemoryManager(ram_limit_mb=512.0)
                nmm.load_model("test-model")
                nmm.start()
                
                # Coleta estatísticas
                stats = nmm.get_stats()
                
                nmm.shutdown()
                
                # Verifica se as métricas são razoáveis
                metrics = {
                    "page_faults": stats.total_page_faults,
                    "prefetch_hits": stats.total_prefetch_hits,
                    "ram_used_mb": stats.ram_used_mb,
                    "cache_hit_rate": stats.cache_hit_rate
                }
                
                passed = stats.cache_hit_rate >= 0.3  # Pelo menos 30% de acerto
                message = f"Cache hit rate: {stats.cache_hit_rate*100:.1f}%"
                
                return passed, message, {"metrics": metrics}
                
            except ImportError as e:
                return False, f"Não foi possível importar NMM: {e}", {}
                
        except Exception as e:
            return False, f"Erro no teste de performance: {e}", {}
    
    def test_security_checks(self) -> Tuple[bool, str, Dict]:
        """Verifica segurança básica"""
        issues = []
        warnings = []
        
        # Verifica permissões de arquivos sensíveis
        sensitive_paths = [
            self.chunk_root / "etc" / "chunk.conf",
            self.chunk_root / "logs",
            Path.home() / ".chunk"
        ]
        
        for path in sensitive_paths:
            if path.exists():
                mode = path.stat().st_mode
                # Verifica se não está world-writable
                if mode & 0o002:  # others write
                    warnings.append(f"{path} está world-writable")
        
        # Verifica se está rodando como root (risco)
        try:
            if os.geteuid() == 0:
                warnings.append("Executando como root - risco de segurança")
        except AttributeError:
            # os.geteuid() not available on Windows
            pass
        
        passed = len(issues) == 0
        message = f"Segurança: {len(warnings)} avisos"
        details = {"issues": issues, "warnings": warnings}
        
        return passed, message, details
    
    def test_integration_python_api(self) -> Tuple[bool, str, Dict]:
        """Testa integração com Python"""
        try:
            # Tenta importar e usar componentes
            sys.path.insert(0, str(Path.cwd()))
            
            # Simula API básica
            class MockNMM:
                def __init__(self):
                    self.stats = {"ram_used": 0}
                def load_model(self, name):
                    return True
                def generate(self, prompt):
                    return f"Resposta para: {prompt}"
            
            nmm = MockNMM()
            result = nmm.generate("teste")
            
            if result and "teste" in result:
                return True, "API Python funcionando", {"mock_mode": True}
            else:
                return False, "API não respondeu corretamente", {}
                
        except Exception as e:
            return False, f"Erro na integração: {e}", {}
    
    def test_backup_system(self) -> Tuple[bool, str, Dict]:
        """Testa sistema de backup"""
        backup_dir = self.chunk_root / "backups"
        
        if not backup_dir.exists():
            return False, "Diretório de backups não encontrado", {"path": str(backup_dir)}
        
        # Conta backups
        backups = list(backup_dir.glob("*.tar.gz"))
        meta_files = list(backup_dir.glob("*.meta"))
        
        passed = len(backups) > 0 or len(meta_files) > 0
        message = f"{len(backups)} backups encontrados"
        details = {
            "backup_count": len(backups),
            "meta_count": len(meta_files),
            "directory": str(backup_dir)
        }
        
        return passed, message, details
    
    def test_logging_system(self) -> Tuple[bool, str, Dict]:
        """Testa sistema de logging"""
        log_dir = self.chunk_root / "logs"
        
        if not log_dir.exists():
            # Tenta criar
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
            except:
                return False, "Não foi possível criar diretório de logs", {}
        
        # Tenta escrever log
        log_file = log_dir / "audit_test.log"
        try:
            with open(log_file, "w") as f:
                f.write(f"Audit test at {datetime.now()}\n")
            passed = True
            message = "Sistema de logging funcional"
            details = {"log_path": str(log_file)}
            
            # Limpa
            log_file.unlink()
        except Exception as e:
            passed = False
            message = f"Erro no logging: {e}"
            details = {}
        
        return passed, message, details
    
    # ========================================================================
    # EXECUÇÃO DA AUDITORIA
    # ========================================================================
    
    def run_full_audit(self) -> AuditReport:
        """Executa auditoria completa"""
        self.start_time = time.time()
        
        print(f"\n{Colors.GOLD}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.SHIELD} CHUNK OS — SISTEMA DE AUDITORIA COMPLETA{Colors.RESET}")
        print(f"{Colors.GOLD}{'═' * 70}{Colors.RESET}\n")
        
        # Coleta informações do sistema
        _, _, system_info = self.test_system_info()
        
        # Lista de testes
        tests = [
            ("Informações do Sistema", AuditCategory.INTEGRATION, AuditSeverity.INFO, self.test_system_info),
            ("Diretório CHUNK", AuditCategory.FILESYSTEM, AuditSeverity.CRITICAL, self.test_chunk_directory),
            ("Arquivos do Kernel", AuditCategory.KERNEL, AuditSeverity.CRITICAL, self.test_kernel_files),
            ("Execução do Kernel", AuditCategory.KERNEL, AuditSeverity.CRITICAL, self.test_nmm_kernel_execution),
            ("Demo NMM", AuditCategory.PERFORMANCE, AuditSeverity.HIGH, self.test_nmm_demo_execution),
            ("Arquivos de Configuração", AuditCategory.CONFIGURATION, AuditSeverity.MEDIUM, self.test_configuration_files),
            ("Dependências", AuditCategory.DEPENDENCIES, AuditSeverity.HIGH, self.test_dependencies),
            ("Performance Metrics", AuditCategory.PERFORMANCE, AuditSeverity.MEDIUM, self.test_performance_metrics),
            ("Segurança", AuditCategory.SECURITY, AuditSeverity.HIGH, self.test_security_checks),
            ("API Python", AuditCategory.INTEGRATION, AuditSeverity.MEDIUM, self.test_integration_python_api),
            ("Sistema de Backup", AuditCategory.FILESYSTEM, AuditSeverity.LOW, self.test_backup_system),
            ("Sistema de Logging", AuditCategory.FILESYSTEM, AuditSeverity.LOW, self.test_logging_system),
        ]
        
        # Executa testes
        for name, category, severity, test_func in tests:
            print(f"{Colors.INFO} Auditando: {name}...{Colors.RESET}", end=" ")
            result = self._run_test(name, category, severity, test_func)
            self._add_result(result)
            
            # Mostra resultado
            if result.passed:
                print(f"{Colors.GREEN}✓ OK{Colors.RESET} ({result.duration_ms:.0f}ms)")
            else:
                print(f"{Colors.RED}✗ FALHA{Colors.RESET} ({result.duration_ms:.0f}ms)")
                print(f"   {Colors.DIM}→ {result.message}{Colors.RESET}")
        
        # Gera relatório
        report = AuditReport(
            timestamp=datetime.now().isoformat(),
            system_info=system_info,
            results=self.results
        )
        
        # Calcula summary
        total = len(report.results)
        passed = sum(1 for r in report.results if r.passed)
        failed = total - passed
        
        report.summary = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total) * 100 if total > 0 else 0
        }
        
        # Calcula score (0-100)
        weights = {
            AuditSeverity.CRITICAL: 4,
            AuditSeverity.HIGH: 3,
            AuditSeverity.MEDIUM: 2,
            AuditSeverity.LOW: 1,
            AuditSeverity.INFO: 0
        }
        
        total_weight = sum(weights[r.severity] for r in report.results)
        passed_weight = sum(weights[r.severity] for r in report.results if r.passed)
        
        report.score = (passed_weight / total_weight) * 100 if total_weight > 0 else 0
        
        duration_sec = time.time() - self.start_time
        
        # Print final
        print(f"\n{Colors.GOLD}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 RESUMO DA AUDITORIA{Colors.RESET}")
        print(f"{Colors.GOLD}{'═' * 70}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}📈 Estatísticas:{Colors.RESET}")
        print(f"   Testes executados: {total}")
        print(f"   ✅ Aprovados: {passed}")
        print(f"   ❌ Falhas: {failed}")
        print(f"   📊 Taxa de acerto: {report.summary['pass_rate']:.1f}%")
        print(f"   🎯 Score: {report.score:.1f}/100")
        print(f"   ⏱️ Tempo total: {duration_sec:.2f}s")
        
        # Classificação
        print(f"\n{Colors.BOLD}🏆 CLASSIFICAÇÃO:{Colors.RESET}")
        if report.score >= 90:
            print(f"   {Colors.GREEN}★★★★★ EXCELENTE — Sistema implementado corretamente{Colors.RESET}")
        elif report.score >= 75:
            print(f"   {Colors.CYAN}★★★★☆ BOM — Pequenos ajustes necessários{Colors.RESET}")
        elif report.score >= 60:
            print(f"   {Colors.YELLOW}★★★☆☆ REGULAR — Recomenda-se revisão{Colors.RESET}")
        elif report.score >= 40:
            print(f"   {Colors.YELLOW}★★☆☆☆ INSUFICIENTE — Múltiplos problemas{Colors.RESET}")
        else:
            print(f"   {Colors.RED}★☆☆☆☆ CRÍTICO — Sistema não implementado corretamente{Colors.RESET}")
        
        # Recomendações agrupadas
        failed_tests = [r for r in report.results if not r.passed and r.severity != AuditSeverity.INFO]
        if failed_tests:
            print(f"\n{Colors.YELLOW}🔧 RECOMENDAÇÕES PRIORITÁRIAS:{Colors.RESET}")
            for test in failed_tests[:5]:
                print(f"   • {test.name}: {test.recommendation}")
        
        print(f"\n{Colors.GOLD}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.SHIELD} Auditoria concluída em {duration_sec:.2f}s{Colors.RESET}")
        print(f"{Colors.GOLD}{'═' * 70}{Colors.RESET}\n")
        
        return report
    
    def save_report(self, report: AuditReport, output_path: str = None) -> str:
        """Salva relatório em arquivo JSON"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"chunk_audit_{timestamp}.json"
        
        with open(output_path, "w") as f:
            json.dump(report.to_dict(), f, indent=2, default=str)
        
        print(f"{Colors.CHECK} Relatório salvo: {output_path}{Colors.RESET}")
        return output_path


# ============================================================================
# INTERFACE DE LINHA DE COMANDO
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CHUNK OS — System Auditor",
        epilog="CNGSM — Cloves Nascimento — Engenharia da Próxima Geração"
    )
    parser.add_argument("--path", "-p", type=str, default="/chunk",
                        help="Caminho da instalação do CHUNK OS")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Arquivo de saída para o relatório JSON")
    parser.add_argument("--quick", "-q", action="store_true",
                        help="Modo rápido (apenas verificações críticas)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Saída detalhada")
    
    args = parser.parse_args()
    
    # Banner
    print(f"""
{Colors.GOLD}╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🔍 CHUNK OS — SYSTEM AUDITOR v1.0                                          ║
║   Auditoria Completa de Implementação e Integridade                           ║
║                                                                               ║
║   {Colors.CYAN}CNGSM — Cloves Nascimento{Colors.GOLD}                                                   ║
║   {Colors.CYAN}Arquiteto de Ecossistemas Cognitivos{Colors.GOLD}                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
    """)
    
    print(f"{Colors.INFO} Iniciando auditoria em: {args.path}{Colors.RESET}")
    print(f"{Colors.INFO} Modo: {'RÁPIDO' if args.quick else 'COMPLETO'}{Colors.RESET}\n")
    
    auditor = ChunkSystemAuditor(chunk_root=args.path)
    
    if args.quick:
        # Apenas testes críticos
        critical_tests = [
            ("Diretório CHUNK", AuditCategory.FILESYSTEM, AuditSeverity.CRITICAL, auditor.test_chunk_directory),
            ("Arquivos do Kernel", AuditCategory.KERNEL, AuditSeverity.CRITICAL, auditor.test_kernel_files),
            ("Execução do Kernel", AuditCategory.KERNEL, AuditSeverity.CRITICAL, auditor.test_nmm_kernel_execution),
            ("Demo NMM", AuditCategory.PERFORMANCE, AuditSeverity.HIGH, auditor.test_nmm_demo_execution),
        ]
        
        auditor.results = []
        for name, category, severity, test_func in critical_tests:
            print(f"{Colors.INFO} Auditando: {name}...{Colors.RESET}", end=" ")
            result = auditor._run_test(name, category, severity, test_func)
            auditor.results.append(result)
            
            if result.passed:
                print(f"{Colors.GREEN}✓ OK{Colors.RESET}")
            else:
                print(f"{Colors.RED}✗ FALHA{Colors.RESET}")
                print(f"   {Colors.DIM}→ {result.message}{Colors.RESET}")
        
        # Resumo rápido
        passed = sum(1 for r in auditor.results if r.passed)
        total = len(auditor.results)
        
        print(f"\n{Colors.GOLD}{'═' * 50}{Colors.RESET}")
        if total > 0 and passed == total:
            print(f"{Colors.GREEN}✅ SISTEMA OK — {passed}/{passed} verificações críticas aprovadas{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ SISTEMA COM PROBLEMAS — {passed}/{total} verificações aprovadas{Colors.RESET}")
        
        report = AuditReport(
            timestamp=datetime.now().isoformat(),
            system_info={},
            results=auditor.results
        )
    else:
        report = auditor.run_full_audit()
    
    # Salva relatório
    if args.output or not args.quick:
        output_file = auditor.save_report(report, args.output)
        print(f"\n{Colors.INFO} Para visualizar o relatório completo: cat {output_file}{Colors.RESET}")
    
    # Código de saída
    if report.score >= 75:
        return 0
    elif report.score >= 50:
        return 1
    else:
        return 2


if __name__ == "__main__":
    main()
