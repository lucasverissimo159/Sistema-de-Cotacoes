# 🧾 Sistema de Cotações Pro

Aplicação desktop (PyQt6) que **extrai e compara cotações de fornecedores a
partir de PDFs** usando IA (API do **Groq**). Lê os PDFs enviados, estrutura os
dados (fornecedor, produto, quantidade, preço, validade, origem) e gera uma
planilha comparativa de preços.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Funcionalidades

- 📄 Importação de múltiplos PDFs de cotação
- 🤖 Extração estruturada via IA (Groq / Llama 3.3)
- 📊 Tabela comparativa e exportação para Excel (`.xlsx`)
- 🔍 Zoom e visualização dos dados

## 🚀 Instalação

```bash
pip install -r requirements.txt
```

## 🔑 Configuração da chave de API (obrigatório para a IA)

A aplicação **não** contém nenhuma chave de API. Você precisa fornecer a sua:

1. Copie o template e crie o seu `.env` (não versionado):
   ```bash
   cp .env.example .env
   ```
2. Edite `.env` e preencha a sua chave do Groq (gratuita em
   <https://console.groq.com/keys>):
   ```
   GROQ_API_KEY=sua_chave_aqui
   ```

Em `config.py`, a chave é lida da variável de ambiente com **valor em branco por
padrão** (`GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')`). Sem a chave, o app
**inicia normalmente** e apenas avisa que é preciso configurá-la ao tentar
processar PDFs (não ocorre exceção não tratada).

## ▶️ Uso

```bash
python app.py
```

Os PDFs enviados vão para `data/uploads/` e as planilhas geradas para
`data/outputs/` — ambos **não versionados** (podem conter dados reais de
fornecedores/cotações).

## 🗂️ Estrutura

```
sistema_cotacoes/
├── app.py               # Ponto de entrada (PyQt6)
├── main_window.py       # Janela principal
├── config.py            # Configuração (lê GROQ_API_KEY do ambiente)
├── pdf_processor.py     # Extração via API do Groq
├── data_manager.py      # Manipulação de dados
├── table_model.py       # Modelo da tabela
├── styles.py            # Estilos da UI
├── .env.example         # Template de configuração (sem segredos)
└── data/                # uploads/ e outputs/ (runtime, não versionados)
```

## 🔒 Segurança

- A chave de API fica apenas no seu `.env` local (no `.gitignore`).
- PDFs de entrada e planilhas de saída não são versionados.

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
