#!/usr/bin/env python3
"""
Configurar PageIndex para usar Opencode Zen com MiMo V2 Omni Free
"""
import os
import yaml
from pathlib import Path

def load_env_file():
    """Carregar variáveis de ambiente do arquivo .env"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def configure_pageindex_mimo():
    """Configurar PageIndex para MiMo V2 Omni Free"""
    
    # Carregar variáveis de ambiente
    load_env_file()
    
    # Chave API (já no .env)
    api_key = os.getenv("OPENCODE_API_KEY")
    if not api_key:
        print("Erro: OPENCODE_API_KEY não encontrada no .env")
        return
    
    model = "mimo-v2-omni-free"
    
    # Configurar PageIndex
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
    
    config_path = Path("PageIndex/pageindex/config.yaml")
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"[OK] PageIndex configurado para modelo: {model}")
    
    # Configurar litellm
    litellm_config = {
        "model_list": [
            {
                "model_name": model,
                "litellm_params": {
                    "model": f"custom/{model}",
                    "api_key": api_key,
                    "api_base": "https://opencode.ai/zen/v1"
                }
            }
        ],
        "routing_strategy": "lowest-cost"
    }
    
    litellm_path = Path("PageIndex/litellm_config.yaml")
    with open(litellm_path, 'w') as f:
        yaml.dump(litellm_config, f, default_flow_style=False)
    print(f"[OK] litellm configurado para Opencode Zen")
    
    # Configurar variáveis de ambiente
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = "https://opencode.ai/zen/v1"
    os.environ["LITELLM_MODEL"] = model
    
    print("\n[OK] Configuração concluída!")
    print(f"Modelo: {model}")
    print(f"API Base: https://opencode.ai/zen/v1")
    print("\nPara testar:")
    print(f"  python run_pageindex_opencode.py PageIndex/tests/pdfs/four-lectures.pdf {model}")

if __name__ == "__main__":
    configure_pageindex_mimo()