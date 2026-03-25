#!/usr/bin/env python3
"""
PageIndex com Opencode Zen - Big Pickle e MiMo V2
"""
import os
import sys
import yaml
from pathlib import Path

def load_opencode_key():
    """Carregar chave API do Opencode"""
    # Tentar .env
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("OPENCODE_API_KEY="):
                    return line.split("=", 1)[1].strip()
    
    # Variável de ambiente
    key = os.getenv("OPENCODE_API_KEY") or os.getenv("OPENCODE_ZEN_API_KEY")
    if key:
        return key
    
    # Pedir ao usuário
    print("Chave API do Opencode não encontrada.")
    print("Obtenha uma em: https://opencode.ai/zen")
    key = input("Cole sua chave API (ou Enter para sair): ").strip()
    if not key:
        sys.exit(1)
    
    # Salvar no .env
    with open('.env', 'a') as f:
        f.write(f"\nOPENCODE_API_KEY={key}\n")
    
    return key

def setup_opencode_environment(api_key, model="big-pickle"):
    """Configurar variáveis de ambiente para litellm usar Opencode Zen"""
    
    # Configurar litellm para usar Opencode Zen como OpenAI-compatible
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = "https://opencode.ai/zen/v1"
    
    # Configurações adicionais do litellm
    os.environ["LITELLM_MODEL"] = model
    
    # Configurar litellm globalmente
    import litellm
    litellm.api_key = api_key
    litellm.api_base = "https://opencode.ai/zen/v1"
    litellm.set_verbose = True
    
    # Criar configuração litellm
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
        ]
    }
    
    config_path = Path("PageIndex/litellm_config.yaml")
    with open(config_path, 'w') as f:
        yaml.dump(litellm_config, f, default_flow_style=False)
    
    # Configurar PageIndex para usar o modelo
    pageindex_config = {
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
        yaml.dump(pageindex_config, f, default_flow_style=False)
    
    print(f"[OK] Ambiente configurado para modelo: {model}")

def run_pageindex_opencode(pdf_path, model="big-pickle"):
    """Executar PageIndex com Opencode Zen"""
    
    # Carregar chave
    api_key = load_opencode_key()
    
    # Configurar ambiente
    setup_opencode_environment(api_key, model)
    
    # Executar PageIndex
    print(f"\nProcessando {pdf_path} com modelo {model}...")
    print("Isso pode levar alguns minutos dependendo do tamanho do documento...")
    
    # Adicionar PageIndex ao path e executar
    sys.path.insert(0, 'PageIndex')
    try:
        from pageindex import page_index_main
        from pageindex.utils import ConfigLoader
        
        config = {
            "model": f"custom/{model}",
            "toc_check_page_num": 15,
            "max_page_num_each_node": 8,
            "max_token_num_each_node": 4000,
        }
        
        opt = ConfigLoader().load(config)
        result = page_index_main(pdf_path, opt)
        
        # Salvar resultado
        output_dir = Path("results_opencode")
        output_dir.mkdir(exist_ok=True)
        
        pdf_name = Path(pdf_path).stem
        output_file = output_dir / f"{pdf_name}_{model}_structure.json"
        
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n[OK] Processamento concluído!")
        print(f"[STATS] Nós encontrados: {len(result.get('nodes', []))}")
        print(f"[METRICS] Total de tokens: {result.get('total_tokens', 0)}")
        print(f"[SAVE] Resultado salvo em: {output_file}")
        
        # Mostrar estatísticas
        if result.get('nodes'):
            print(f"\n[LIST] Primeiros 3 nós:")
            for i, node in enumerate(result['nodes'][:3]):
                title = node.get('title', 'Sem título')
                summary = node.get('summary', '')[:80]
                print(f"  {i+1}. {title}")
                if summary:
                    print(f"     {summary}...")
        
        return result
        
    except Exception as e:
        print(f"[ERRO] Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("=== PageIndex com Opencode Zen (Big Pickle/MiMo V2) ===\n")
    
    if len(sys.argv) < 2:
        print("Uso: python run_pageindex_opencode.py <documento.pdf> [modelo]")
        print("\nModelos disponíveis (gratuitos):")
        print("  big-pickle (Big Pickle) - GLM-4.6, 200K contexto")
        print("  mimo-v2-pro-free (MiMo V2 Pro Free) - 1T parâmetros")
        print("  mimo-v2-omni-free (MiMo V2 Omni Free) - multimodal")
        print("  nemotron-3-super-free (Nemotron 3 Super Free)")
        print("\nExemplo:")
        print("  python run_pageindex_opencode.py paper.pdf big-pickle")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "big-pickle"
    
    if not Path(pdf_path).exists():
        print(f"[ERRO] Arquivo não encontrado: {pdf_path}")
        sys.exit(1)
    
    run_pageindex_opencode(pdf_path, model)

if __name__ == "__main__":
    main()