#!/usr/bin/env python3
"""
PageIndex com Ollama Local - Script de Execução Unificado
"""
import os
import sys
import subprocess
import time
import json
import requests
from pathlib import Path

class PageIndexLocal:
    def __init__(self, model="phi3:3.8b"):
        self.model = model
        self.ollama_port = 11434
        self.ollama_url = f"http://localhost:{self.ollama_port}"
        
    def is_ollama_running(self):
        """Verificar se o servidor Ollama está rodando"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start_ollama(self):
        """Iniciar servidor Ollama"""
        if self.is_ollama_running():
            print("[OK] Ollama já está rodando")
            return True
        
        print("Iniciando servidor Ollama...")
        try:
            # Windows
            if sys.platform == "win32":
                # Iniciar em background no Windows
                subprocess.Popen(["ollama", "serve"], 
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Linux/macOS
                subprocess.Popen(["ollama", "serve"],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            
            # Aguardar inicialização
            for i in range(10):
                time.sleep(1)
                if self.is_ollama_running():
                    print("[OK] Ollama iniciado com sucesso")
                    return True
                print(f"  Aguardando... {i+1}/10")
            
            print("[ERRO] Timeout ao iniciar Ollama")
            return False
            
        except Exception as e:
            print(f"[ERRO] Erro ao iniciar Ollama: {e}")
            return False
    
    def check_model(self):
        """Verificar se o modelo está disponível"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                return self.model in model_names
            return False
        except:
            return False
    
    def download_model(self):
        """Baixar modelo se não existir"""
        if self.check_model():
            print(f"[OK] Modelo {self.model} já está disponível")
            return True
        
        print(f"📥 Baixando modelo {self.model}...")
        try:
            # Usar comando ollama pull
            result = subprocess.run(["ollama", "pull", self.model],
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"[OK] Modelo {self.model} baixado com sucesso")
                return True
            else:
                print(f"[ERRO] Erro ao baixar modelo: {result.stderr}")
                return False
        except Exception as e:
            print(f"[ERRO] Erro: {e}")
            return False
    
    def process_pdf(self, pdf_path, output_dir="results"):
        """Processar PDF com PageIndex"""
        
        # Verificar se o PDF existe
        if not os.path.exists(pdf_path):
            print(f"[ERRO] PDF não encontrado: {pdf_path}")
            return None
        
        # Verificar se Ollama está rodando
        if not self.is_ollama_running():
            if not self.start_ollama():
                return None
        
        # Verificar se o modelo está disponível
        if not self.check_model():
            if not self.download_model():
                return None
        
        # Configurar PageIndex
        sys.path.insert(0, 'PageIndex')
        try:
            from pageindex import page_index_main
            from pageindex.utils import ConfigLoader
            
            # Configurações otimizadas para CPU
            config = {
                "model": f"ollama/{self.model}",
                "toc_check_page_num": 15,
                "max_page_num_each_node": 8,
                "max_token_num_each_node": 4000
            }
            
            print(f"[DOC] Processando: {pdf_path}")
            print(f"[AI] Modelo: {self.model}")
            print(f"[CFG]  Configuração: {config}")
            
            # Executar PageIndex
            opt = ConfigLoader().load(config)
            result = page_index_main(pdf_path, opt)
            
            # Salvar resultados
            os.makedirs(output_dir, exist_ok=True)
            pdf_name = Path(pdf_path).stem
            output_file = os.path.join(output_dir, f"{pdf_name}_structure.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n[OK] Processamento concluído!")
            print(f"[INFO] Nós encontrados: {len(result.get('nodes', []))}")
            print(f"[INFO] Total de tokens: {result.get('total_tokens', 0)}")
            print(f"[INFO] Resultado salvo em: {output_file}")
            
            return result
            
        except Exception as e:
            print(f"[ERRO] Erro no processamento: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    print("=== PageIndex com Ollama Local (Gratuito) ===\n")
    
    if len(sys.argv) < 2:
        print("Uso: python run_pageindex_local.py <caminho_do_pdf> [modelo]")
        print("\nModelos disponíveis:")
        print("  phi3:3.8b    - Recomendado (4GB RAM)")
        print("  gemma3:1b    - Leve (1GB RAM)")
        print("  gemma3:4b    - Médio (4GB RAM)")
        print("  qwen2.5-coder:7b - Avançado (5GB RAM)")
        print("\nExemplo:")
        print("  python run_pageindex_local.py documento.pdf phi3:3.8b")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "phi3:3.8b"
    
    processor = PageIndexLocal(model=model)
    result = processor.process_pdf(pdf_path)
    
    if result:
        # Mostrar estatísticas rápidas
        nodes = result.get("nodes", [])
        if nodes:
            print("\n[LIST] Primeiros 3 nós:")
            for i, node in enumerate(nodes[:3]):
                title = node.get("title", "Sem título")
                summary = node.get("summary", "")[:50]
                print(f"  {i+1}. {title}")
                if summary:
                    print(f"     {summary}...")

if __name__ == "__main__":
    main()