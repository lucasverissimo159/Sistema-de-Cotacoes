# 🧾 Pro Quotes System (Sistema de Cotações Pro)

Desktop application (PyQt6) that **extracts and compares supplier quotes from PDFs** using AI (**Groq** API). It reads uploaded PDFs, structures the data (supplier, product, quantity, price, validity, origin), and generates a comparative price spreadsheet.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 📄 Import multiple quote PDFs
- 🤖 Structured extraction via AI (Groq / Llama 3.3)
- 📊 Comparative table and export to Excel (`.xlsx`)
- 🔍 Zoom and data visualization

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 🔑 API Key Configuration (required for AI)

The application does **not** contain any API keys. You must provide your own:

1. Copy the template and create your `.env` (not versioned):
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and fill in your Groq key (free at <https://console.groq.com/keys>):
   ```
   GROQ_API_KEY=your_key_here
   ```

In `config.py`, the key is read from the environment variable with a **blank value by default** (`GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')`). Without the key, the app **starts normally** and only warns that it needs to be configured when trying to process PDFs (no unhandled exceptions occur).

## ▶️ Usage

```bash
python app.py
```

Uploaded PDFs go to `data/uploads/` and generated spreadsheets to `data/outputs/` — both **not versioned** (they may contain real supplier/quote data).

### 🧪 Example Data

The `exemplos/` folder contains **fictitious** spreadsheets to test the application without depending on real PDFs:

- `exemplos/cotacoes_exemplo.xlsx` — example quotes (8 products × 3 suppliers). Open in **📂 Load Excel** and click **Compare**.
- `exemplos/comparacao_precos_exemplo.xlsx` — example of the comparison result (sorted by product/price, with the cheapest highlighted).

## 🗂️ Structure

```
sistema_cotacoes/
├── app.py                  # Entry point (PyQt6)
├── requirements.txt
├── .env.example            # Configuration template (no secrets)
├── cotacoes/               # Main package
│   ├── config.py           # Configuration (reads GROQ_API_KEY from environment)
│   ├── core/
│   │   ├── data_manager.py # Data handling / Excel
│   │   └── pdf_processor.py# Extraction via Groq API
│   └── ui/
│       ├── main_window.py  # Main window
│       ├── table_model.py  # Table model
│       └── styles.py       # UI Styles
├── scripts/                # install/run (.bat and .sh)
├── docs/                   # Guides (.txt)
├── tests/                  # teste_ia.py
├── exemplos/               # Example spreadsheets (fictitious)
└── data/                   # uploads/ and outputs/ (runtime, not versioned)
```

## 🔒 Security

- The API key stays only in your local `.env` (in `.gitignore`).
- Input PDFs and output spreadsheets are not versioned.

## 📄 License

Distributed under the MIT license. See [LICENSE](LICENSE).

---

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

### 🧪 Dados de exemplo

A pasta `exemplos/` contém planilhas **fictícias** para testar a aplicação sem
depender de PDFs reais:

- `exemplos/cotacoes_exemplo.xlsx` — cotações de exemplo (8 produtos × 3
  fornecedores). Abra em **📂 Carregar Excel** e clique em **Comparar**.
- `exemplos/comparacao_precos_exemplo.xlsx` — exemplo do resultado da
  comparação (ordenado por produto/preço, com o mais barato destacado).

## 🗂️ Estrutura

```
sistema_cotacoes/
├── app.py                  # Ponto de entrada (PyQt6)
├── requirements.txt
├── .env.example            # Template de configuração (sem segredos)
├── cotacoes/               # Pacote principal
│   ├── config.py           # Configuração (lê GROQ_API_KEY do ambiente)
│   ├── core/
│   │   ├── data_manager.py # Manipulação de dados / Excel
│   │   └── pdf_processor.py# Extração via API do Groq
│   └── ui/
│       ├── main_window.py  # Janela principal
│       ├── table_model.py  # Modelo da tabela
│       └── styles.py       # Estilos da UI
├── scripts/                # install/run (.bat e .sh)
├── docs/                   # Guias (.txt)
├── tests/                  # teste_ia.py
├── exemplos/               # Planilhas de exemplo (fictícias)
└── data/                   # uploads/ e outputs/ (runtime, não versionados)
```

## 🔒 Segurança

- A chave de API fica apenas no seu `.env` local (no `.gitignore`).
- PDFs de entrada e planilhas de saída não são versionados.

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).