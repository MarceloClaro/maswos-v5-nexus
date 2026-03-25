#!/usr/bin/env python3
"""
Script de Instalação de Dependências para MCP Academic Transform - CPU
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Executa comando de instalação"""
    print("\n" + "="*60)
    print(f"[INSTALANDO] {description}")
    print("="*60)
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print("[OK] Concluído com sucesso!")
        if result.stdout:
            print(f"Output: {result.stdout[:500]}")
        return True
    except subprocess.CalledProcessError as e:
        print("[ERRO] Erro ao executar comando")
        print(f"Erro: {e.stderr[:500]}")
        return False

def main():
    print("="*60)
    print("INSTALACAO CPU-OPTIMIZED - MCP ACADEMIC TRANSFORM")
    print("="*60)
    print(f"Python: {sys.version}")
    print(f"Diretorio: {os.getcwd()}")
    
    # Lista de pacotes para instalar
    installations = [
        # 1. PyTorch para CPU (sem CUDA)
        (
            "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu",
            "Instalando PyTorch para CPU (versao sem GPU)"
        ),
        
        # 2. Transformers e dependências
        (
            "pip install transformers[cpu] accelerate",
            "Instalando Transformers e Accelerate"
        ),
        
        # 3. Utilitários de sistema
        (
            "pip install psutil",
            "Instalando psutil para monitoramento"
        ),
        
        # 4. GeoPandas para geoprocessamento
        (
            "pip install geopandas shapely fiona pyproj",
            "Instalando GeoPandas para geoprocessamento"
        ),
        
        # 5. Visualização
        (
            "pip install matplotlib seaborn folium contextily",
            "Instalando bibliotecas de visualizacao"
        ),
        
        # 6. Processamento de dados
        (
            "pip install pandas numpy scipy",
            "Instalando pandas, numpy e scipy"
        ),
        
        # 7. Web scraping (para coleta de dados)
        (
            "pip install requests beautifulsoup4 lxml",
            "Instalando bibliotecas de web scraping"
        ),
        
        # 8. Processamento de texto
        (
            "pip install nltk",
            "Instalando NLTK"
        ),
        
        # 9. Formatação de documentos
        (
            "pip install python-docx openpyxl",
            "Instalando bibliotecas para documentos"
        ),
        
        # 10. HTTP e APIs
        (
            "pip install aiohttp httpx",
            "Instalando bibliotecas HTTP assincronas"
        ),
    ]
    
    # Executa instalações
    success_count = 0
    fail_count = 0
    
    for command, description in installations:
        if run_command(command, description):
            success_count += 1
        else:
            fail_count += 1
            print("[INFO] Continuando com proximas instalacoes...")
    
    # Resumo final
    print("\n" + "="*60)
    print("RESUMO DA INSTALACAO")
    print("="*60)
    print(f"[SUCESSO] Instalacoes bem-sucedidas: {success_count}")
    print(f"[FALHA] Instalacoes com erro: {fail_count}")
    print(f"[INFO] Total de pacotes: {len(installations)}")
    
    # Verifica instalações principais
    print("\n[VERIFICANDO] Verificando instalacoes principais...")
    
    packages_to_check = [
        "torch",
        "transformers",
        "psutil",
        "geopandas",
        "matplotlib",
        "pandas",
        "numpy",
        "requests"
    ]
    
    for package in packages_to_check:
        try:
            __import__(package)
            print(f"[OK] {package}: Instalado")
        except ImportError:
            print(f"[FALTA] {package}: NAO INSTALADO")
    
    print("\n" + "="*60)
    print("[FINALIZADO] INSTALACAO CONCLUIDA!")
    print("="*60)
    print("\nPara testar a instalacao, execute:")
    print("  python -c \"import torch, transformers; print('Instalacao OK')\"")
    print("\nPara executar o pipeline CPU-optimized:")
    print("  python mcp_cpu_optimized.py")
    
    return success_count, fail_count

if __name__ == "__main__":
    main()