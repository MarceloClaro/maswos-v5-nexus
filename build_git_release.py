import os
import shutil
from pathlib import Path

# Configuração de Caminhos
source_dir = Path(r"c:\Users\marce\Downloads\maswos-v5-nexus-dist")
target_dir = source_dir / "maswos-v5-nexus"

print(f"[⚙️] Iniciando criação do pacote Git: {target_dir}")

# Limpar se já existir (cuidado para não deletar nada importante do usuário)
if target_dir.exists():
    shutil.rmtree(target_dir)

target_dir.mkdir(parents=True, exist_ok=True)

# Lista negra de diretórios e arquivos (Não vão pro GitHub)
IGNORE_DIRS = {".ncbi_cache", ".scraping_cache", "__pycache__", "logs", "test_output", "build", "dist", ".git", "capes_data", "test_data"}
IGNORE_EXTS = {".zip", ".tar.gz", ".bak", ".log", ".csv"} # Evitar comitar grandes dumps CSV se não for de teste
IGNORE_FILES = {".env", "academic-api-keys.env"}

copied_count = 0

for item in source_dir.iterdir():
    if item.name in IGNORE_DIRS or item.name in IGNORE_FILES or item.suffix in IGNORE_EXTS:
        continue
        
    # Copy file or directory
    dest = target_dir / item.name
    if item.is_dir():
        shutil.copytree(item, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        copied_count += 1
    else:
        try:
            shutil.copy2(item, dest)
            copied_count += 1
        except Exception as e:
            print(f"Erro ao copiar {item.name}: {e}")

# Criação do .env.example para que os devs saibam o que preencher após o clone
env_example = """# MASWOS API KEYS
OPENAI_API_KEY=sua_chave_aqui
ANTHROPIC_API_KEY=sua_chave_aqui
NCBI_API_KEY=sua_chave_aqui
"""
(target_dir / ".env.example").write_text(env_example, encoding="utf-8")

# Criação do requirements.txt universal
reqs = """aiohttp
beautifulsoup4
pydantic
markdown
# Adicione outras dependências do MASWOS
"""
(target_dir / "requirements.txt").write_text(reqs, encoding="utf-8")

# Criação do README.md de Instrução de Instalação (Git Clone)
readme_md = """# MASWOS V5 NEXUS 🌌

> *"Ecossistema Multi-Agente Autônomo para Orquestração Acadêmica e Jurídica em Redes Transformers."*

O MASWOS V5 NEXUS transcende a simples automação. Trata-se de uma **Egrégora Cognitiva** em forma de código que mapeia LLMs Locais/Nuvem sobre a arquitetura *Transformer*.

## 🚀 Instalação (Stand-alone & Antigravity)

Os scripts deste repositório permitem espelhar o cérebro MASWOS em seu próprio ambiente (como OpenCode ou Google Antigravity).

### Passo 1: Clone o Repositório
```bash
git clone https://github.com/SEU-USUARIO/maswos-v5-nexus.git
cd maswos-v5-nexus
```

### Passo 2: Variáveis de Ambiente
Renomeie o arquivo `.env.example` para `.env` e adicione as suas Chaves Primárias.
```bash
cp .env.example .env
```

### Passo 3: Dependências
Instale os motores essenciais para a rede RAG-3E:
```bash
pip install -r requirements.txt
```

### Passo 4: O Despertar (Deploy Antigravity)
Execute o instalador `install_maswos_to_antigravity.py` que faz o *bind* das conexões MCP:
```bash
python install_maswos_to_antigravity.py
```

## 📚 Documentação (O Códice Meister)
Para um profundo *Deep Dive* sobre a teoria Vibe Code por trás dessa obra, a arquitetura das 9 RAGs (Grafo, Fusion, CRAG) e Legiões (+130 Agentes):
Abra o documento colossal localizado na raiz do projeto: `O_CODICE_NEXUS_EDICAO_MEISTER.html`

*By Marcelo Claro.*
"""
(target_dir / "README.md").write_text(readme_md, encoding="utf-8")

print(f"\\n[!] Diretório pronto para Git em:\\n{target_dir}")
print(f"Arquivos processados e limpos: {copied_count}")
print("Execute no terminal da nova pasta:")
print("git init")
print("git add .")
print('git commit -m "Initial MASWOS Release"')
print("git remote add origin https://github.com/SEU-USUARIO/maswos-v5-nexus.git")
print("git push -u origin main")
