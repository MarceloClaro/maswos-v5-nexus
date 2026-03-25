#!/usr/bin/env python3
"""
Verificar se o setup do PageIndex com Ollama está correto
"""
import sys
import subprocess
import requests

def check_ollama():
    """Verificar se Ollama está instalado e rodando"""
    try:
        # Verificar instalação
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print("[ERRO] Ollama não instalado")
            return False
        print(f"[OK] Ollama instalado: {result.stdout.strip()}")
        
        # Verificar se servidor está rodando
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                print("[OK] Servidor Ollama está rodando")
                models = response.json().get("models", [])
                print(f"   Modelos disponíveis: {len(models)}")
                for m in models:
                    print(f"   - {m.get('name', 'desconhecido')}")
                return True
            else:
                print("[AVISO]  Servidor Ollama não responde")
                return False
        except:
            print("[AVISO]  Servidor Ollama não está rodando")
            print("   Inicie com: ollama serve")
            return False
            
    except Exception as e:
        print(f"[ERRO] Erro ao verificar Ollama: {e}")
        return False

def check_dependencies():
    """Verificar dependências Python"""
    required = ["litellm", "pymupdf", "requests"]
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
            print(f"[OK] {pkg} instalado")
        except ImportError:
            print(f"[ERRO] {pkg} não instalado")
            missing.append(pkg)
    
    if missing:
        print(f"\n[AVISO]  Instale dependências: pip install {' '.join(missing)}")
        return False
    return True

def check_model(model="phi3:3.8b"):
    """Verificar se modelo está disponível"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = [m.get("name", "") for m in response.json().get("models", [])]
            if model in models:
                print(f"[OK] Modelo {model} disponível")
                return True
            else:
                print(f"[AVISO]  Modelo {model} não encontrado")
                print(f"   Baixe com: ollama pull {model}")
                return False
    except:
        print("[ERRO] Não foi possível verificar modelos")
        return False

def check_config():
    """Verificar configuração do PageIndex"""
    try:
        import yaml
        with open("PageIndex/pageindex/config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        model = config.get("model", "")
        if "ollama/" in model:
            print(f"[OK] Configuração PageIndex OK")
            print(f"   Modelo configurado: {model}")
            return True
        else:
            print(f"[AVISO]  Modelo não é Ollama: {model}")
            return False
    except Exception as e:
        print(f"[ERRO] Erro ao ler configuração: {e}")
        return False

def main():
    print("=== Verificação do Setup PageIndex + Ollama ===\n")
    
    ollama_ok = check_ollama()
    deps_ok = check_dependencies()
    config_ok = check_config()
    
    if ollama_ok and deps_ok and config_ok:
        print("\n[SUCESSO] Tudo configurado corretamente!")
        print("\nPara processar um PDF:")
        print("  python run_pageindex_local.py documento.pdf")
        print("\nOu usar o PageIndex diretamente:")
        print("  cd PageIndex && python run_pageindex.py --pdf_path documento.pdf")
    else:
        print("\n[ERRO] Alguns problemas encontrados")
        print("\nPassos para corrigir:")
        print("1. Instalar Ollama: https://ollama.ai/download")
        print("2. Baixar modelo: ollama pull phi3:3.8b")
        print("3. Instalar dependências: pip install -r PageIndex/requirements.txt")
        print("4. Verificar config.yaml no diretório PageIndex/pageindex/")

if __name__ == "__main__":
    main()