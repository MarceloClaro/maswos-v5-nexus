# Ecosystem Cloner - Documentação

## Visão Geral

O **Ecosystem Cloner** é um skill completo para clonagem cirúrgica do ecossistema Opencode. Ele replica todos os componentes do sistema com precisão e validação de integridade.

## Componentes Clonáveis

| Componente | Descrição | Quantidade |
|------------|-----------|-------------|
| Skills | Módulos de conhecimento especializados | 45+ |
| Workflows | Fluxos de trabalho automatizados | 11 |
| RAGs | Implementações de Retrieval Augmented Generation | 10+ |
| Scripts | Ferramentas e utilitários | 15+ |
| Configs | Arquivos de configuração | 5+ |
| Agentes | Definições de agentes | 21+ |

## Uso

### Clonagem Completa (Um Único OK)

```bash
# Clone completo com um único comando
python scripts/one_click_clone.py \
    --source "C:\Users\marce\Downloads\maswos-v5-nexus-dist" \
    --target "C:\backup\opencode_clone" \
    --approve
```

### Clonagem Seletiva

```bash
# Clone apenas skills
python scripts/ecosystem_cloner.py clone \
    --source <fonte> \
    --target <destino> \
    --skills

# Clone apenas workflows
python scripts/ecosystem_cloner.py clone \
    --source <fonte> \
    --target <destino> \
    --workflows
```

### Validação

```bash
# Validar clone
python scripts/validate_clone.py \
    --target <caminho_clone> \
    --full

# Validação rápida
python scripts/validate_clone.py \
    --target <caminho_clone> \
    --quick
```

### Escanear

```bash
# Escanear ecossistema
python scripts/ecosystem_cloner.py scan \
    --source <caminho> \
    --output manifesto.json
```

## Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `ecosystem_cloner.py` | Script principal de clonagem |
| `one_click_clone.py` | Clone com um único OK |
| `validate_clone.py` | Validação de integridade |

## Workflow de Clonagem

```
1. Escaneamento → Identifica componentes
2. Validação → Verifica estrutura fonte
3. Clonagem → Copia componentes
4. Verificação → Checksums
5. Relatório → Gera relatório final
```

## Estrutura de Saída

```
[destino]/
├── .agent/
│   ├── skills/
│   │   ├── [todos os skills]
│   │   └── SKILL.md
│   ├── workflows/
│   │   └── [11 workflows]
│   ├── TRANSFORMER_NETWORK_ARCHITECTURE.md
│   ├── mcp_config.json
│   └── doc.md
├── rag/
│   ├── base/
│   ├── classic/
│   ├── hybrid/
│   ├── agentic/
│   └── [outros módulos]
└── CLONE_REPORT.json
```

## Validação

O sistema de validação verifica:

- **Integridade Estrutural**: Diretórios e arquivos presentes
- **Completude**: Skills, workflows, RAGs esperados
- **Conteúdo**: Arquivos não estão vazios
- **Metadados**: Manifesto e relatórios

## Score de Validação

| Score | Status | Ação |
|-------|--------|------|
| 95-100% | PASS | Pronto para uso |
| 70-94% | PARTIAL | Revisar avisos |
| <70% | FAIL | Reclonar componentes |

## Troubleshooting

### Erro: "Source não encontrado"
- Verifique o caminho da fonte
- Use `--dry-run` para testar

### Erro: "Checksum falhou"
- Execute novamente a clonagem
- Use `--skip-existing false`

### Warning: "Arquivos existentes"
- Use `--skip-existing false` para sobrescrever
- Use `--approve` para confirmar

## Exemplo de Uso Completo

```bash
# 1. Escanear ecossistema fonte
python scripts/ecosystem_cloner.py scan \
    --source "C:\Users\marce\Downloads\maswos-v5-nexus-dist" \
    --output scan_report.json

# 2. Validar que o scan está OK
cat scan_report.json | python -m json.tool

# 3. Executar clone com um OK
python scripts/one_click_clone.py \
    --source "C:\Users\marce\Downloads\maswos-v5-nexus-dist" \
    --target "D:\meu_backup\opencode" \
    --approve

# 4. Validar clone
python scripts/validate_clone.py \
    --target "D:\meu_backup\opencode" \
    --full \
    --report validation.json

# 5. Verificar resultado
cat validation.json | python -m json.tool
```

## Requisitos

- Python 3.8+
- pathlib (stdlib)
- hashlib (stdlib)
- json (stdlib)
- shutil (stdlib)

## Autor

- **Nome:** Transformer Network
- **Versão:** 1.0.0
- **Data:** 2026-03-24
- **Domínio:** DevOps/System Administration

## Licença

Este skill faz parte do ecossistema Opencode e está disponível para uso imediato.
