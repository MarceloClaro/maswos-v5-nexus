import os

new_content = """

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
    print("\\n[!] INICIANDO PIPELINE QUALIS A1 - MODO DEUS...\\n")
    
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
        
    print("\\n[🏆] TESE GERADA E AUDITADA COM SUCESSO. DROP: TESE_FINAL_A1_NEXUS.md")

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

"""

target_file = r'c:\Users\marce\Downloads\maswos-v5-nexus-dist\LIVRO_NEXUS_VIBE_CODE_MARCELO_CLARO.md'
with open(target_file, 'a', encoding='utf-8') as f:
    f.write(new_content)
