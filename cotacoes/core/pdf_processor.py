import base64
import requests
import json
from pathlib import Path
import PyPDF2
from typing import List, Dict, Any
from ..config import GROQ_API_KEY, GROQ_MODEL, GROQ_API_URL

class PDFProcessor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise ValueError("API Key do Groq não configurada. Configure através da variável GROQ_API_KEY")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrai texto do PDF usando PyPDF2"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")
    
    def pdf_to_base64(self, pdf_path: str) -> str:
        """Converte PDF para base64"""
        with open(pdf_path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')
    
    def process_pdf_with_ai(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Processa o PDF e extrai dados da cotação usando IA"""
        
        text_content = self.extract_text_from_pdf(pdf_path)
        fornecedor = Path(pdf_path).stem.upper()
        
        prompt = f"""Você é um assistente especializado em extrair dados de cotações de insumos farmacêuticos.

Analise o texto abaixo extraído de uma cotação do fornecedor "{fornecedor}" e extraia TODOS os produtos listados.

TEXTO DA COTAÇÃO:
{text_content}

INSTRUÇÕES:
1. Extraia TODOS os produtos/insumos listados na cotação
2. Para cada produto, extraia:
   - FORNECEDOR: Use "{fornecedor}"
   - PRODUTO: Nome completo do produto/insumo
   - QUANTIDADE: Quantidade com unidade (ex: "1 KG", "500 G", "100 ML")
   - PREÇO: Valor unitário em reais (apenas número, ex: "150.00")
   - VALIDADE: Data de validade no formato DD/MM/YYYY
   - ORIGEM: País de origem (Brasil, China, Índia, etc)

3. IMPORTANTE:
   - Se um produto tiver múltiplas quantidades/preços, crie uma linha para CADA quantidade
   - Normalize as quantidades: use "KG" para quilos, "G" para gramas, "ML" ou "L" para líquidos
   - Para preços, use APENAS números com ponto decimal (ex: "150.50")
   - Se algum campo não estiver disponível, use "N/A"
   - Mantenha os nomes dos produtos EXATAMENTE como aparecem na cotação

RETORNE APENAS UM JSON ARRAY COM OS DADOS, SEM NENHUM TEXTO ADICIONAL:
[
  {{
    "FORNECEDOR": "nome_fornecedor",
    "PRODUTO": "nome_produto",
    "QUANTIDADE": "quantidade com unidade",
    "PREÇO": "valor_numerico",
    "VALIDADE": "DD/MM/YYYY",
    "ORIGEM": "país"
  }}
]

RETORNE APENAS O JSON, NADA MAIS."""

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': GROQ_MODEL,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.1,
            'max_tokens': 4000
        }
        
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            data = json.loads(content)
            
            if not isinstance(data, list):
                raise ValueError("Resposta da IA não é uma lista")
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição à API Groq: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar JSON da resposta: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao processar PDF com IA: {str(e)}")
    
    def process_multiple_pdfs(self, pdf_paths: List[str]) -> List[Dict[str, Any]]:
        """Processa múltiplos PDFs e retorna dados consolidados"""
        all_data = []
        
        for pdf_path in pdf_paths:
            try:
                data = self.process_pdf_with_ai(pdf_path)
                all_data.extend(data)
            except Exception as e:
                print(f"Erro ao processar {pdf_path}: {str(e)}")
                continue
        
        return all_data
