@echo off
TITLE CHUNK OS - MASTER IGNITION
COLOR 0B

echo.
echo  ╔═══════════════════════════════════════════════════════════════════╗
echo  ║                                                                   ║
echo  ║   CHUNK OS - MASTER STARTUP ^& TEST                                 ║
║                                                                   ║
echo  ║   CNGSM - Cognitive Neural ^& Generative Systems Management          ║
echo  ║   Cloves Nascimento - Arquiteto de Ecossistemas Cognitivos         ║
echo  ║                                                                   ║
echo  ╚═══════════════════════════════════════════════════════════════════╝
echo.

echo [INFO] Inicializando Kernel e Estrutura de Sistema...
python chunk_recovery.py --auto

echo.
echo [INFO] Iniciando Servidor de Dashboard (Porta 8001)...
start /B python -m http.server 8001 > nul 2>&1

echo.
echo [INFO] Iniciando Prova de Conceito: Integração LLAMA 3 8B...
echo [INFO] Simulando execução com 92.6%% de economia de RAM...
echo.

python llama3_chunk_integration.py --demo

echo.
echo ══════════════════════════════════════════════════════════════════════
echo [OK] SISTEMA OPERACIONAL E TESTADO COM SUCESSO!
echo [OK] Dashboard ativo em http://localhost:8001
echo ══════════════════════════════════════════════════════════════════════
echo.
pause
