#!/usr/bin/env python3
"""Script para testar a configuração da API Groq"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

def test_api():
    print("=" * 50)
    print("TESTE DE CONFIGURAÇÃO - API GROQ")
    print("=" * 50)
    print()
    
    if not GROQ_API_KEY or GROQ_API_KEY == 'your_api_key_here':
        print("❌ ERRO: API Key não configurada!")
        print()
        print("Configure a variável GROQ_API_KEY:")
        print("1. Crie um arquivo .env na pasta do projeto")
        print("2. Adicione: GROQ_API_KEY=sua_chave_aqui")
        print()
        print("Obtenha sua chave em: https://console.groq.com/keys")
        return False
    
    print(f"✅ API Key encontrada: {GROQ_API_KEY[:20]}...")
    print()
    print("Testando conexão com API Groq...")
    print()
    
    try:
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'llama-3.3-70b-versatile',
            'messages': [
                {
                    'role': 'user',
                    'content': 'Responda apenas: OK'
                }
            ],
            'max_tokens': 10
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ SUCESSO! API está funcionando corretamente!")
            print()
            print("Resposta da API:")
            data = response.json()
            content = data['choices'][0]['message']['content']
            print(f"  {content}")
            print()
            print("=" * 50)
            print("Configuração OK! Você pode usar o sistema.")
            print("=" * 50)
            return True
        else:
            print(f"❌ ERRO {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO de conexão: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_api()
    sys.exit(0 if success else 1)
