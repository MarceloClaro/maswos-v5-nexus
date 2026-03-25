#!/usr/bin/env python3
"""
Testar API do Opencode Zen
"""
import os
import requests
from pathlib import Path

# Carregar .env
env_path = Path(".env")
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

api_key = os.getenv("OPENCODE_API_KEY")
if not api_key:
    print("Chave não encontrada")
    exit(1)

url = "https://opencode.ai/zen/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "mimo-v2-omni-free",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Erro: {e}")