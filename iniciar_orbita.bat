@echo off
chcp 65001 >nul
title Orbita Server - Configuracao Gratuita (SITEEE)
echo ============================================================
echo   ORBITA — Iniciando Ambiente Local Gratuito (FastAPI + WS)
echo   Pasta: %~dp0
echo ============================================================

cd /d "%~dp0"

if not exist ".venv" (
    echo [1/3] Criando ambiente virtual Python (.venv)...
    python -m venv .venv
)

echo [2/3] Ativando ambiente e verificando pacotes gratuitos...
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo [3/3] Abrindo navegador em http://localhost:8000 e iniciando servidor...
start http://localhost:8000
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
pause
