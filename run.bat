@echo off
echo ========================================
echo Sistema de Cotacoes Pro v3.1
echo Iniciando aplicacao...
echo ========================================
echo.

if not exist ".env" (
    echo AVISO: Arquivo .env nao encontrado!
    echo Configure a API Key do Groq antes de usar a importacao de PDFs.
    echo.
    set /p GROQ_KEY="Cole sua API Key do Groq (ou Enter para pular): "
    if not "!GROQ_KEY!"=="" (
        echo GROQ_API_KEY=!GROQ_KEY! > .env
        echo API Key salva em .env
    )
    echo.
)

python app.py

if errorlevel 1 (
    echo.
    echo ERRO ao executar aplicacao!
    echo Verifique se todas as dependencias estao instaladas.
    pause
)
