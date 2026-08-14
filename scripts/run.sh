#!/bin/bash
cd "$(dirname "$0")/.." || exit 1

echo "========================================"
echo "Sistema de Cotações Pro v3.1"
echo "Iniciando aplicação..."
echo "========================================"
echo

if [ ! -f ".env" ]; then
    echo "AVISO: Arquivo .env não encontrado!"
    echo "Configure a API Key do Groq antes de usar a importação de PDFs."
    echo
    read -p "Cole sua API Key do Groq (ou Enter para pular): " GROQ_KEY
    if [ ! -z "$GROQ_KEY" ]; then
        echo "GROQ_API_KEY=$GROQ_KEY" > .env
        echo "API Key salva em .env"
    fi
    echo
fi

python3 app.py

if [ $? -ne 0 ]; then
    echo
    echo "ERRO ao executar aplicação!"
    echo "Verifique se todas as dependências estão instaladas."
    read -p "Pressione Enter para continuar..."
fi
