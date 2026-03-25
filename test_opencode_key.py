#!/usr/bin/env python3
"""
Testar chave API do Opencode Zen
"""
import os
import sys
import requests

def test_opencode_api(api_key, model="big-pickle"):
    """Testar se a API do Opencode Zen está acessível"""
    url = "https://opencode.ai/zen/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello, test connection"}],
        "max_tokens": 10
    }
    
    print(f"Testando modelo: {model}")
    print(f"Chave: {api_key[:20]}...")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("[OK] Conexão bem-sucedida!")
            data = response.json()
            print(f"Resposta: {data.get('choices', [{}])[0].get('message', {}).get('content', 'Sem conteúdo')}")
            return True
        else:
            print(f"[ERRO] Erro: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERRO] Exceção: {e}")
        return False

if __name__ == "__main__":
    # Chave fornecida pelo usuário
    api_key = "sk-9tLO5NcQkCrG8WG6ZfVWckcX0aMPRDou4xNYT4z2QLRtbTIptEqZXCBuxIuWGgDD"
    
    print("=== Teste da Chave API Opencode Zen ===\n")
    
    # Testar diferentes modelos
    models = ["big-pickle", "mimo-v2-pro-free", "mimo-v2-omni-free"]
    
    for model in models:
        print(f"\n--- Testando {model} ---")
        success = test_opencode_api(api_key, model)
        if success:
            print(f"[OK] Modelo {model} disponível")
        else:
            print(f"[ERRO] Modelo {model} indisponível")
    
    print("\n=== Configuração ===")
    if any(test_opencode_api(api_key, m) for m in models):
        print("[OK] Pelo menos um modelo está acessível")
        print("\nConfigure o PageIndex com:")
        print(f"  export OPENCODE_API_KEY={api_key}")
        print("  python config_pageindex_opencode.py")
    else:
        print("[ERRO] Nenhum modelo acessível. Verifique a chave.")