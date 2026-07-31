#!/bin/bash

echo "========================================"
echo "Sistema de Cotações Pro v3.1"
echo "Instalando dependências..."
echo "========================================"
echo

if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python não está instalado!"
    echo "Instale Python 3.8+ do gerenciador de pacotes do seu sistema"
    exit 1
fi

echo "Instalando pacotes Python..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo
echo "========================================"
echo "Instalação concluída!"
echo
echo "PRÓXIMO PASSO:"
echo "1. Configure a API Key do Groq"
echo "2. Execute: ./run.sh"
echo "========================================"
