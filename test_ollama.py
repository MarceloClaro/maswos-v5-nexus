#!/usr/bin/env python3
"""
Testar Ollama local
"""
import requests

try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        models = data.get("models", [])
        print(f"Modelos: {len(models)}")
        for m in models:
            print(f"  - {m.get('name', 'desconhecido')}")
except Exception as e:
    print(f"Erro: {e}")