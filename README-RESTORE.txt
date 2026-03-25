# Backup do Ecossistema Opencode
Data: 2026-03-23
Arquivo: backup-opencode-todos-20260323.tar.gz (51MB)

## Conteúdo do Backup:
1. Diretório ~/.opencode (skills, configs, node_modules)
2. Skills locais (criador-de-artigo-v2)
3. Projeto PageIndex
4. Exemplos (examples/)
5. Configurações MCP (arquivos .json)
6. Diretórios de projeto (mcp-ecossistema-tese, mcp-tese-completa)
7. Arquivos de configuração (.env, academic-api-keys.env, etc.)
8. Documentação (SKILL*.md)

## Instruções de Restauração:

### 1. Restaurar ~/.opencode:
```bash
cd ~
tar -xzvf /caminho/para/backup-opencode-todos-20260323.tar.gz .opencode
```

### 2. Restaurar arquivos do projeto:
```bash
cd /caminho/do/projeto
tar -xzvf /caminho/para/backup-opencode-todos-20260323.tar.gz \
  criador-de-artigo-v2 PageIndex examples \
  .env academic-api-keys.env academic-api-config.json \
  mcp_servers_config.json ecosystem-transformer-config.json \
  maswos-academic-config.json maswos-academic-geospatial-config.json \
  maswos-juridico-config.json maswos-mcp-config.json \
  mcp-ecossistema-tese mcp-tese-completa \
  SKILL.md SKILL_ACADEMIC.md SKILL_UNIFICADO.md
```

### 3. Verificar instalação:
- Instalar opencode novamente
- Copiar ~/.opencode para o diretório do usuário
- Restaurar arquivos de configuração no diretório do projeto
- Verificar chaves de API nos arquivos .env

## Notas:
- As chaves de API estão incluídas (.env, academic-api-keys.env)
- O backup inclui node_modules do opencode (pode ser reinstalado via npm)
- Para reinstalar dependências Python, executar: pip install -r requirements.txt (se existir)
- O diretório PageIndex já está incluído com suas dependências