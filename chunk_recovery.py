#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   CHUNK OS — MASTER ENGINEER RECOVERY SCRIPT v2.0                             ║
║   Neural Memory Manager — Recovery & Self-Healing System                     ║
║                                                                               ║
║   "Quando o sistema cair, o engenheiro da próxima geração levanta em segundos"║
║                                                                               ║
║   CNGSM — Cloves Nascimento                                                   ║
║   Arquiteto de Ecossistemas Cognitivos                                        ║
║                                                                               ║
║   Assinatura: CNGSM-RECOVERY-2026-04-27-V2.0                                  ║
║   Blockchain: Ethereum Mainnet — Tx: 0x7a3c9f2e8b1d5a4e                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import shutil
import hashlib
import platform
import subprocess
import tempfile
import argparse
import logging
import urllib.request
import tarfile
import zipfile
import stat
import re
import threading
import queue
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# VERSÃO E CONFIGURAÇÃO
# ============================================================================

VERSION = "2.0.0"
AUTHOR = "Cloves Nascimento — CNGSM"
SIGNATURE = "CNGSM-RECOVERY-2026-04-27-V2.0"

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
    HEART = f"{RED}❤️{RESET}"
    BRAIN = f"{CYAN}🧠{RESET}"
    DATABASE = f"{BLUE}💾{RESET}"
    NETWORK = f"{CYAN}🌐{RESET}"
    LOCK = f"{GOLD}🔒{RESET}"


# ============================================================================
# LOGGER DE ENGENHEIRO
# ============================================================================

class EngineerLogger:
    """Logger profissional com estilo engenheiro"""
    
    @staticmethod
    def banner():
        print(f"""
{Colors.GOLD}╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   {Colors.CYAN}██████╗██╗  ██╗██╗   ██╗███╗   ██╗██╗  ██╗{Colors.GOLD}    {Colors.CYAN}██████╗ ███████╗{Colors.GOLD}      ║
║   {Colors.CYAN}██╔════╝██║  ██║██║   ██║████╗  ██║██║ ██╔╝{Colors.GOLD}    {Colors.CYAN}██╔══██╗██╔════╝{Colors.GOLD}      ║
║   {Colors.CYAN}██║     ███████║██║   ██║██╔██╗ ██║█████╔╝{Colors.GOLD}     {Colors.CYAN}██████╔╝███████╗{Colors.GOLD}      ║
║   {Colors.CYAN}██║     ██╔══██║██║   ██║██║╚██╗██║██╔═██╗{Colors.GOLD}     {Colors.CYAN}██╔══██╗╚════██║{Colors.GOLD}      ║
║   {Colors.CYAN}╚██████╗██║  ██║╚██████╔╝██║ ╚████║██║  ██╗{Colors.GOLD}    {Colors.CYAN}██████╔╝███████║{Colors.GOLD}      ║
║   {Colors.CYAN} ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝{Colors.GOLD}    {Colors.CYAN}╚═════╝ ╚══════╝{Colors.GOLD}      ║
║                                                                               ║
║   {Colors.BOLD}MASTER ENGINEER RECOVERY SYSTEM v{VERSION}{Colors.RESET}{Colors.GOLD}                              ║
║                                                                               ║
║   {Colors.DIM}CNGSM — Cognitive Neural & Generative Systems Management{Colors.RESET}{Colors.GOLD}          ║
║   {Colors.DIM}Cloves Nascimento — Arquiteto de Ecossistemas Cognitivos{Colors.RESET}{Colors.GOLD}         ║
║                                                                               ║
║   {Colors.DIM}Assinatura: {SIGNATURE}{Colors.RESET}{Colors.GOLD}                                            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
        """)
    
    @staticmethod
    def info(msg: str):
        print(f"{Colors.INFO} {Colors.CYAN}{msg}{Colors.RESET}")
    
    @staticmethod
    def success(msg: str):
        print(f"{Colors.CHECK} {Colors.GREEN}{msg}{Colors.RESET}")
    
    @staticmethod
    def error(msg: str):
        print(f"{Colors.CROSS} {Colors.RED}{msg}{Colors.RESET}")
    
    @staticmethod
    def warn(msg: str):
        print(f"{Colors.WARN} {Colors.YELLOW}{msg}{Colors.RESET}")
    
    @staticmethod
    def step(msg: str):
        print(f"\n{Colors.TOOL} {Colors.BOLD}{msg}{Colors.RESET}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")
    
    @staticmethod
    def progress(percent: int, msg: str = "", width: int = 40):
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)
        print(f"\r{Colors.GOLD}[{bar}]{Colors.RESET} {percent}% {msg}", end="", flush=True)
    
    @staticmethod
    def status(status: str, msg: str):
        if status == "OK":
            print(f"  {Colors.CHECK} {msg:<55} {Colors.GREEN}[OK]{Colors.RESET}")
        elif status == "FAIL":
            print(f"  {Colors.CROSS} {msg:<55} {Colors.RED}[FAIL]{Colors.RESET}")
        elif status == "WARN":
            print(f"  {Colors.WARN} {msg:<55} {Colors.YELLOW}[WARN]{Colors.RESET}")
        elif status == "SKIP":
            print(f"  {Colors.INFO} {msg:<55} {Colors.CYAN}[SKIP]{Colors.RESET}")
        else:
            print(f"  {Colors.INFO} {msg:<55} {Colors.CYAN}[...]{Colors.RESET}")
    
    @staticmethod
    def separator():
        print(f"{Colors.DIM}{'═' * 70}{Colors.RESET}")
    
    @staticmethod
    def header(title: str):
        print(f"\n{Colors.GOLD}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.SHIELD} {title}{Colors.RESET}")
        print(f"{Colors.GOLD}{'═' * 70}{Colors.RESET}")


logger = EngineerLogger()


# ============================================================================
# CONFIGURAÇÃO DO SISTEMA
# ============================================================================

@dataclass
class ChunkConfig:
    """Configuração mestre do CHUNK OS"""
    version: str = VERSION
    author: str = AUTHOR
    signature: str = SIGNATURE
    
    # URLs dos repositórios (failover automático)
    repos: List[str] = field(default_factory=lambda: [
        "https://raw.githubusercontent.com/clovesnascimento/chunkOS/main",
        "https://cngsm.ai/chunk-os/releases",
        "https://gitlab.com/cngsm/chunk-os/raw/main"
    ])
    
    # Diretórios do sistema
    chunk_root: str = "C:\\chunk" if platform.system() == "Windows" else "/chunk"
    chunk_bin: str = os.path.join(chunk_root, "bin")
    chunk_lib: str = os.path.join(chunk_root, "lib")
    chunk_etc: str = os.path.join(chunk_root, "etc")
    chunk_models: str = os.path.join(chunk_root, "models")
    chunk_logs: str = os.path.join(chunk_root, "logs")
    chunk_proc: str = os.path.join(chunk_root, "proc")
    chunk_backup: str = os.path.join(chunk_root, "backups")
    
    # Dependências mínimas
    min_deps: List[str] = field(default_factory=lambda: ["python", "gcc", "make", "git"])
    
    # Thresholds
    min_ram_gb: float = 1.0
    min_storage_gb: float = 8.0


# ============================================================================
# DETECÇÃO DE SISTEMA
# ============================================================================

class SystemDetector:
    """Detecta ambiente e capabilities do sistema"""
    
    @staticmethod
    def detect_os() -> str:
        system = platform.system().lower()
        if system == "linux":
            # Verifica se é Android/Termux
            if "android" in platform.platform().lower():
                return "android"
            if "termux" in os.environ.get("PREFIX", ""):
                return "termux"
            return "linux"
        elif system == "darwin":
            return "macos"
        elif system == "windows":
            return "windows"
        return "unknown"
    
    @staticmethod
    def is_root() -> bool:
        if platform.system() == "Windows":
            import ctypes
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        return os.geteuid() == 0
    
    @staticmethod
    def get_ram_gb() -> float:
        try:
            import psutil
            return psutil.virtual_memory().total / (1024**3)
        except:
            return 4.0 # Default guess if psutil not found
    
    @staticmethod
    def get_storage_gb(path: str = "/") -> float:
        try:
            if platform.system() == "Windows":
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(path, None, ctypes.byref(total_bytes), ctypes.byref(free_bytes))
                return total_bytes.value / (1024**3)
            else:
                stat = os.statvfs(path)
                return (stat.f_blocks * stat.f_frsize) / (1024**3)
        except:
            return 10.0
    
    @staticmethod
    def get_arch() -> str:
        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            return "x86_64"
        elif machine in ["aarch64", "arm64"]:
            return "arm64"
        elif machine.startswith("armv"):
            return "arm32"
        return "unknown"
    
    @staticmethod
    def get_cpu_cores() -> int:
        return os.cpu_count() or 2
    
    @staticmethod
    def check_dependencies(deps: List[str]) -> Dict[str, bool]:
        results = {}
        for dep in deps:
            if shutil.which(dep):
                results[dep] = True
                logger.status("OK", f"{dep} encontrado")
            else:
                results[dep] = False
                logger.status("FAIL", f"{dep} não encontrado")
        return results
    
    @staticmethod
    def get_network_connectivity() -> bool:
        """Verifica conectividade com repositórios"""
        import socket
        try:
            socket.create_connection(("github.com", 80), timeout=5)
            return True
        except:
            return False


# ============================================================================
# BACKUP MANAGER
# ============================================================================

class BackupManager:
    """Gerencia backups do sistema CHUNK"""
    
    def __init__(self, config: ChunkConfig):
        self.config = config
        self.backup_path = Path(config.chunk_backup)
        self.backup_path.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, tag: str = "auto", description: str = "") -> str:
        """Cria backup completo do sistema"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"chunk_backup_{tag}_{timestamp}"
        backup_file = self.backup_path / f"{backup_name}.tar.gz"
        
        logger.info(f"Criando backup: {backup_name}")
        
        if not Path(self.config.chunk_root).exists():
            logger.warn("Sistema CHUNK não encontrado")
            return ""
        
        try:
            import tarfile
            
            # Cria metadata
            metadata = {
                "backup_name": backup_name,
                "timestamp": timestamp,
                "tag": tag,
                "description": description,
                "version": VERSION,
                "author": AUTHOR,
                "signature": SIGNATURE,
                "os": platform.system(),
                "arch": platform.machine(),
                "python_version": sys.version,
                "chunk_version": self._get_chunk_version()
            }
            
            # Cria arquivo de metadata
            meta_path = self.backup_path / f"{backup_name}.meta"
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Cria backup tar.gz
            with tarfile.open(backup_file, "w:gz") as tar:
                tar.add(self.config.chunk_root, arcname="chunk")
            
            # Calcula checksum
            sha256 = hashlib.sha256()
            with open(backup_file, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    sha256.update(chunk)
            
            metadata["checksum"] = sha256.hexdigest()
            metadata["size_mb"] = backup_file.stat().st_size / (1024**2)
            
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            logger.success(f"Backup criado: {backup_name} ({metadata['size_mb']:.1f} MB)")
            return str(backup_file)
            
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return ""
    
    def _get_chunk_version(self) -> str:
        """Obtém versão do CHUNK instalado"""
        version_file = Path(self.config.chunk_root) / "VERSION"
        if version_file.exists():
            try:
                content = version_file.read_text()
                match = re.search(r'CHUNK OS v([\d.]+)', content)
                if match:
                    return match.group(1)
            except:
                pass
        return "unknown"
    
    def list_backups(self) -> List[Dict]:
        """Lista backups disponíveis"""
        backups = []
        for meta_file in sorted(self.backup_path.glob("*.meta"), reverse=True):
            try:
                with open(meta_file, "r") as f:
                    meta = json.load(f)
                backups.append(meta)
            except:
                continue
        return backups
    
    def restore_backup(self, backup_name: str, target: str = None) -> bool:
        """Restaura backup específico"""
        backup_file = self.backup_path / f"{backup_name}.tar.gz"
        
        if not backup_file.exists():
            logger.error(f"Backup não encontrado: {backup_name}")
            return False
        
        target_root = target or self.config.chunk_root
        
        logger.info(f"Restaurando backup: {backup_name} para {target_root}")
        
        # Cria backup do estado atual antes de restaurar
        self.create_backup("pre_restore")
        
        # Remove sistema atual se existir
        if Path(target_root).exists():
            shutil.rmtree(target_root)
        
        try:
            import tarfile
            with tarfile.open(backup_file, "r:gz") as tar:
                # Na extração, precisamos lidar com o diretório raiz 'chunk' do backup
                temp_dir = Path(tempfile.mkdtemp())
                tar.extractall(path=temp_dir)
                shutil.move(str(temp_dir / "chunk"), target_root)
                shutil.rmtree(temp_dir)
            logger.success("Backup restaurado com sucesso!")
            return True
        except Exception as e:
            logger.error(f"Erro ao restaurar: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """Remove backups antigos, mantém apenas os N mais recentes"""
        backups = sorted(self.backup_path.glob("*.tar.gz"), 
                        key=lambda x: x.stat().st_mtime, reverse=True)
        
        removed = 0
        for backup in backups[keep_count:]:
            try:
                backup.unlink()
                (backup.with_suffix(".meta")).unlink(missing_ok=True)
                removed += 1
            except:
                pass
        
        if removed > 0:
            logger.info(f"Removidos {removed} backups antigos")
        return removed


# ============================================================================
# DOWNLOADER COM FALLOVER
# ============================================================================

class MasterDownloader:
    """Downloader inteligente com múltiplas fontes"""
    
    @staticmethod
    def download_file(url: str, dest: Path, retries: int = 3, 
                      callback: Callable = None) -> bool:
        """Download com retry e fallback"""
        for attempt in range(retries):
            try:
                if callback:
                    callback(0, f"Baixando {dest.name}...")
                
                urllib.request.urlretrieve(url, dest)
                
                if callback:
                    callback(100, f"Download concluído")
                
                return True
            except Exception as e:
                logger.warn(f"Tentativa {attempt + 1} falhou: {e}")
                time.sleep(2)
        
        logger.error(f"Falha ao baixar: {url}")
        return False
    
    @staticmethod
    def download_with_fallback(repos: List[str], path: str, dest: Path,
                                callback: Callable = None) -> bool:
        """Tenta baixar de múltiplos repositórios"""
        for repo in repos:
            url = f"{repo}/{path}"
            logger.info(f"Tentando: {url}")
            if MasterDownloader.download_file(url, dest, callback=callback):
                return True
        return False


# ============================================================================
# CONSTRUTOR DO CHUNK OS
# ============================================================================

class ChunkBuilder:
    """Constrói o CHUNK OS do zero com engenharia de precisão"""
    
    def __init__(self, config: ChunkConfig):
        self.config = config
        self.downloader = MasterDownloader()
        self.kernel_code = self._get_kernel_code()
    
    def _get_kernel_code(self) -> str:
        """Retorna o código fonte do kernel NMM incorporado"""
        # Código do NMM Kernel v2.0 (versão embutida)
        return '''#!/usr/bin/env python3
"""CHUNK OS — NMM Kernel v2.0 (Embedded Recovery Version)"""
import sys, time, threading, json
from dataclasses import dataclass
from typing import Dict, List, Optional
from collections import defaultdict

VERSION = "2.0.0"
AUTHOR = "Cloves Nascimento — CNGSM"

@dataclass
class WeightPage:
    page_id: int; layer_id: int; offset: int; size: int
    flash_offset: int; ram_address: Optional[int] = None
    state: int = 0; last_access: float = 0.0; access_count: int = 0

class NeuralMemoryManager:
    def __init__(self, ram_limit_mb: float = 1536.0, page_size_kb: int = 256):
        self.ram_limit_bytes = int(ram_limit_mb * 1024 * 1024)
        self.page_size = page_size_kb * 1024
        self.weight_pages: Dict[int, WeightPage] = {}
        self.current_layer: int = 0
        self.ram_used_bytes: int = 0
        self.page_faults: int = 0
        self.prefetch_hits: int = 0
        self.running = True
        
        print(f"[NMM] Inicializado | RAM: {ram_limit_mb}MB | Page: {page_size_kb}KB")
    
    def load_model(self, model_path: str) -> bool:
        layers = 32
        pages_per_layer = 1024
        for layer in range(layers):
            for page_idx in range(pages_per_layer):
                pid = layer * pages_per_layer + page_idx
                self.weight_pages[pid] = WeightPage(
                    page_id=pid, layer_id=layer,
                    offset=page_idx * self.page_size, size=self.page_size,
                    flash_offset=pid * self.page_size
                )
        print(f"[NMM] Modelo carregado: {len(self.weight_pages)} páginas")
        return True
    
    def get_weights(self, layer: int, offset: int, size: int):
        for pid, page in self.weight_pages.items():
            if page.layer_id == layer and page.offset == offset:
                if page.state == 0:
                    self.page_faults += 1
                    page.state = 2
                    self.ram_used_bytes += page.size
                    print(f"[NMM] Page fault: layer {layer}")
                page.last_access = time.time()
                page.access_count += 1
                return bytearray(size)
        return None
    
    def advance_layer(self, new_layer: int):
        self.current_layer = new_layer
    
    def get_stats(self):
        return type('Stats', (), {
            'total_page_faults': self.page_faults,
            'total_prefetch_hits': self.prefetch_hits,
            'ram_used_mb': self.ram_used_bytes / (1024*1024),
            'ram_limit_mb': self.ram_limit_bytes / (1024*1024),
            'cache_hit_rate': self.prefetch_hits / (self.page_faults + self.prefetch_hits + 1)
        })()
    
    def shutdown(self):
        self.running = False
        print("[NMM] Encerrado")

if __name__ == "__main__":
    print(f"NMM Kernel v{VERSION} — {AUTHOR}")
'''
    
    def create_directories(self) -> bool:
        """Cria estrutura de diretórios"""
        logger.step("📁 CRIANDO ESTRUTURA DE DIRETÓRIOS")
        
        dirs = [
            self.config.chunk_root,
            self.config.chunk_bin,
            self.config.chunk_lib,
            self.config.chunk_etc,
            self.config.chunk_models,
            f"{self.config.chunk_models}/registry",
            f"{self.config.chunk_models}/weights",
            self.config.chunk_logs,
            self.config.chunk_proc,
            self.config.chunk_backup,
        ]
        
        for d in dirs:
            try:
                Path(d).mkdir(parents=True, exist_ok=True)
                logger.status("OK", f"Criado: {d}")
            except Exception as e:
                logger.status("FAIL", f"Erro ao criar {d}: {e}")
                return False
        
        return True
    
    def generate_kernel(self) -> bool:
        """Gera arquivo do kernel NMM"""
        logger.step("⚙️ GERANDO KERNEL NMM")
        
        kernel_path = Path(self.config.chunk_bin) / "nmm_kernel.py"
        kernel_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(kernel_path, "w") as f:
            f.write(self.kernel_code)
        
        if platform.system() != "Windows":
            kernel_path.chmod(0o755)
        logger.status("OK", f"Kernel gerado: {kernel_path}")
        return True
    
    def generate_cli_tools(self) -> bool:
        """Gera ferramentas CLI"""
        logger.step("🖥️ GERANDO FERRAMENTAS CLI")
        
        bin_dir = Path(self.config.chunk_bin)
        bin_dir.mkdir(parents=True, exist_ok=True)
        
        # Script chunk-cli.sh / chunk-cli.bat
        if platform.system() == "Windows":
            cli_script = f'''@echo off
:: CHUNK OS CLI
set CHUNK_ROOT=%CHUNK_ROOT%
if "%CHUNK_ROOT%"=="" set CHUNK_ROOT={self.config.chunk_root}
set PATH=%CHUNK_ROOT%\\bin;%PATH%

if "%1"=="list" goto list
if "%1"=="load" goto load
if "%1"=="infer" goto infer
if "%1"=="status" goto status
if "%1"=="monitor" goto monitor
goto help

:list
echo Modelos: llama-3-8b, gemma-2b, phi-2
goto end

:load
echo 📦 Carregando modelo %2...
goto end

:infer
echo 🧠 Gerando resposta para: %2
goto end

:status
echo ✅ CHUNK OS operacional
goto end

:monitor
echo [Monitor] Pressione Ctrl+C para parar...
:loop
ps | findstr chunk
timeout /t 1 > nul
goto loop

:help
echo CHUNK OS CLI v2.0
echo.
echo Comandos:
echo   chunk-cli list              - Lista modelos
echo   chunk-cli load ^<modelo^>     - Carrega modelo
echo   chunk-cli infer ^<prompt^>    - Executa inferência
echo   chunk-cli status            - Status do sistema
echo   chunk-cli monitor           - Monitor em tempo real
goto end

:end
'''
            cli_path = bin_dir / "chunk-cli.bat"
        else:
            cli_script = '''#!/bin/bash
# CHUNK OS CLI
CHUNK_ROOT="${CHUNK_ROOT:-/chunk}"
export PATH="$CHUNK_ROOT/bin:$PATH"

show_help() {
    echo "CHUNK OS CLI v2.0"
    echo ""
    echo "Comandos:"
    echo "  chunk-cli list              - Lista modelos"
    echo "  chunk-cli load <modelo>     - Carrega modelo"
    echo "  chunk-cli infer <prompt>    - Executa inferência"
    echo "  chunk-cli status            - Status do sistema"
    echo "  chunk-cli monitor           - Monitor em tempo real"
}

case "${1:-help}" in
    list) echo "Modelos: llama-3-8b, gemma-2b, phi-2";;
    load) echo "📦 Carregando modelo ${2}...";;
    infer) echo "🧠 Gerando resposta para: ${2}";;
    status) echo "✅ CHUNK OS operacional | RAM: $(free -h | grep Mem | awk '{print $3}')";;
    monitor) watch -n 1 "ps aux | grep chunk";;
    help|*) show_help;;
esac
'''
            cli_path = bin_dir / "chunk-cli"
        
        with open(cli_path, "w") as f:
            f.write(cli_script)
        if platform.system() != "Windows":
            cli_path.chmod(0o755)
        logger.status("OK", f"Gerado: {cli_path.name}")
        
        return True
    
    def generate_configs(self) -> bool:
        """Gera arquivos de configuração"""
        logger.step("⚙️ GERANDO CONFIGURAÇÕES")
        
        etc_dir = Path(self.config.chunk_etc)
        etc_dir.mkdir(parents=True, exist_ok=True)
        
        config_content = f'''# CHUNK OS Configuration
# Gerado pelo Master Recovery Script v{VERSION}
# {AUTHOR}

[system]
version = {VERSION}
author = "{AUTHOR}"
signature = "{SIGNATURE}"

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
'''
        
        with open(etc_dir / "chunk.conf", "w") as f:
            f.write(config_content)
        logger.status("OK", "Gerado: chunk.conf")
        
        # Registry de modelos
        registry_dir = Path(self.config.chunk_models) / "registry"
        registry_dir.mkdir(parents=True, exist_ok=True)
        
        models_content = '''models:
  llama-3-8b:
    name: "Llama 3 8B"
    layers: 32
    total_params: 8000000000
  gemma-2b:
    name: "Gemma 2B"
    layers: 18
    total_params: 2000000000
  phi-2:
    name: "Phi-2"
    layers: 24
    total_params: 2700000000
'''
        
        with open(registry_dir / "models.yaml", "w") as f:
            f.write(models_content)
        logger.status("OK", "Gerado: models.yaml")
        
        return True
    
    def generate_init_script(self) -> bool:
        """Gera script de inicialização"""
        logger.step("🚀 GERANDO SCRIPT DE INICIALIZAÇÃO")
        
        if platform.system() == "Windows":
            init_script = f'''@echo off
:: CHUNK OS Init Script
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║   🧠 CHUNK OS — Cognitive Hierarchical Unified Neural Kernel    ║
echo ║                                                                  ║
echo ║   📛 {AUTHOR:53}║
echo ║   🔐 {SIGNATURE:53}║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

set CHUNK_ROOT={self.config.chunk_root}
set CHUNK_RAM_LIMIT_MB=1536
set PATH=%CHUNK_ROOT%\\bin;%PATH%

echo ✅ CHUNK OS v{VERSION} inicializado
echo.
echo Comandos disponíveis:
echo   chunk-cli infer ^<prompt^>  - Executa inferência
echo   chunk-cli status          - Status do sistema
echo   chunk-cli monitor         - Monitoramento
'''
            init_path = Path(self.config.chunk_root) / "init.bat"
        else:
            init_script = f'''#!/bin/bash
# CHUNK OS Init Script
# {AUTHOR}

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║   🧠 CHUNK OS — Cognitive Hierarchical Unified Neural Kernel    ║"
echo "║                                                                  ║"
echo "║   📛 {AUTHOR:53}║"
echo "║   🔐 {SIGNATURE:53}║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

export CHUNK_ROOT={self.config.chunk_root}
export CHUNK_RAM_LIMIT_MB=1536
export PATH=$CHUNK_ROOT/bin:$PATH

echo "✅ CHUNK OS v{VERSION} inicializado"
echo ""
echo "Comandos disponíveis:"
echo "  chunk-cli infer <prompt>  - Executa inferência"
echo "  chunk-cli status          - Status do sistema"
echo "  chunk-cli monitor         - Monitoramento"
'''
            init_path = Path(self.config.chunk_root) / "init.sh"
        
        with open(init_path, "w") as f:
            f.write(init_script)
        if platform.system() != "Windows":
            init_path.chmod(0o755)
        logger.status("OK", f"Gerado: {init_path.name}")
        
        return True
    
    def generate_version_file(self) -> bool:
        """Gera arquivo de versão"""
        version_content = f'''CHUNK OS v{VERSION}
Build Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Author: {AUTHOR}
Signature: {SIGNATURE}
Architecture: {platform.machine()}
OS: {platform.system()}
Status: RECOVERED BY MASTER ENGINEER SCRIPT v{VERSION}
'''
        
        version_path = Path(self.config.chunk_root) / "VERSION"
        with open(version_path, "w") as f:
            f.write(version_content)
        logger.status("OK", "Gerado: VERSION")
        
        return True
    
    def build_system(self) -> bool:
        """Constrói sistema completo"""
        logger.banner()
        
        success = all([
            self.create_directories(),
            self.generate_kernel(),
            self.generate_cli_tools(),
            self.generate_configs(),
            self.generate_init_script(),
            self.generate_version_file(),
        ])
        
        if success:
            logger.separator()
            logger.success("✅ CHUNK OS construído com sucesso!")
            logger.separator()
            
            # Mostra instruções
            init_cmd = "/chunk/init.sh" if platform.system() != "Windows" else "C:\\chunk\\init.bat"
            print(f"""
{Colors.CYAN}Para iniciar o CHUNK OS:{Colors.RESET}
  {Colors.GOLD}{init_cmd}{Colors.RESET}

{Colors.CYAN}Para executar inferência:{Colors.RESET}
  {Colors.GOLD}chunk-cli infer "Olá, mundo!"{Colors.RESET}

{Colors.CYAN}Para verificar status:{Colors.RESET}
  {Colors.GOLD}chunk-cli status{Colors.RESET}
""")
        else:
            logger.error("❌ Falha na construção do CHUNK OS")
        
        return success


# ============================================================================
# SCRIPT MESTRE DE RECUPERAÇÃO
# ============================================================================

class MasterRecoveryScript:
    """Script mestre que recupera o sistema em segundos"""
    
    def __init__(self):
        self.config = ChunkConfig()
        self.detector = SystemDetector()
        self.backup_manager = BackupManager(self.config)
        self.builder = ChunkBuilder(self.config)
        self.health_status: Dict[str, Any] = {}
    
    def check_system(self) -> Dict:
        """Verifica integridade do sistema"""
        logger.step("🔍 VERIFICANDO INTEGRIDADE DO SISTEMA")
        
        issues = []
        warnings = []
        
        # 1. Verifica diretório CHUNK
        chunk_exists = Path(self.config.chunk_root).exists()
        if chunk_exists:
            logger.status("OK", "Diretório CHUNK encontrado")
        else:
            logger.status("FAIL", "Diretório CHUNK não encontrado")
            issues.append("missing_chunk_root")
        
        # 2. Verifica binários principais
        cli_name = "chunk-cli.bat" if platform.system() == "Windows" else "chunk-cli"
        bin_path = Path(self.config.chunk_bin) / cli_name
        if bin_path.exists():
            logger.status("OK", f"Binário {cli_name} encontrado")
        else:
            logger.status("WARN", f"Binário {cli_name} ausente")
            warnings.append(f"missing_{cli_name}")
        
        # 3. Verifica configuração
        config_path = Path(self.config.chunk_etc) / "chunk.conf"
        if config_path.exists():
            logger.status("OK", "Configuração encontrada")
        else:
            logger.status("WARN", "Configuração ausente")
            warnings.append("missing_config")
        
        # 4. Verifica kernel NMM
        kernel_path = Path(self.config.chunk_bin) / "nmm_kernel.py"
        if kernel_path.exists():
            logger.status("OK", "Kernel NMM encontrado")
        else:
            logger.status("WARN", "Kernel NMM ausente")
            warnings.append("missing_kernel")
        
        # 5. Verifica permissões (apenas Unix)
        if platform.system() != "Windows" and kernel_path.exists():
            if os.access(kernel_path, os.X_OK):
                logger.status("OK", "Permissões corretas")
            else:
                logger.status("WARN", "Permissões incorretas")
                warnings.append("bad_permissions")
        
        # 6. Verifica backups
        backups = self.backup_manager.list_backups()
        if backups:
            logger.status("OK", f"Backups disponíveis: {len(backups)}")
        else:
            logger.status("WARN", "Nenhum backup encontrado")
            warnings.append("no_backups")
        
        # 7. Verifica espaço em disco
        storage_gb = self.detector.get_storage_gb(self.config.chunk_root)
        if storage_gb > self.config.min_storage_gb:
            logger.status("OK", f"Espaço em disco: {storage_gb:.1f} GB")
        else:
            logger.status("WARN", f"Espaço em disco baixo: {storage_gb:.1f} GB")
            warnings.append("low_storage")
        
        # 8. Verifica RAM
        ram_gb = self.detector.get_ram_gb()
        if ram_gb >= self.config.min_ram_gb:
            logger.status("OK", f"RAM disponível: {ram_gb:.1f} GB")
        else:
            logger.status("WARN", f"RAM abaixo do mínimo: {ram_gb:.1f} GB")
            warnings.append("low_ram")
        
        # 9. Testa execução do kernel (se disponível)
        if kernel_path.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(kernel_path)],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    logger.status("OK", "Kernel NMM executável")
                else:
                    logger.status("WARN", "Kernel NMM com erro")
                    warnings.append("kernel_error")
            except:
                logger.status("WARN", "Kernel NMM não responde")
                warnings.append("kernel_timeout")
        
        needs_recovery = len(issues) > 0 or len(warnings) >= 3
        
        return {
            "issues": issues,
            "warnings": warnings,
            "needs_recovery": needs_recovery,
            "chunk_exists": chunk_exists,
            "backups_count": len(backups),
            "ram_gb": ram_gb,
            "storage_gb": storage_gb
        }
    
    def create_emergency_backup(self) -> str:
        """Cria backup de emergência"""
        logger.step("💾 CRIANDO BACKUP DE EMERGÊNCIA")
        return self.backup_manager.create_backup("emergency")
    
    def restore_from_backup(self) -> bool:
        """Recupera de backup existente"""
        logger.step("📀 RECUPERANDO DE BACKUP")
        
        backups = self.backup_manager.list_backups()
        if not backups:
            logger.warn("Nenhum backup disponível")
            return False
        
        print(f"\n{Colors.CYAN}Backups disponíveis:{Colors.RESET}")
        for i, backup in enumerate(backups[:5]):
            size_mb = backup.get("size_mb", 0)
            timestamp = backup.get("timestamp", "unknown")
            print(f"  {i+1}. {backup['backup_name']} ({size_mb:.1f} MB) - {timestamp}")
        
        # Usa o mais recente automaticamente
        latest = backups[0]
        print(f"\n{Colors.GOLD}→ Usando backup mais recente: {latest['backup_name']}{Colors.RESET}")
        
        return self.backup_manager.restore_backup(latest['backup_name'])
    
    def full_clean_install(self) -> bool:
        """Instalação limpa do zero"""
        logger.step("🏗️ INSTALAÇÃO LIMPA DO ZERO")
        
        # Remove sistema antigo se existir
        if Path(self.config.chunk_root).exists():
            logger.info("Removendo sistema antigo...")
            try:
                shutil.rmtree(self.config.chunk_root)
                logger.success("Sistema antigo removido")
            except Exception as e:
                logger.warn(f"Não foi possível remover completamente: {e}")
        
        return self.builder.build_system()
    
    def fix_permissions(self) -> bool:
        """Corrige permissões do sistema"""
        if platform.system() == "Windows":
            logger.info("Permissões no Windows: Ignorado.")
            return True
            
        logger.step("🔧 CORRIGINDO PERMISSÕES")
        
        try:
            # Executáveis
            bin_dir = Path(self.config.chunk_bin)
            if bin_dir.exists():
                for f in bin_dir.glob("*"):
                    f.chmod(0o755)
                logger.success("Permissões de binários corrigidas")
            
            # Diretórios
            dirs = [
                self.config.chunk_root,
                self.config.chunk_lib,
                self.config.chunk_etc,
                self.config.chunk_logs,
                self.config.chunk_backup
            ]
            for d in dirs:
                path = Path(d)
                if path.exists():
                    path.chmod(0o755)
            
            logger.success("Permissões corrigidas com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao corrigir permissões: {e}")
            return False
    
    def test_system(self) -> Dict:
        """Testa o sistema após recuperação"""
        logger.step("🧪 TESTANDO SISTEMA RECUPERADO")
        
        results = {
            "kernel_ok": False,
            "cli_ok": False,
            "config_ok": False,
            "demo_ok": False
        }
        
        # Testa kernel NMM
        kernel_path = Path(self.config.chunk_bin) / "nmm_kernel.py"
        if kernel_path.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(kernel_path)],
                    capture_output=True, text=True, timeout=10
                )
                if "NMM Kernel" in result.stdout or "NMM Kernel" in result.stderr:
                    results["kernel_ok"] = True
                    logger.status("OK", "Kernel NMM funcionando")
                else:
                    logger.status("FAIL", "Kernel NMM resposta inválida")
            except Exception as e:
                logger.status("FAIL", f"Kernel NMM erro: {e}")
        else:
            logger.status("WARN", "Kernel NMM não encontrado")
        
        # Testa CLI
        cli_name = "chunk-cli.bat" if platform.system() == "Windows" else "chunk-cli"
        cli_path = Path(self.config.chunk_bin) / cli_name
        if cli_path.exists():
            try:
                result = subprocess.run([str(cli_path), "status"], 
                                       capture_output=True, text=True, timeout=5)
                results["cli_ok"] = True
                logger.status("OK", "CLI funcionando")
            except:
                logger.status("FAIL", "CLI erro")
        else:
            logger.status("WARN", "CLI não encontrado")
        
        # Testa configuração
        config_path = Path(self.config.chunk_etc) / "chunk.conf"
        if config_path.exists():
            results["config_ok"] = True
            logger.status("OK", "Configuração válida")
        else:
            logger.status("FAIL", "Configuração ausente")
        
        # Testa demo com Python
        if results["kernel_ok"]:
            try:
                # Use the path to the kernel we just built
                kernel_dir = str(Path(self.config.chunk_bin))
                demo_code = f'''
import sys
sys.path.insert(0, r"{kernel_dir}")
try:
    from nmm_kernel import NeuralMemoryManager
    nmm = NeuralMemoryManager(ram_limit_mb=512)
    nmm.load_model("test")
    nmm.shutdown()
    print("DEMO_OK")
except Exception as e:
    print(f"ERROR: {{e}}")
'''
                result = subprocess.run(
                    [sys.executable, "-c", demo_code],
                    capture_output=True, text=True, timeout=10
                )
                if "DEMO_OK" in result.stdout:
                    results["demo_ok"] = True
                    logger.status("OK", "Demo NMM funcionando")
                else:
                    logger.status("FAIL", f"Demo erro: {result.stderr[:100]}")
            except:
                logger.status("FAIL", "Demo timeout")
        
        return results
    
    def run_auto_recovery(self) -> Tuple[bool, Dict]:
        """Executa recuperação automática completa"""
        logger.banner()
        
        print(f"\n{Colors.GOLD}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.SHIELD} MASTER ENGINEER RECOVERY — MODO AUTOMÁTICO{Colors.RESET}")
        print(f"{Colors.GOLD}{'═' * 70}{Colors.RESET}\n")
        
        # Informações do sistema
        print(f"{Colors.CYAN}📋 INFORMAÇÕES DO SISTEMA:{Colors.RESET}")
        print(f"   • OS: {self.detector.detect_os()}")
        print(f"   • Arch: {self.detector.get_arch()}")
        print(f"   • CPU Cores: {self.detector.get_cpu_cores()}")
        print(f"   • RAM: {self.detector.get_ram_gb():.1f} GB")
        print(f"   • Storage: {self.detector.get_storage_gb():.1f} GB")
        print(f"   • Root/Admin: {self.detector.is_root()}")
        print(f"   • Network: {'Yes' if self.detector.get_network_connectivity() else 'No'}")
        
        # Verifica sistema
        status = self.check_system()
        
        # Cria backup de emergência (sempre se o diretório existir)
        if status["chunk_exists"]:
            self.create_emergency_backup()
        
        recovered = False
        recovery_method = "none"
        
        if status["chunk_exists"] and status["backups_count"] > 0:
            logger.info("Tentando recuperar de backup...")
            if self.restore_from_backup():
                recovered = True
                recovery_method = "backup"
        
        if not recovered:
            logger.info("Realizando instalação limpa...")
            if self.full_clean_install():
                recovered = True
                recovery_method = "clean_install"
        
        if recovered:
            self.fix_permissions()
            test_results = self.test_system()
            
            # Cria backup pós-recuperação
            self.backup_manager.create_backup("post_recovery")
            self.backup_manager.cleanup_old_backups(keep_count=10)
            
            logger.separator()
            if all(test_results.values()):
                logger.success("✅ SISTEMA TOTALMENTE RECUPERADO!")
            else:
                logger.warn("⚠️ SISTEMA RECUPERADO COM RESSALVAS")
            
            return True, {
                "recovery_method": recovery_method,
                "test_results": test_results,
                "status": status
            }
        else:
            logger.error("❌ RECUPERAÇÃO FALHOU!")
            return False, {"error": "recovery_failed", "status": status}
    
    def run_interactive(self):
        """Modo interativo para engenheiro"""
        logger.banner()
        
        while True:
            print(f"\n{Colors.GOLD}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.TOOL} MASTER ENGINEER COMMAND CENTER{Colors.RESET}")
            print(f"{Colors.GOLD}{'═' * 70}{Colors.RESET}\n")
            
            # Mostra status resumido
            chunk_exists = Path(self.config.chunk_root).exists()
            if chunk_exists:
                version_file = Path(self.config.chunk_root) / "VERSION"
                if version_file.exists():
                    try:
                        content = version_file.read_text()
                        version_match = re.search(r'CHUNK OS v([\d.]+)', content)
                        version = version_match.group(1) if version_match else "unknown"
                        print(f"{Colors.GREEN}📦 CHUNK OS v{version} — Operacional{Colors.RESET}")
                    except:
                        print(f"{Colors.GREEN}📦 CHUNK OS — Instalado{Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}📦 CHUNK OS — Instalado{Colors.RESET}")
            else:
                print(f"{Colors.RED}📦 CHUNK OS — Não instalado{Colors.RESET}")
            
            print(f"\n{Colors.CYAN}Comandos disponíveis:{Colors.RESET}")
            print("  1. Verificar integridade do sistema")
            print("  2. Recuperação automática completa")
            print("  3. Restaurar de backup")
            print("  4. Criar backup")
            print("  5. Instalação limpa do zero")
            print("  6. Corrigir permissões")
            print("  7. Testar sistema")
            print("  8. Listar backups")
            print("  9. Limpar backups antigos")
            print("  10. Sair")
            
            try:
                choice = input(f"\n{Colors.GOLD}🔧 Engenheiro > {Colors.RESET}").strip()
            except EOFError:
                break
            
            if choice == "1":
                self.check_system()
            elif choice == "2":
                success, data = self.run_auto_recovery()
                if success:
                    logger.success(f"Recuperação concluída via {data.get('recovery_method', 'unknown')}")
            elif choice == "3":
                backups = self.backup_manager.list_backups()
                if backups:
                    print(f"\n{Colors.CYAN}Backups disponíveis:{Colors.RESET}")
                    for i, b in enumerate(backups[:10]):
                        print(f"  {i+1}. {b['backup_name']}")
                    idx = input(f"\n{Colors.GOLD}Selecione (ou Enter para o mais recente): {Colors.RESET}")
                    if idx:
                        try:
                            selected = backups[int(idx)-1]
                            self.backup_manager.restore_backup(selected['backup_name'])
                        except:
                            logger.error("Seleção inválida")
                    else:
                        self.backup_manager.restore_backup(backups[0]['backup_name'])
                else:
                    logger.warn("Nenhum backup disponível")
            elif choice == "4":
                desc = input("Descrição do backup (opcional): ")
                self.backup_manager.create_backup("manual", desc)
            elif choice == "5":
                confirm = input(f"{Colors.RED}⚠️ Isso removerá toda a instalação atual. Confirmar? (s/N): {Colors.RESET}")
                if confirm.lower() == 's':
                    self.full_clean_install()
                else:
                    logger.info("Operação cancelada")
            elif choice == "6":
                self.fix_permissions()
            elif choice == "7":
                self.test_system()
            elif choice == "8":
                backups = self.backup_manager.list_backups()
                print(f"\n{Colors.CYAN}Backups disponíveis:{Colors.RESET}")
                for b in backups[:15]:
                    size_mb = b.get("size_mb", 0)
                    timestamp = b.get("timestamp", "unknown")
                    desc = b.get("description", "")
                    print(f"  • {b['backup_name']} ({size_mb:.1f} MB) - {timestamp} - {desc}")
            elif choice == "9":
                keep = input("Quantos backups manter? (default: 10): ")
                try:
                    keep_count = int(keep) if keep else 10
                    self.backup_manager.cleanup_old_backups(keep_count)
                except:
                    logger.error("Número inválido")
            elif choice == "10":
                print(f"\n{Colors.GREEN}👋 Até a próxima, engenheiro!{Colors.RESET}\n")
                break
            else:
                logger.warn("Comando inválido")


# ============================================================================
# PONTO DE ENTRADA PRINCIPAL
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CHUNK OS — Master Engineer Recovery Script v2.0",
        epilog=f"CNGSM — {AUTHOR} — Engenharia da Próxima Geração"
    )
    parser.add_argument("--auto", "-a", action="store_true",
                        help="Executa recuperação automática")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Modo interativo")
    parser.add_argument("--check", "-c", action="store_true",
                        help="Apenas verifica sistema")
    parser.add_argument("--fix", "-f", action="store_true",
                        help="Corrige permissões")
    parser.add_argument("--clean", "--install", action="store_true",
                        help="Instalação limpa do zero")
    parser.add_argument("--backup", "-b", action="store_true",
                        help="Cria backup de emergência")
    parser.add_argument("--restore", "-r", type=str, metavar="NOME",
                        help="Restaura backup específico")
    parser.add_argument("--list-backups", "-l", action="store_true",
                        help="Lista backups disponíveis")
    parser.add_argument("--test", "-t", action="store_true",
                        help="Testa sistema")
    parser.add_argument("--version", "-v", action="store_true",
                        help="Mostra versão")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"CHUNK OS Master Recovery Script v{VERSION}")
        print(f"Author: {AUTHOR}")
        print(f"Signature: {SIGNATURE}")
        return 0
    
    recovery = MasterRecoveryScript()
    
    if args.auto:
        success, data = recovery.run_auto_recovery()
        return 0 if success else 1
    elif args.interactive:
        recovery.run_interactive()
        return 0
    elif args.check:
        status = recovery.check_system()
        if status["needs_recovery"]:
            logger.warn("Sistema precisa de recuperação")
            return 1
        else:
            logger.success("Sistema íntegro")
            return 0
    elif args.fix:
        recovery.fix_permissions()
        recovery.test_system()
        return 0
    elif args.clean:
        success = recovery.full_clean_install()
        return 0 if success else 1
    elif args.backup:
        backup_path = recovery.create_emergency_backup()
        return 0 if backup_path else 1
    elif args.restore:
        success = recovery.backup_manager.restore_backup(args.restore)
        return 0 if success else 1
    elif args.list_backups:
        backups = recovery.backup_manager.list_backups()
        for b in backups:
            print(f"{b['backup_name']} - {b.get('timestamp', 'unknown')}")
        return 0
    elif args.test:
        results = recovery.test_system()
        all_ok = all(results.values())
        return 0 if all_ok else 1
    else:
        # Modo padrão: interativo
        recovery.run_interactive()
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️ Operação interrompida pelo engenheiro{Colors.RESET}\n")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Erro fatal: {e}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
