<div align="center">
  <img src="https://via.placeholder.com/800x200/0f0f15/FF3366?text=MASWOS+V5+NEXUS++|++VIBE+CODE+EDITION" alt="Header RPG MASWOS">
  <h1 style="color: #FF3366; font-family: 'Courier New', monospace; text-shadow: 0px 0px 10px rgba(255, 51, 102, 0.8);">
    O CÓDICE NEXUS: DEPLOY AUTÔNOMO
  </h1>
  <p style="color: #A0A0B0; font-size: 1.2em;">
    <em>Autor: Marcelo Claro</em>
  </p>
</div>

<br>

> <span style="color: #FF3366; font-weight: bold;">[!] AVISO DO SISTEMA</span>  
> *Este documento utiliza princípios de neurociência cognitiva. A cor <span style="color: #FF3366">Vermelho Carmesim (#FF3366)</span> atuará como âncora de dopamina para pontos críticos de execução (scripts e deploys), focando sua atenção como as interfaces de combate em RPGs modernos. O fundo mental é <span style="color: #1A1A24">Deep Dark</span>, reduzindo a fadiga visual.*

---

## 🎒 INVENTÁRIO (PRÉ-REQUISITOS)

Antes de iniciarmos a "Quest" de instalação do **MASWOS V5 NEXUS** no Antigravity e no OpenCode, verifique seu inventário de desenvolvedor:

- [x] **Antigravity Engine**: Ativo e configurado no seu diretório `~/.gemini/antigravity`.
- [x] **OpenCode IDE**: Instalado e rodando localmente.
- [x] **Sistema Operacional**: Windows, Linux ou macOS (A magia "Vibe Code" adapta-se a todos).
- [x] **Python 3.10+**: O mana vital do ecossistema.

---

## 🗺️ MAPA DA QUEST: ARQUITETURA TRANSFORMER

O ecossistema MASWOS V5 NEXUS não é apenas um software, é uma **Rede Transformer de Agentes**. Quando dizemos "Tudo automático", significa que vamos injetar configurações nos cérebros do Antigravity e do OpenCode de uma só vez, conectando:

1. <span style="color: #FF3366">Encoder Layer</span>: Seus Agentes Interpretadores (RAGs, Indexadores, Analyzers).
2. <span style="color: #FF3366">Decoder Layer</span>: Seus Roteadores e Construtores de Resposta (Orchestrators, Skills).
3. <span style="color: #FF3366">Attention Mechanism</span>: Os MCPs Servers (A mágica que vincula tudo).

---

<br>

<h2 style="color: #FF3366; border-bottom: 2px solid #FF3366;">🔥 LEVEL 1: O RITUAL DE INVOCAÇÃO (AUTO-DEPLOY NO ANTIGRAVITY)</h2>

Você não vai copiar arquivos manualmente. Nós vamos rodar o feitiço de integração que pega todo o ecossistema e funde com o núcleo do Antigravity.

### 📜 Objetivo da Quests:
Integrar MCPs, Skills, Agentes, RAGs e Arquivos .env no diretório nativo do Antigravity.

### ⚔️ Ação (Execute no Terminal):

```python
# Crie um arquivo chamado 'deploy_nexus.py' na raiz do seu projeto e rode: python deploy_nexus.py

import os, json, shutil
from pathlib import Path

print("\n[+] INICIANDO INFUSÃO DO NEXUS NO ANTIGRAVITY...\n")

# 1. Definindo o portal (Path do Antigravity)
ag_path = Path.home() / ".gemini" / "antigravity"
ag_path.mkdir(parents=True, exist_ok=True)

# 2. Fundindo as Almas dos MCPs (mcp_servers_config.json -> mcp_config.json)
nexus_mcp_file = "mcp_servers_config.json"
ag_mcp_file = ag_path / "mcp_config.json"

if Path(nexus_mcp_file).exists():
    with open(nexus_mcp_file, "r") as f:
        nexus_mcp = json.load(f)
    
    ag_mcp = json.loads(ag_mcp_file.read_text()) if ag_mcp_file.exists() else {"mcpServers": {}}
    
    for name, config in nexus_mcp.get("mcpServers", {}).items():
        ag_mcp.setdefault("mcpServers", {})[name] = config
        print(f"  [MCP Linkado] -> {name} (Nível máximo de afinidade)")
        
    ag_mcp_file.write_text(json.dumps(ag_mcp, indent=2))

# 3. Transferência de Atributos (Skills & Agentes)
ag_skills, ag_maswos = ag_path / "skills", ag_path / "maswos"
ag_maswos.mkdir(exist_ok=True)

local_skills = Path(".agent/skills")
if local_skills.exists():
    for skill in local_skills.iterdir():
        if skill.is_dir():
            shutil.copytree(skill, ag_skills / skill.name, dirs_exist_ok=True)
            print(f"  [Skill Adquirida] -> {skill.name}")

# 4. Copiando a Magia (RAGs, Templates, Python Core)
print("\n[+] TRANSFERINDO NÚCLEOS TRANSFORMER...")
for item in Path(".").iterdir():
    if item.suffix in [".py", ".json", ".md", ".env"] or item.name in [".env", "rag", "mcp-tese-completa"]:
        if item.is_file():
            shutil.copy2(item, ag_maswos / item.name)
        elif item.is_dir():
            shutil.copytree(item, ag_maswos / item.name, dirs_exist_ok=True)

print("\n[✔] QUEST CONCLUÍDA! LEVEL UP! ANTIGRAVITY AGORA É UM NEXUS A1.")
```

> **Resultado (XP Ganha):** O Antigravity agora possui as ferramentas para invocar 60 agentes jurídicos e 55 acadêmicos autonomamente.

---

<br>

<h2 style="color: #FF3366; border-bottom: 2px solid #FF3366;">🔥 LEVEL 2: SINCRONIZANDO A MATRIZ COM O OPENCODE</h2>

Se o Antigravity é o cérebro, o **OpenCode** é o seu *HUD (Heads-Up Display)* de jogador. Precisamos garantir que o OpenCode esteja visualizando os mesmos MCPs (Model Context Protocol).

### 📜 Objetivo da Quest:
Habilitar a arquitetura MCP no OpenCode lendo o motor central que acabamos de configurar.

### ⚔️ Ação (Execute no Terminal via Vibe Code):

Abra o seu OpenCode, e na raiz do MASWOS (pasta `maswos-v5-nexus-dist`), vamos subir uma configuração automatizada pro `opencode.json`:

```bash
# Rode este comando mágico no powershell do OpenCode
$OpenCodeConfig = "$env:APPDATA\OpenCode\User\globalStorage\opencode.mcp\settings.json"

# Verifica e injeta as regras do MASWOS
If (!(Test-Path $openCodeConfig)) { New-Item -ItemType File -Force -Path $OpenCodeConfig }
Copy-Item ".\mcp_servers_config.json" -Destination $OpenCodeConfig -Force

Write-Host "[!] MATRIZ OPENCODE ESTABELECIDA. O SANGUE DO NEXUS FLUI NA IDE." -ForegroundColor Red
```

---

<br>

<h2 style="color: #FF3366; border-bottom: 2px solid #FF3366;">🔥 LEVEL 3: ENGRENANDO A REDE TRANSFORMER (O TESTE DE FOGO)</h2>

A rede precisa de um sinal elétrico para ligar. Na arquitetura Transformer que construímos, o `mcp_sync.py` atua como o **Mecanismo de Atenção (Attention Mechanism)**, alinhando os encoders e decoders entre o sistema de arquivos local e a matriz do Antigravity.

### ⚔️ Ação (Ritual Final):

```bash
# Execute o sincronizador dimensional
python mcp_sync.py
```

Você verá a interface estilo RPG do terminal confirmando que os nós da rede foram alinhados. 

> <span style="color: #FF3366">**BUFF ATIVADO:**</span> *Cross-MCP Coordination*. Seu sistema agora consegue buscar dados no arXiv (Agente A2), validá-los pelo método Qualis A1 (Validador V05) e construir o artigo automaticamente, guiado pelas SKILLS que instalamos no Passo 1!

---

<br>

<h2 style="color: #FF3366; border-bottom: 2px solid #FF3366;">🕹️ GAMEPLAY: COMO USAR NO DIA A DIA (TUTORIAL FINAL)</h2>

Tudo está automatizado. Para jogar este jogo acadêmico/jurídico em *"God Mode"*, interaja diretamente com o Antigravity ou com o OpenCode com gatilhos curtos (Prompts de RPG).

**No Chat do Antigravity ou OpenCode, digite o feitiço de evocação:**

> *"@app-builder ou @criador-de-artigo-v2, inicie a produção de uma Tese A1 sobre Inteligência Artificial. Utilize o ecossistema Nexus que está em ~/.gemini/antigravity/maswos"*

### 🧠 O Que Acontece "Por Baixo dos Panos" (Visão Além do Véu):
1. **Roteamento de Intenção:** O Antigravity detecta o gatilho.
2. **MCP Summoning:** Ele aciona os servidores MCP local (`maswos-rag`, `pageindex`, etc).
3. **Transformer Flow:** O `orchestrator_unified` aloca a tarefa dividindo-a em Encoder (Pesquisa), Processamento Paralelo (Análise de dados Gov/Acadêmica) e Decoder (Redação ABNT).
4. **Output Final:** Um artefato gerado na sua pasta `/output`, perfeitamente referenciado, livre de alucinações.

---

<br>

<div align="center" style="border: 2px solid #33FF99; padding: 20px; border-radius: 10px; background-color: #0f0f15;">
  <h3 style="color: #33FF99; margin-top: 0;">🏆 CONQUISTA DESBLOQUEADA: NEXUS ARCHITECT</h3>
  <p style="color: #E0E0E0;">Você concluiu o Codex do MASWOS V5. O poder computacional autônomo está 100% estabelecido na sua máquina. A era da criação assistida acabou. Bem-vindo à era da Criação Autônoma Escalonável.</p>
</div>

<br>

<div align="right">
  <p><i>"O limite do conhecimento é definido pela capacidade da sua orquestração."</i><br>
  <b>— Marcelo Claro</b></p>
</div>


<br>

<h2 style="color: #FF3366; border-bottom: 2px solid #FF3366;">🔮 LEVEL 4: O DESPERTAR DOS ORÁCULOS (DOMINANDO OS RAGS)</h2>

> <span style="color: #FF3366">*Aviso Neural:*</span> O sistema MASWOS V5 não apenas Lê dados, ele **Pensa** sobre eles. Você possui 9 Estratégias de Recuperação de Informação (RAGs) implementadas.

Se o Antigravity é sua central, os **RAGs** são os feitiços de clarividência. 

### 📜 Objetivo da Quest:
Mapear e acionar a biblioteca de RAGs (Vanilla, Memory, Agentic, Graph, Hybrid, CRAG, Adaptive, Fusion, HyDE).

### 📖 O Códice de Invocações RAG (Via Prompt Terminal):
Ao interagir com o modelo (seja pelo terminal OpenCode ou chat Antigravity), você pode **forçar** uma postura de RAG específica baseada na complexidade do inimigo (a pesquisa).

* **Spell 1 (GraphRAG + PageIndex):** Para teses colossais de +100 páginas.  
  👉 *"@maswos-rag, ative a estratégia [GraphRAG]. Mapeie as conexões de entidades sobre [Seu Tema] usando o PageIndex sem vetorização."*
* **Spell 2 (CRAG - Corrective RAG):** Quando a banca exige fontes incontestáveis.  
  👉 *"@maswos-rag, ative o [CRAG]. Valide absolutamente cada paper através das fontes NCBI/ArXiv antes de gerar o parágrafo da metodologia."*
* **Spell 3 (RAG-Fusion):** Para pesquisas multidisciplinares.  
  👉 *"@maswos-rag, use [Fusion]. Mescle dados do IBGE, DATASUS e PubMed e pondere a relevância pelo algoritmo RRF."*

---

<br>

<h2 style="color: #FF3366; border-bottom: 2px solid #FF3366;">⚔️ LEVEL 5: O EXÉRCITO MULTIAGENTE (130+ UNIDADES)</h2>

Você agora controla duas legiões. Se você usou o macro do `deploy_nexus.py` no Level 1 de forma correta, sua aba de MCPs no OpenCode ou no painel do Antigravity agora brilha listando as corporações de agentes.

### 🏛️ Legião Acadêmica (55 Agentes):
- **Batedores (Scrapers):** Extraem dados primários de 14 portais (CAPES, Arxiv, SemanticScholar).
- **Alquimistas (Data Scientists):** Limpam bases do IBGE e WorldBank, transformando CSVs em narrativas.
- **Formadores (ABNT Makers):** Formatam até a alma do texto (Margens, Citações e Layout).

### ⚖️ Legião Jurídica (60 Agentes):
- **Táticos Processuais:** Peticionamento Acelerado, Consultas de Jurisprudência STF/STJ.
- **Auditores de Lei:** Agentes que não escrevem, apenas **Julgam** o texto dos outros agentes, destruindo alucinações.

### 🕹️ Como Invocar o Enxame (Comando Vibe Code):
No seu terminal ou prompt de intenção, você invoca o `orchestrator_unified`.

```bash
# Copie e cole no Antigravity/OpenCode
@orchestrator_unified, inicie a Legião Acadêmica.
[Missão]: Escrever um paper A1 sobre "Educação como Mecanismo de Fuga da Armadilha da Renda Média".
[Parâmetros]: Execute a Fase 1 (Diagnóstico) e pare para minha aprovação.
```
> <span style="color: #00fa9a">**DICA VIBE CODE:**</span> Sempre mande o orquestrador pausar após a Fase 1. Isso permite que você ajuste a "Build" (A estrutura da tese) antes dos agentes gastarem mana (tokens) gerando 110 páginas!

---

<br>

<h2 style="color: #FF3366; border-bottom: 2px solid #FF3366;">👑 LEVEL 6: O MODO DEUS (PIPELINE QUALIS A1)</h2>

Chegamos ao End-Game. Para automatizar um livro ou uma tese completa, nós não chamamos agentes separados. Nós disparamos o **Pipeline Automatizado Transformer**.

### 📜 O Feitiço Master (Auto-Escrita de Tese):
Crie um arquivo chamado `run_thesis_god_mode.py` no diretório raiz do Antigravity/MASWOS e execute-o.

```python
# run_thesis_god_mode.py
import asyncio
from maswos_core.orchestrator import Orchestrator

async def cast_qualis_a1():
    print("\n[!] INICIANDO PIPELINE QUALIS A1 - MODO DEUS...\n")
    
    # 1. Instanciando o Cérebro Transformer
    nexus = Orchestrator(mode="autonomous", tier="A1")
    
    # 2. Injetando a Intenção
    missao = {
        "tema": "Análise Comparativa de Sete Países (1960-2023)",
        "tamanho": "110_paginas",
        "auditoria": "strict_7_layers",
        "fontes": ["WorldBank", "IBGE", "Scopus"]
    }
    
    # 3. Disparo da Rede (Fire and Forget)
    print("[⚡] Conectando Layers de Attention. Iniciando Batedores...")
    artefato = await nexus.execute_pipeline('academic_research', missao)
    
    with open("output/TESE_FINAL_A1_NEXUS.md", "w", encoding="utf-8") as f:
        f.write(artefato.content)
        
    print("\n[🏆] TESE GERADA E AUDITADA COM SUCESSO. DROP: TESE_FINAL_A1_NEXUS.md")

if __name__ == "__main__":
    asyncio.run(cast_qualis_a1())
```

Execute isso no seu terminal e levante-se para tomar um café. O painel da IDE será inundado com registros de logs cibernéticos indicando cada agente fazendo RAG, cruzando dados, redigindo, refatorando e aplicando as Normas ABNT automaticamente.

---

<br>

<h2 style="color: #FF3366; border-bottom: 2px solid #FF3366;">🧪 LEVEL 7: POÇÕES DE CURA (TROUBLESHOOTING)</h2>

Todo jogo tem seus *Bugs/Glitches*. Se a rede Transformer falhar durante o deploy automatizado, consulte seu inventário de poções:

<table style="width:100%; text-align: left; background-color: #1A1A24; border: 1px solid #FF3366; border-radius: 8px; color: #DDD; padding: 10px;">
  <tr>
    <th style="color: #FF3366; padding-bottom: 10px;">👾 O Boss (Erro)</th>
    <th style="color: #FF3366; padding-bottom: 10px;">🧪 A Poção (Solução Vibe Code)</th>
  </tr>
  <tr>
    <td style="padding: 10px;"><b>MCP Server não conecta</b> no OpenCode/Antigravity</td>
    <td style="padding: 10px;">Rode <code>python fix_mcp_issues.py</code> na raiz. Verifique se as portas 3001 a 3003 estão livres.</td>
  </tr>
  <tr>
    <td style="padding: 10px;"><b>"Agent Not Found"</b> na legião Jurídica</td>
    <td style="padding: 10px;">Você pulou o <b>Level 3</b>. Rode <code>python mcp_sync.py</code> para realinhar os encoders.</td>
  </tr>
  <tr>
    <td style="padding: 10px;">Tese gera <b>referências fantasmas (Alucinações)</b></td>
    <td style="padding: 10px;">Forçe o Gate de Qualidade. No prompt adicione: <code>Set-QualityGate -Level V04_CRAG</code></td>
  </tr>
</table>

<br>

---

<div align="center" style="background-color: #0f0f15; padding: 25px; border: 1px solid #FF3366; border-radius: 8px; box-shadow: 0 0 15px rgba(255,51,102,0.4);">
  <h2 style="color: #FF3366; margin-top: 5px;">🌌 EPÍLOGO: A TRANSCENDÊNCIA DO CÓDIGO</h2>
  <p style="color: #E0E0E0; font-size: 1.1em; line-height: 1.6;">
    Você não instalou um simples programa. Você construiu uma <b>Egrégora Cognitiva</b>.<br>
    O <b>MASWOS V5 NEXUS</b> vive no cérebro da sua máquina, orquestrando conexões muito além do prompt-response padrão. Ao seguir este Códice, você transformou sua interface gráfica em uma Matrix de agência autônoma.<br><br>
    <i>Execute. Orquestre. Sublime.</i>
  </p>
  <p style="color: #888;">—— Fim do Códice NEXUS ——</p>
</div>

