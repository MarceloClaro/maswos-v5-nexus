#!/usr/bin/env python3
"""
Configurar PageIndex para usar modelos do Opencode Zen (Big Pickle, MiMo V2)
"""
import os
import sys
import yaml
import requests
from pathlib import Path

def check_opencode_key():
    """Verificar se a chave API do Opencode está configurada"""
    key = os.getenv("OPENCODE_API_KEY") or os.getenv("OPENCODE_ZEN_API_KEY")
    if key:
        print(f"[OK] Chave OpenCode encontrada: {key[:20]}...")
        return key
    else:
        print("[ERRO] Chave API do Opencode não encontrada")
        print("Configure uma das seguintes variáveis:")
        print("  export OPENCODE_API_KEY=sua-chave")
        print("  export OPENCODE_ZEN_API_KEY=sua-chave")
        print("\nObtenha uma chave em: https://opencode.ai/zen")
        return None

def test_opencode_api(api_key, model="big-pickle"):
    """Testar se a API do Opencode Zen está acessível"""
    url = "https://opencode.ai/zen/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Teste de conexão"}],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"[OK] API Opencode Zen acessível (modelo: {model})")
            return True
        else:
            print(f"[ERRO] API Opencode Zen retornou status {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"[ERRO] Falha na conexão: {e}")
        return False

def create_opencode_config(api_key, model="big-pickle"):
    """Criar config.yaml para PageIndex com Opencode Zen"""
    
    # Configuração base
    config = {
        "model": f"custom/{model}",
        "toc_check_page_num": 15,
        "max_page_num_each_node": 8,
        "max_token_num_each_node": 4000,
        "if_add_node_id": "yes",
        "if_add_node_summary": "yes",
        "if_add_doc_description": "no",
        "if_add_node_text": "no"
    }
    
    # Configuração adicional para litellm (será salva em arquivo separado)
    litellm_config = {
        "model_list": [
            {
                "model_name": model,
                "litellm_params": {
                    "model": "custom/opencode_zen",
                    "api_key": api_key,
                    "api_base": "https://opencode.ai/zen/v1"
                }
            }
        ],
        "routing_strategy": "lowest-cost"
    }
    
    # Salvar config.yaml do PageIndex
    config_path = Path("PageIndex/pageindex/config.yaml")
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"[OK] Configuração PageIndex salva em: {config_path}")
    
    # Salvar config.yaml do litellm
    litellm_config_path = Path("PageIndex/litellm_config.yaml")
    with open(litellm_config_path, 'w') as f:
        yaml.dump(litellm_config, f, default_flow_style=False)
    print(f"[OK] Configuração litellm salva em: {litellm_config_path}")
    
    return config_path, litellm_config_path

def update_env_file(api_key):
    """Atualizar arquivo .env com a chave do Opencode"""
    env_path = Path(".env")
    env_content = ""
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            env_content = f.read()
    
    # Verificar se já existe a chave
    if "OPENCODE_API_KEY" in env_content:
        print("[AVISO] OPENCODE_API_KEY já existe no .env")
        return
    
    # Adicionar nova chave
    with open(env_path, 'a') as f:
        f.write(f"\n# OpenCode Zen API\n")
        f.write(f"OPENCODE_API_KEY={api_key}\n")
    
    print(f"[OK] Chave adicionada ao .env")

def main():
    print("=== Configuração PageIndex + Opencode Zen ===\n")
    
    # 1. Verificar chave API
    api_key = check_opencode_key()
    if not api_key:
        sys.exit(1)
    
    # 2. Escolher modelo
    print("\nModelos disponíveis no Opencode Zen (gratuitos):")
    print("  1. big-pickle (Big Pickle) - Recomendado")
    print("  2. mimo-v2-pro-free (MiMo V2 Pro Free)")
    print("  3. mimo-v2-omni-free (MiMo V2 Omni Free)")
    print("  4. nemotron-3-super-free (Nemotron 3 Super Free)")
    
    choice = input("\nEscolha um modelo (1-4) [1]: ").strip() or "1"
    
    models = {
        "1": "big-pickle",
        "2": "mimo-v2-pro-free", 
        "3": "mimo-v2-omni-free",
        "4": "nemotron-3-super-free"
    }
    
    selected_model = models.get(choice, "big-pickle")
    print(f"\nModelo selecionado: {selected_model}")
    
    # 3. Testar API
    print("\nTestando conexão com Opencode Zen...")
    if not test_opencode_api(api_key, selected_model):
        print("[AVISO] Teste de conexão falhou, mas continuando...")
    
    # 4. Criar configurações
    print("\nCriando configurações...")
    config_path, litellm_path = create_opencode_config(api_key, selected_model)
    
    # 5. Atualizar .env
    update_env_file(api_key)
    
    # 6. Instruções finais
    print("\n" + "="*50)
    print("✅ Configuração concluída!")
    print("\nPróximos passos:")
    print("1. Certifique-se de que o servidor Ollama está rodando:")
    print("   ollama serve")
    print("\n2. Execute o PageIndex com Opencode Zen:")
    print(f"   python run_pageindex_local.py documento.pdf {selected_model}")
    print("\n3. Ou use o script específico para Opencode Zen:")
    print("   python run_pageindex_opencode.py documento.pdf")
    
    print("\nNota: Os modelos do Opencode Zen são baseados em API, então")
    print("não precisam de Ollama. O script run_pageindex_local.py")
    print("funciona tanto com Ollama local quanto com APIs externas.")

if __name__ == "__main__":
    main()