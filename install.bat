@echo off
echo ========================================
echo Sistema de Cotacoes Pro v3.1
echo Instalando dependencias...
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao esta instalado!
    echo Instale Python 3.8+ de: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Instalando pacotes Python...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ========================================
echo Instalacao concluida!
echo.
echo PROXIMO PASSO:
echo 1. Configure a API Key do Groq
echo 2. Execute: run.bat
echo ========================================
pause
