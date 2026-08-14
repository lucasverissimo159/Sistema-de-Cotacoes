import os
from pathlib import Path
from dotenv import load_dotenv

# Raiz do projeto (config.py fica em cotacoes/, portanto sobe um nivel)
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / 'data'
UPLOADS_DIR = DATA_DIR / 'uploads'
OUTPUTS_DIR = DATA_DIR / 'outputs'

for dir_path in [DATA_DIR, UPLOADS_DIR, OUTPUTS_DIR]:
    dir_path.mkdir(exist_ok=True)

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_MODEL = 'llama-3.3-70b-versatile'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

COLUNAS_IMPORTANTES = ['FORNECEDOR', 'PRODUTO', 'QUANTIDADE', 'PREÇO', 'VALIDADE', 'ORIGEM']

ZOOM_MIN = 0.5
ZOOM_MAX = 3.0
ZOOM_DEFAULT = 1.0
ZOOM_STEP = 0.1
