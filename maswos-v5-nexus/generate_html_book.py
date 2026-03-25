import os

# Estrutura base do HTML com CSS para Vibe Code + Neuroscience Red
html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>O CÓDICE NEXUS: DEPLOY AUTÔNOMO (Edição Completa)</title>
    
    <!-- Fonte Monospace e Sans-Serif -->
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    
    <!-- Mermaid.js para fluxogramas automáticos -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true, theme: 'dark', themeVariables: { primaryColor: '#FF3366', edgeLabelBackground:'#0f0f15', clusterBkg: '#1A1A24'}});</script>
    
    <style>
        :root {
            --bg-color: #0f0f15;
            --text-color: #E0E0E0;
            --accent-red: #FF3366;
            --secondary-bg: #1A1A24;
            --code-bg: #050508;
            --success-color: #00fa9a;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.8;
            margin: 0;
            padding: 0;
        }
        
        .page-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        h1, h2, h3, h4 {
            font-family: 'Fira Code', monospace;
            color: var(--accent-red);
        }
        
        h1 {
            font-size: 3em;
            text-shadow: 0 0 15px rgba(255, 51, 102, 0.6);
            border-bottom: 2px solid var(--accent-red);
            padding-bottom: 20px;
            text-align: center;
        }
        
        h2 {
            font-size: 2em;
            margin-top: 60px;
            border-bottom: 1px solid rgba(255, 51, 102, 0.4);
            padding-bottom: 10px;
        }
        
        .cover {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            page-break-after: always;
        }
        
        .ascii-art {
            font-family: 'Fira Code', monospace;
            color: var(--accent-red);
            white-space: pre;
            font-size: 14px;
            line-height: 1.2;
            margin-bottom: 40px;
            text-shadow: 0 0 10px rgba(255, 51, 102, 0.4);
        }
        
        .alert-box {
            background-color: var(--secondary-bg);
            border-left: 4px solid var(--accent-red);
            padding: 20px;
            margin: 30px 0;
            border-radius: 0 8px 8px 0;
        }
        
        .tip-box {
            background-color: var(--secondary-bg);
            border-left: 4px solid var(--success-color);
            padding: 20px;
            margin: 30px 0;
            border-radius: 0 8px 8px 0;
        }
        
        pre {
            background-color: var(--code-bg);
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid #333;
            font-family: 'Fira Code', monospace;
            font-size: 0.9em;
        }
        
        code {
            font-family: 'Fira Code', monospace;
            color: #ff99aa;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 40px 0;
            background-color: var(--secondary-bg);
        }
        
        th, td {
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: left;
        }
        
        th {
            color: var(--accent-red);
            font-family: 'Fira Code', monospace;
            background-color: rgba(255, 51, 102, 0.05);
        }
        
        .diagram-container {
            background-color: var(--secondary-bg);
            padding: 30px;
            border-radius: 8px;
            margin: 40px 0;
            text-align: center;
            border: 1px dashed rgba(255, 51, 102, 0.3);
        }
        
        .page-break {
            page-break-after: always;
            margin: 100px 0;
            border-bottom: 1px dashed #333;
        }
        
        /* Tema de impressão para PDF */
        @media print {
            body {
                background-color: #fff;
                color: #000;
            }
            .page-container {
                max-width: 100%;
            }
            h1, h2, h3 {
                color: #d90429;
                text-shadow: none;
            }
            .cover {
                color: #000;
            }
            .ascii-art {
                color: #d90429;
                text-shadow: none;
            }
            pre {
                background-color: #f4f4f4;
                border: 1px solid #ccc;
                color: #333;
            }
            code {
                color: #d90429;
            }
            .alert-box, .tip-box, table, .diagram-container {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-left-width: 4px;
            }
            .diagram-container {
                filter: invert(1);
            }
        }
    </style>
</head>
<body>
    <div class="page-container">
        
        <!-- COVER -->
        <div class="cover">
            <div class="ascii-art">
███╗   ███╗ █████╗ ███████╗██╗    ██╗ ██████╗ ███████╗
████╗ ████║██╔══██╗██╔════╝██║    ██║██╔═══██╗██╔════╝
██╔████╔██║███████║███████╗██║ █╗ ██║██║   ██║███████╗
██║╚██╔╝██║██╔══██║╚════██║██║███╗██║██║   ██║╚════██║
██║ ╚═╝ ██║██║  ██║███████║╚███╔███╔╝╚██████╔╝███████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚══════╝
                                                      
N E X U S   E D I T I O N
            </div>
            <h1>O CÓDICE NEXUS</h1>
            <h2>DEPLOY AUTÔNOMO & ARQUITETURA TRANSFORMER</h2>
            <p style="font-size: 1.5em; margin-top: 50px;">O Guia Definitivo: Reprodução Universal via OpenCode e Antigravity</p>
            <p style="margin-top: 80px; color: var(--accent-red); font-family: 'Fira Code', monospace;">NÍVEL DE ACESSO: ARCHITECT</p>
            <p><strong>Autor: Marcelo Claro</strong></p>
        </div>

        <div class="page-break"></div>

        <!-- INTRO -->
        <h2>PRELÚDIO: A NEUROCIÊNCIA DO "VIBE CODE"</h2>
        <div class="alert-box">
            <strong>Aviso de Engenharia Cognitiva:</strong><br>
            Este manual foi projetado com gatilhos de dopamina visuais. O uso do vermelho (Carmesim) serve para hiper-focar sua leitura nas estruturas mais críticas do código. Se você busca implementar o ecossistema MASWOS V5 em sua máquina, não pule os blocos vermelhos.
        </div>
        
        <p>A era da configuração manual acabou. O Ecossistema MASWOS V5 NEXUS é projetado para instalação fluida através de injeções de script automatizadas em ambientes como <strong>Antigravity</strong> e <strong>OpenCode</strong>. O design que você lerá a partir de agora é desenhado em Módulos, guiando-o pelas Arquiteturas de Redes Transformers, RAGs, Swarms, e Integrações MCP Múltiplas.</p>

        <div class="page-break"></div>

        <!-- MÓDULO 1 -->
        <h2>MÓDULO 1: O MOTOR ANTIGRAVITY E A REDE TRANSFORMER</h2>
        <p>A Arquitetura Multi-Agente MASWOS opera sob o mesmo esquema dimensional que um modelo Transformer original, traduzindo as camadas do *Attention Is All You Need* para a Orquestração LLM Local.</p>
        
        <div class="diagram-container">
            <div class="mermaid">
            graph TD
                subgraph "Transformer Layer Mapping"
                    A[Input Embedding] --> B[Positional Encoding]
                    B --> C[Encoder Stack]
                    C --> D[Multi-Head Attention]
                    D --> E[Layer Normalization]
                    E --> F[Decoder Stack]
                    F --> G[Output Projection]
                end

                subgraph "MASWOS V5 Orquestração"
                    A1[Intent Parser 01] --> B1[TIER Router 02]
                    B1 --> C1[RAG-3E Coordinator 03]
                    C1 --> D1[Critic-Router 24]
                    D1 --> E1[CrossValidator 13]
                    E1 --> F1[DocumentSynthesizer 21]
                    F1 --> G1[QualityScorer 26]
                end

                A -.-> A1
                B -.-> B1
                C -.-> C1
                D -.-> D1
                E -.-> E1
                F -.-> F1
                G -.-> G1
            </div>
            <p style="margin-top: 15px; font-size: 0.85em; color: #888;">Figura 1.0 - Correlação Estrutural: Transformer Numérico vs MASWOS Orquestração</p>
        </div>

        <h3>1.1 O Script Prático de Setup</h3>
        <p>Para injetar todo este mapeamento dentro do Antigravity, precisamos apenas de um código Vibe. Ele mapeia os JSONs, cria as subpastas e engata nas portas locais de MCP.</p>

<pre><code>import os, json, shutil
from pathlib import Path

# VIBE CODE: Auto Deploy Antigravity
ag_path = Path.home() / ".gemini" / "antigravity"
ag_path.mkdir(parents=True, exist_ok=True)

# Lendo o Codex Local e Atualizando
config_source = json.loads(Path("mcp_servers_config.json").read_text())
ag_mcp = ag_path / "mcp_config.json"
current_ag = json.loads(ag_mcp.read_text()) if ag_mcp.exists() else {"mcpServers": {}}

# Injetando Servidores de RAG e Legiões
current_ag["mcpServers"].update(config_source.get("mcpServers", {}))
ag_mcp.write_text(json.dumps(current_ag, indent=2))
print("[NEXUS] Matriz Antigravity atualizada dimensionalmente.")
</code></pre>

        <div class="page-break"></div>

        <!-- MÓDULO 2 -->
        <h2>MÓDULO 2: OS ORÁCULOS RAG (RETRIEVAL-AUGMENTED GENERATION)</h2>
        <p>Ao invocar os agentes para construir sua tese, o Antigravity não pode "adivinhar" fatos. Ele usa nossa grade com 9 fluxos de recuperação da verdade. Abaixo, a Tabela de Armas RAG disponíveis.</p>

        <table>
            <thead>
                <tr>
                    <th>Gatilho (Spell)</th>
                    <th>Estrutura Arquitetural</th>
                    <th>Caso de Uso (Boss Fight)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>[VanillaRAG]</code></td>
                    <td>Busca Semântica Simples e Rápida</td>
                    <td>Verificações corriqueiras de definições e conceitos curtos na memória RAM.</td>
                </tr>
                <tr>
                    <td><code>[GraphRAG]</code></td>
                    <td>Construção de Nodos e Entidades (Sem Vetor)</td>
                    <td>Teses Críticas. Mais de 110 páginas relacionando temas complexos (ex: Armadilha da Renda Média).</td>
                </tr>
                <tr>
                    <td><code>[CRAG]</code></td>
                    <td>Corrective-RAG com dupla checagem de fontes</td>
                    <td>Quando a Banca/CNPq exige fontes 100% livres de alucinações. Usa R013 para auditar.</td>
                </tr>
                <tr>
                    <td><code>[Fusion]</code></td>
                    <td>RRF (Reciprocal Rank Fusion) multi-fontes</td>
                    <td>Cruzar IBGE + WorldBank + PubMed ao mesmo tempo para obter um viés único de análise.</td>
                </tr>
            </tbody>
        </table>

        <div class="tip-box">
            <strong>Implementação do PageIndex:</strong><br>
            A API do PageIndex substitui o Chunking tradicional. O GraphRAG do MASWOS alimenta-se dele garantindo que as árvores de raciocínio de 3 milhões de tokens não se percam pelo caminho.
        </div>

        <div class="page-break"></div>

        <!-- MÓDULO 3 -->
        <h2>MÓDULO 3: LEGIÕES - ACADÊMICA E JURÍDICA</h2>
        <p>A orquestração não chama APIs frias, ela acorda <strong>Personas e Ferramentas</strong>. A Legião A (Acadêmica) possui 55 cabeças. A Legião J (Jurídica) possui 60. E você é o Maestro.</p>

        <div class="diagram-container">
            <div class="mermaid">
            flowchart LR
                User([Usuário]) -- "@orchestrator_unified" --> Central{Orquestrador Central}
                
                Central -- Intent = Legal --> J[MASWOS-JURÍDICO]
                Central -- Intent = Academic --> A[MASWOS-ACADEMIC]
                
                subgraph J[Módulo Jurídico - 60 Agentes]
                    J1[STF Scraper]
                    J2[Peticionador]
                    J3[Revisor OAB]
                end

                subgraph A[Módulo Acadêmico - 55 Agentes]
                    A1[ArXiv/Pubmed API]
                    A2[IBGE/WorldBank CSV]
                    A3[ABNT Formatter]
                end

                J3 -.-> CrossValidator
                A3 -.-> CrossValidator
                
                CrossValidator((Validação Cruzada G0-GF)) --> Output[Artefato Final]
                
                style Central fill:#FF3366,color:#fff
                style Output fill:#00fa9a,color:#000
            </div>
            <p style="margin-top: 15px; font-size: 0.85em; color: #888;">Figura 3.0 - Topologia do Swarm de Agentes</p>
        </div>

        <h3>3.1. Invocando pela Interface (OpenCode)</h3>
        <p>No chat do OpenCode, a magia acontece apenas se a skill estiver carregada. Por exemplo, a skill <code>criador-de-artigo-v2</code>.</p>
<pre><code>@criador-de-artigo-v2, ative a Legião Acadêmica.
Tema: Educação Básica no Brasil como Salvação da Renda Média.
Estrutura: Mapeie o IBGE e use CRAG para validação de dados.
Auto-Run: Ativado (True).
</code></pre>

        <div class="page-break"></div>

        <!-- MÓDULO 4 -->
        <h2>MÓDULO 4: PIPELINE MODO DEUS (QUALIS A1 AUTO-THESIS)</h2>
        <p>Chegamos ao cerne do sistema. Construímos o Códice para que você não perca seu tempo gerando capítulos picados. É aqui que o código <code>run_thesis_god_mode.py</code> é engatilhado no servidor.</p>
        
        <p>Eis o ciclo de vida do "Modo Deus":</p>
        <ol>
            <li><strong>Despertar do Cérebro:</strong> <code>nexus = TransformerOrchestrator(tier="MAGNUM")</code></li>
            <li><strong>Emissão do Tema:</strong> O Intent Parser (Camada 1) quebra seu tema de 10 palavras em 50 vetores dimensionais.</li>
            <li><strong>Disparo Semântico:</strong> O RAG vai ao arXiv e puxa 55 referências bibliográficas do zero.</li>
            <li><strong>Escrita Assíncrona:</strong> Múltiplos agentes redigem Seção 1 (Metodologia) e Seção 2 (Fundamentação) paralelamente.</li>
            <li><strong>Auditoria CRAG:</strong> Agentes de "Red Team" tentam derrubar os argumentos da tese em memória. Se a tese não se defender (score < 80%), o texto é reescrito.</li>
            <li><strong>Drop do Loot:</strong> O arquivo <code>TESE_FINAL_A1_NEXUS.md</code> é salvo na pasta <code>output/</code>.</li>
        </ol>

        <div class="alert-box">
            <strong>DICA DE ALTO ESCALÃO:</strong><br>
            A Orquestração Transformer não sofre de loops infinitos. Se o <code>Critic-Router</code> detectar que o conteúdo da Legião A está alucinando, ele para a execução em 3 iterações limite, gera o Markdown com o que conseguiu, e anexa um <code>relatorio_auditoria.json</code> dizendo exatamente onde a literatura acadêmica falhou em embasar sua premissa.
        </div>

        <div class="page-break"></div>

        <!-- MÓDULO 5 -->
        <h2>MÓDULO 5: O TROUBLESHOOTING E ALQUIMIAS</h2>
        <p>Arquiteturas complexas têm fluxos complexos. Para garantir a imortalidade do Nexus na sua máquina, utilize as Táticas de Reparação.</p>

        <table>
            <thead>
                <tr>
                    <th>Anomalia Detectada (Erro)</th>
                    <th>Origem na Rede Transformer</th>
                    <th>Script de Cura (Vibe Code)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Timeout no MCP Jurídico</td>
                    <td>O Attention Mechanism perdeu ponte UDP</td>
                    <td><code>python fix_mcp_issues.py --restart</code></td>
                </tr>
                <tr>
                    <td>Referências Falsas no Artigo</td>
                    <td>Gate de Validação G2 (CRAG) desativado</td>
                    <td>Alterar <code>tier="STANDARD"</code> para <code>tier="MAGNUM"</code></td>
                </tr>
                <tr>
                    <td>Erro UnicodeEncodeError (\u26a1)</td>
                    <td>Console Windows não renderiza UTF-8</td>
                    <td>Executar: <code>$env:PYTHONIOENCODING="utf-8"</code></td>
                </tr>
                <tr>
                    <td>OpenCode não vê os Agentes</td>
                    <td>Skills não copiadas para GlobalStorage</td>
                    <td>Re-executar o Feitiço do Level 1 (<code>deploy_nexus.py</code>)</td>
                </tr>
            </tbody>
        </table>
        
        <div style="text-align: center; margin-top: 100px;">
            <h1 style="border-bottom: none;">FIM DO CÓDICE</h1>
            <p style="color: #666;">Gerado Autonomamente por Agência de Inteligência Artificial Antigravity</p>
            <p style="color: #444; font-size: 0.8em;">(Módulo PDF/HTML Export Support - MASWOS 5.0 NEXUS)</p>
        </div>
    </div>
</body>
</html>
"""

try:
    with open("LIVRO_NEXUS_VIBE_CODE_COMPLETO.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML Content successfully generated!")
except Exception as e:
    print(f"Error writing HTML: {e}")
