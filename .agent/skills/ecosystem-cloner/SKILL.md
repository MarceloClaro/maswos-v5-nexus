# SKILL: ECOSYSTEM CLONER - Clonagem Cirúrgica do Ecossistema Opencode

## Identificação do Skill

- **Nome:** ecosystem-cloner
- **Domínio:** DevOps/System Administration
- **TIER:** 1 (Magnum)
- **Descrição:** Clona todo o ecossistema Opencode de forma cirúrgica e minuciosa, replicando MCPs, Skills, Agentes, Prompts, RAGs, Workflows e todas as configurações com um único comando de aprovação.
- **Versão:** 1.0.0
- **Data de Criação:** 2026-03-24
- **Autor:** Transformer Network

---

## visão Geral

Este skill é responsável por clonar/replicar todo o ecossistema Opencode implementado, incluindo:

1. **Skills** - Todos os módulos de conhecimento (50+ skills)
2. **Workflows** - Fluxos de trabalho automatizados (11 workflows)
3. **MCP Servers** - Servidores de contexto (academic, juridico, maswos, ecosystem, orchestrator)
4. **Agentes** - 21+ tipos de agentes especializados
5. **Prompts** - Templates de prompts otimizados
6. **RAGs** - 10+ implementações de RAG (Classic, Hybrid, Agentic, Graph, etc.)
7. **Configurações** - Arquivos de configuração e arquitetura
8. **Scripts** - Ferramentas auxiliares e utilitários

---

## Arquitetura do Clonador

### Fase 1: Análise do Ecossistema Fonte

```yaml
analise_fonte:
  componentes_identificados:
    - skills: "~50 módulos"
    - workflows: "11 fluxos"
    - mcp_servers: "5+ servidores"
    - agentes: "21+ tipos"
    - prompts: "múltiplos templates"
    - rags: "10+ implementações"
    - scripts: "diversas ferramentas"
    - configs: "arquitetura completa"
  
  mapeamento_estrutura:
    skills_dir: "~/.opencode/skills/"
    workflows_dir: ".agent/workflows/"
    mcp_config: "~/.gemini/antigravity/mcp_config.json"
    rag_dir: "rag/"
    agent_config: ".agent/"
```

### Fase 2: Estratégia de Clonagem

```yaml
estrategia:
  tipo_clonagem: "cirúrgica_e_minuciosa"
  nivel_granularidade: "arquivo_a_arquivo"
  preservacao_estrutura: true
  validacao_integridade: true
  compressao: "opcional"
  
  metodos_replicacao:
    - direct_copy: "Cópia direta de arquivos"
    - template_based: "Geração por templates"
    - dynamic_reconstruction: "Reconstrução dinâmica"
    - archive_based: "Baseado em arquivos compactados"
```

### Fase 3: Validação Pós-Clonagem

```yaml
validacao:
  checksum_verification: true
  structural_integrity: true
  functionality_test: true
  dependency_check: true
  configuration_sync: true
```

---

## Agentes Especializados

### 1. ECOSYSTEM_SCANNER_AGENT
**ID:** 01
**Função:** Escaneia e cataloga todo o ecossistema fonte

```yaml
capabilidades:
  - scanner_de_skills
  - identificador_de_workflows
  - mapeador_de_mcps
  - catalogo_de_agentes
  - inventario_de_rags
  - deteccao_de_configuracoes
  
entrada:
  - source_path: "Caminho do ecossistema fonte"
  - scan_depth: "profundidade do escaneamento"
  - include_patterns: "padrões a incluir"
  - exclude_patterns: "padrões a excluir"

saida:
  - ecosystem_inventory: "Inventário completo"
  - component_map: "Mapeamento de componentes"
  - dependency_graph: "Grafo de dependências"
  - metadata_catalog: "Catálogo de metadados"
```

### 2. SKILL_CLONER_AGENT
**ID:** 02
**Função:** Clona todos os skills com precisão cirúrgica

```yaml
capabilidades:
  - identificacao_de_skills
  - extracao_de_conteudo
  - conversao_de_formato
  - injecao_de_metadados
  - validacao_de_estrutura
  
processamento:
  etapa_1: "Identificar todos os SKILL.md"
  etapa_2: "Extrair estrutura (agentes, workflows, scripts)"
  etapa_3: "Preservar frontmatter e metadados"
  etapa_4: "Replicar subdiretórios"
  etapa_5: "Validar integridade"

formato_saida:
  - skill_name/
  - ├── SKILL.md
  - ├── [subdiretorios]/
  - └── scripts/
```

### 3. WORKFLOW_CLONER_AGENT
**ID:** 03
**Função:** Clona todos os workflows do ecossistema

```yaml
capabilidades:
  - mapeamento_de_workflows
  - extracao_de_fases
  - preservacao_de_prompt_templates
  - validacao_de_estruturas
  
workflows_suportados:
  - brainstorm.md
  - create.md
  - debug.md
  - deploy.md
  - enhance.md
  - orchestrate.md
  - plan.md
  - preview.md
  - status.md
  - test.md
  - ui-ux-pro-max.md
```

### 4. MCP_CLONER_AGENT
**ID:** 04
**Função:** Clona configurações e estruturas de MCP Servers

```yaml
capabilidades:
  - extracao_de_configuracoes
  - mapeamento_de_endpoints
  - replicacao_de_tools
  - sincronizacao_de_recursos
  
mcps_alvo:
  - academic_mcp
  - juridico_mcp
  - maswos_mcp
  - ecosystem_mcp
  - orchestrator_mcp
  - context7_mcp
  - shadcn_mcp
```

### 5. AGENT_TEMPLATES_CLONER_AGENT
**ID:** 05
**Função:** Clona definições e templates de agentes

```yaml
capabilidades:
  - extracao_de_definicoes
  - mapeamento_de_capacidades
  - replicacao_de_agentes
  - geracao_de_mapeamentos

agentes_suportados:
  - backend-specialist
  - frontend-specialist
  - devops-engineer
  - database-architect
  - security-auditor
  - penetration-tester
  - debugger
  - performance-optimizer
  - test-engineer
  - qa-automation-engineer
  - mobile-developer
  - game-developer
  - documentation-writer
  - code-archaeologist
  - orchestrator
  - project-planner
  - product-manager
  - product-owner
  - explorer-agent
  - seo-specialist
  - transformer-network
```

### 6. RAG_CLONER_AGENT
**ID:** 06
**Função:** Clona todas as implementações de RAG

```yaml
capabilidades:
  - mapeamento_de_arquiteturas
  - extracao_de_codigo
  - replicacao_de_modulos
  - validacao_de_dependencias

rags_suportados:
  - classic/vanilla_rag.py
  - hybrid/hybrid_rag.py
  - agentic/agentic_rag.py
  - graph/graph_rag.py
  - adaptive/adaptive_rag.py
  - corrective/crag.py
  - hyde/hyde.py
  - fusion/rag_fusion.py
  - memory/memory_rag.py
  - orchestrator/rag_orchestrator.py
  
modulos_base:
  - base/encoder.py
  - base/chunker.py
  - base/retriever.py
  - base/generator.py
  - base/augmenter.py
```

### 7. PROMPT_TEMPLATES_CLONER_AGENT
**ID:** 07
**Função:** Clona templates de prompts do ecossistema

```yaml
capabilidades:
  - extracao_de_templates
  - categorizacao_de_prompts
  - otimizacao_de_estruturas
  - geracao_de_biblioteca

tipos_suportados:
  - system_prompts
  - user_prompts
  - few_shot_examples
  - chain_of_thought
  - role_definitions
```

### 8. SCRIPT_UTILITIES_CLONER_AGENT
**ID:** 08
**Função:** Clona scripts e ferramentas auxiliares

```yaml
capabilidades:
  - identificacao_de_scripts
  - extracao_de_codigo
  - categorizacao_por_tipo
  - validacao_de_dependencias

scripts_identificados:
  - security_scan.py
  - geo_checker.py
  - test_runner.py
  - lighthouse_audit.py
  - schema_validator.py
  - playwright_runner.py
  - react_performance_checker.py
  - convert_rules.py
  - seo_checker.py
  - accessibility_checker.py
  - ux_audit.py
```

### 9. ARCHITECTURE_CLONER_AGENT
**ID:** 09
**Função:** Clona configurações e documentação de arquitetura

```yaml
capabilidades:
  - extracao_de_configs
  - mapeamento_de_estrutura
  - replicacao_de_documentacao
  - sincronizacao_de_arquivos

arquivos_alvo:
  - TRANSFORMER_NETWORK_ARCHITECTURE.md
  - mcp_config.json
  - transform_example.json
  - doc.md
  - Arquivos de configuração diversos
```

### 10. VALIDATOR_CLONER_AGENT
**ID:** 10
**Função:** Valida integridade do ecossistema clonado

```yaml
capabilidades:
  - verificacao_de_checksum
  - validacao_estrutural
  - teste_de_funcionalidade
  - comparacao_de_conteudo
  - relatorio_de_diferencas

checkpoints:
  - integrity_check
  - content_verification
  - structure_validation
  - dependency_resolution
  - functionality_test
```

---

## Workflow de Clonagem Completa

### ETAPA 1: Escaneamento Inicial

```yaml
escaneamento:
  comando: "/clone scan --source [caminho_fonte]"
  
  acoes:
    1: "Identificar diretório raiz do ecossistema"
    2: "Mapear estrutura de diretórios"
    3: "Catalogar todos os componentes"
    4: "Gerar inventário completo"
    5: "Calcular checksums originais"
  
  saida:
    - scan_report.yaml
    - component_tree.json
    - original_checksums.md5
```

### ETAPA 2: Clonagem de Skills

```yaml
clonagem_skills:
  comando: "/clone skills --target [caminho_destino]"
  
  acoes:
    1: "Localizar todos os SKILL.md no ecossistema"
    2: "Identificar subdiretórios (scripts, templates, etc.)"
    3: "Copiar estrutura preservada"
    4: "Gerar manifesto de skills clonados"
    5: "Validar cada skill individualmente"
  
  skills_alvo:
    - academic-thesis-production
    - api-patterns
    - app-builder
    - architecture
    - bash-linux
    - behavioral-modes
    - brainstorming
    - clean-code
    - code-review-checklist
    - database-design
    - data-scientist-phd
    - deployment-procedures
    - documentation-templates
    - frontend-design
    - game-development
    - geo-fundamentals
    - i18n-localization
    - intelligent-integration
    - intelligent-routing
    - lint-and-validate
    - mcp-builder
    - mobile-design
    - nextjs-react-expert
    - nodejs-best-practices
    - parallel-agents
    - performance-profiling
    - plan-writing
    - powershell-windows
    - python-patterns
    - red-team-tactics
    - rust-pro
    - seo-fundamentals
    - server-management
    - systematic-debugging
    - tailwind-patterns
    - tdd-workflow
    - testing-patterns
    - vulnerability-scanner
    - webapp-testing
    - web-design-guidelines
  
  saida:
    - cloned_skills/
    - skills_manifest.json
    - skills_validation_report.md
```

### ETAPA 3: Clonagem de Workflows

```yaml
clonagem_workflows:
  comando: "/clone workflows --target [caminho_destino]"
  
  acoes:
    1: "Copiar todos os arquivos .md de workflows"
    2: "Preservar estrutura e metadados"
    3: "Validar completude"
  
  workflows_alvo:
    - brainstorm.md
    - create.md
    - debug.md
    - deploy.md
    - enhance.md
    - orchestrate.md
    - plan.md
    - preview.md
    - status.md
    - test.md
    - ui-ux-pro-max.md
  
  saida:
    - cloned_workflows/
    - workflows_manifest.json
```

### ETAPA 4: Clonagem de MCPs

```yaml
clonagem_mcps:
  comando: "/clone mcps --target [caminho_destino]"
  
  acoes:
    1: "Exportar configurações de MCP"
    2: "Clonar definições de tools"
    3: "Replicar recursos"
    4: "Sincronizar prompts do sistema"
  
  mcps_configurados:
    - academic_mcp
    - juridico_mcp
    - maswos_mcp
    - ecosystem_mcp
    - orchestrator_mcp
    - context7_mcp
    - shadcn_mcp
  
  saida:
    - mcps_config.json
    - tools_definitions/
    - resources/
    - system_prompts/
```

### ETAPA 5: Clonagem de RAGs

```yaml
clonagem_rags:
  comando: "/clone rags --target [caminho_destino]"
  
  acoes:
    1: "Copiar todos os módulos de RAG"
    2: "Replicar base/common"
    3: "Preservar estrutura de diretórios"
    4: "Validar dependências Python"
  
  saida:
    - cloned_rag/
    - ├── base/
    - ├── classic/
    - ├── hybrid/
    - ├── agentic/
    - ├── graph/
    - ├── adaptive/
    - ├── corrective/
    - ├── hyde/
    - ├── fusion/
    - ├── memory/
    - └── orchestrator/
```

### ETAPA 6: Clonagem de Agentes

```yaml
clonagem_agentes:
  comando: "/clone agents --target [caminho_destino]"
  
  acoes:
    1: "Mapear definições de agentes"
    2: "Copiar templates"
    3: "Replicar configurações"
  
  saida:
    - agents_definitions/
    - agent_templates/
    - agent_mappings.yaml
```

### ETAPA 7: Clonagem de Scripts

```yaml
clonagem_scripts:
  comando: "/clone scripts --target [caminho_destino]"
  
  scripts_localizados:
    - vulnerability-scanner/scripts/security_scan.py
    - geo-fundamentals/scripts/geo_checker.py
    - testing-patterns/scripts/test_runner.py
    - performance-profiling/scripts/lighthouse_audit.py
    - database-design/scripts/schema_validator.py
    - webapp-testing/scripts/playwright_runner.py
    - nextjs-react-expert/scripts/react_performance_checker.py
    - nextjs-react-expert/scripts/convert_rules.py
    - seo-fundamentals/scripts/seo_checker.py
    - frontend-design/scripts/accessibility_checker.py
    - frontend-design/scripts/ux_audit.py
  
  saida:
    - cloned_scripts/
    - scripts_index.json
```

### ETAPA 8: Clonagem de Configurações

```yaml
clonagem_configs:
  comando: "/clone config --target [caminho_destino]"
  
  arquivos:
    - TRANSFORMER_NETWORK_ARCHITECTURE.md
    - mcp_config.json
    - transform_example.json
    - doc.md
  
  saida:
    - configs/
    - architecture_docs/
```

### ETAPA 9: Validação Final

```yaml
validacao:
  comando: "/clone validate --target [caminho_destino]"
  
  verificacoes:
    - checksum_comparison
    - structural_integrity
    - file_count_verification
    - content_similarity
    - dependency_check
  
  saida:
    - validation_report.json
    - diff_report.md
    - integrity_certificate.md
```

---

## Comandos de Clonagem

### Clonagem Completa (Um Único OK)

```bash
# Clonar todo o ecossistema com um único comando de aprovação
/clone full --source [caminho_fonte] --target [caminho_destino] --approve

# Sintaxe alternativa
/clone ecosystem --from [fonte] --to [destino] --ok
```

Este comando executa todas as etapas automaticamente e requer apenas uma aprovação.

### Clonagem Seletiva

```bash
# Clonar apenas skills
/clone skills --source [fonte] --target [destino]

# Clonar apenas workflows
/clone workflows --source [fonte] --target [destino]

# Clonar apenas RAGs
/clone rags --source [fonte] --target [destino]

# Clonar apenas MCPs
/clone mcps --source [fonte] --target [destino]

# Clonar apenas agentes
/clone agents --source [fonte] --target [destino]

# Clonar apenas configurações
/clone config --source [fonte] --target [destino]

# Clonar apenas scripts
/clone scripts --source [fonte] --target [destino]
```

### Comandos de Verificação

```bash
# Escanear ecossistema fonte
/clone scan --source [caminho]

# Verificar integridade
/clone verify --target [caminho]

# Comparar ecossistemas
/clone diff --source [fonte] --target [destino]

# Gerar relatório
/clone report --target [caminho]
```

---

## Estrutura de Saída do Clone

```
[destino]/
├── .agent/
│   ├── skills/
│   │   ├── [todos os 50+ skills]
│   │   └── SKILL.md (índice)
│   ├── workflows/
│   │   ├── brainstorm.md
│   │   ├── create.md
│   │   ├── debug.md
│   │   ├── deploy.md
│   │   ├── enhance.md
│   │   ├── orchestrate.md
│   │   ├── plan.md
│   │   ├── preview.md
│   │   ├── status.md
│   │   ├── test.md
│   │   └── ui-ux-pro-max.md
│   ├── TRANSFORMER_NETWORK_ARCHITECTURE.md
│   ├── mcp_config.json
│   ├── transform_example.json
│   └── doc.md
├── rag/
│   ├── base/
│   ├── classic/
│   ├── hybrid/
│   ├── agentic/
│   ├── graph/
│   ├── adaptive/
│   ├── corrective/
│   ├── hyde/
│   ├── fusion/
│   ├── memory/
│   └── orchestrator/
├── mcps/
│   ├── academic/
│   ├── juridico/
│   ├── maswos/
│   ├── ecosystem/
│   └── orchestrator/
└── clone_manifest.json
```

---

## Sistema de Validação

### Checkpoints de Qualidade

```yaml
qualidade:
  threshold_minimo: 0.95
  
  checkpoints:
    - name: "checksum_integrity"
      status: required
      weight: 0.20
      
    - name: "structural_integrity"
      status: required
      weight: 0.20
      
    - name: "content_completeness"
      status: required
      weight: 0.20
      
    - name: "dependency_resolution"
      status: required
      weight: 0.15
      
    - name: "functionality_test"
      status: required
      weight: 0.15
      
    - name: "metadata_preservation"
      status: optional
      weight: 0.10
```

### Relatório de Validação

```json
{
  "validation_report": {
    "timestamp": "2026-03-24T00:00:00Z",
    "source": "[caminho_fonte]",
    "target": "[caminho_destino]",
    "overall_score": 0.98,
    "checks": {
      "checksum_integrity": {
        "status": "PASS",
        "score": 1.0,
        "details": "Todos os checksums correspondem"
      },
      "structural_integrity": {
        "status": "PASS",
        "score": 0.99,
        "details": "Estrutura preservada"
      },
      "content_completeness": {
        "status": "PASS",
        "score": 0.97,
        "details": "98.5% do conteúdo clonado"
      },
      "dependency_resolution": {
        "status": "PASS",
        "score": 0.95,
        "details": "Dependências resolvidas"
      },
      "functionality_test": {
        "status": "PASS",
        "score": 0.96,
        "details": "Testes passaram"
      }
    },
    "cloned_components": {
      "skills": 45,
      "workflows": 11,
      "mcps": 7,
      "rags": 10,
      "scripts": 11,
      "configs": 4
    }
  }
}
```

---

## Metadados do Skill

```yaml
metadata:
  name: "ecosystem-cloner"
  version: "1.0.0"
  created: "2026-03-24"
  author: "Transformer Network"
  tier: 1
  domain: "devops"
  capabilities:
    - "Clonagem completa de ecossistema"
    - "Clonagem seletiva por componente"
    - "Validação de integridade"
    - "Geração de relatórios"
    - "Verificação de checksums"
  dependencies:
    - "file_system_access"
    - "checksum_computation"
    - "json_processing"
    - "yaml_processing"
  performance:
    - "Processamento paralelo"
    - "Compressão opcional"
    - "Progress tracking"
```

---

## Exemplos de Uso

### Exemplo 1: Clonagem Completa

```
Usuário: "Clone todo o ecossistema opencode para o diretório /backup/opencode"

Agente: Executa /clone full --source C:\Users\marce\Downloads\maswos-v5-nexus-dist\.agent --target /backup/opencode --approve

Resultado: Ecossistema completo clonado com validação
```

### Exemplo 2: Clonagem Seletiva

```
Usuário: "Preciso apenas dos skills de segurança e banco de dados"

Agente: Executa /clone skills --category security,database --source [fonte] --target [destino]

Resultado: Apenas skills relevantes clonados
```

### Exemplo 3: Verificação

```
Usuário: "Verifique se o clone está íntegro"

Agente: Executa /clone validate --target [destino]

Resultado: Relatório de validação detalhado
```

---

## Notas de Implementação

1. **Precisão Cirúrgica**: Cada arquivo é copiado individualmente com verificação de integridade
2. **Preservação de Metadados**: Timestamps, permissões e atributos são mantidos
3. **Tratamento de Erros**: Qualquer falha interrompe e reporta imediatamente
4. **Modo Verbose**: Opcionalmente mostra progresso detalhado
5. **Compressão**: Suporte a compactação para transferência
6. **Incremental**: Suporte a clonagem incremental (apenas diferenças)

---

## Troubleshooting

```yaml
problemas_comuns:
  - problema: "Permissão negada"
    solucao: "Verificar permissões de leitura/escrita"
    
  - problema: "Checksums não correspondem"
    solucao: "Reexecutar clonagem do componente afetado"
    
  - problema: "Dependências faltando"
    solucao: "Executar /clone resolve-dependencies"
    
  - problema: "Espaço insuficiente"
    solucao: "Usar modo comprimido /clone --compress"
```

---

## Conclusão

Este skill fornece uma ferramenta completa e minuciosa para clonar todo o ecossistema Opencode com um único comando de aprovação. A arquitetura permite tanto clonagem completa quanto seletiva, com validação rigorosa de integridade em cada etapa.
