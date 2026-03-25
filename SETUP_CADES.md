# Configuração MCP CAPES Externo
# Baseado em: https://github.com/damarals/periodicos-capes-mcp

## Instalação

```bash
# 1. Instalar dependências
npm install -g periodicos-capes-mcp

# 2. Criar conta Zyte (obrigatório para bypass de proteção)
# https://zyte.com

# 3. Configurar API key
export ZYTE_API_KEY="sua_chave_aqui"
```

## Configuração Claude Code / OpenCode

Adicione ao arquivo de configuração do MCP:

```json
{
  "mcpServers": {
    "maswos-academic": {
      "command": "python",
      "args": ["C:/Users/marce/Downloads/maswos-v5-nexus-dist/mcp_academic_proxy.py"]
    },
    "capes": {
      "command": "periodicos-capes-mcp",
      "env": {
        "ZYTE_API_KEY": "${ZYTE_API_KEY}"
      }
    }
  }
}
```

## Variáveis de Ambiente

Crie arquivo `.env`:

```bash
# Zyte API (OBRIGATÓRIA para CAPES)
ZYTE_API_KEY=sua_chave_zyte_aqui

# API Keys Opcionais
SEMANTIC_SCHOLAR_API_KEY=
NCBI_API_KEY=
KAGGLE_USERNAME=
KAGGLE_KEY=
GITHUB_TOKEN=
```

## Ferramentas CAPES Disponíveis

- `capes_search` - Busca artigos no Portal CAPES
- `capes_export` - Exporta para pasta estruturada (RIS/BibTeX)
- `capes_journals` - Lista periódicos por área

## Notas

- O Portal CAPES requer acesso via CAFe ou Zyte API para bypass
- O MCP oferece métricas integradas OpenAlex (citações, FWCI) + Qualis
- Suporta filtros: tipo, acesso aberto, revisão por pares, ano, idioma
