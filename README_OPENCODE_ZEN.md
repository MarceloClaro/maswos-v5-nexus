# PageIndex com Opencode Zen (Big Pickle & MiMo V2)

## 🚀 Como Usar os Modelos do Opencode Zen no PageIndex

### 1. Obter Chave API do Opencode Zen

1. Acesse: https://opencode.ai/zen
2. Crie uma conta (gratuita)
3. Vá para "API Keys" e crie uma nova chave
4. Copie a chave (ex: `sk-...`)

### 2. Configurar Variáveis de Ambiente

**Windows (PowerShell):**
```powershell
$env:OPENCODE_API_KEY="sua-chave-aqui"
```

**Linux/macOS:**
```bash
export OPENCODE_API_KEY="sua-chave-aqui"
```

Ou adicione ao arquivo `.env`:
```
OPENCODE_API_KEY=sua-chave-aqui
```

### 3. Instalar Dependências

```bash
pip install litellm pyyaml requests
```

### 4. Executar PageIndex

**Com Big Pickle (GLM-4.6):**
```bash
python run_pageindex_opencode.py documento.pdf big-pickle
```

**Com MiMo V2 Pro Free:**
```bash
python run_pageindex_opencode.py documento.pdf mimo-v2-pro-free
```

**Com MiMo V2 Omni Free:**
```bash
python run_pageindex_opencode.py documento.pdf mimo-v2-omni-free
```

**Com Nemotron 3 Super Free:**
```bash
python run_pageindex_opencode.py documento.pdf nemotron-3-super-free
```

## 📊 Modelos Disponíveis (Gratuitos)

| Modelo | Descrição | Contexto | Melhor Para |
|--------|-----------|----------|-------------|
| **big-pickle** | GLM-4.6, otimizado para código | 200K | Documentos técnicos, papers |
| **mimo-v2-pro-free** | Modelo grande da Xiaomi (1T parâmetros) | 1M | Análise complexa, raciocínio |
| **mimo-v2-omni-free** | Multimodal (texto, imagem, áudio) | 256K | Documentos com figuras |
| **nemotron-3-super-free** | Modelo NVIDIA | 128K | Documentos gerais |

## 🔧 Configuração Manual

Se preferir configurar manualmente, edite `PageIndex/pageindex/config.yaml`:

```yaml
model: "custom/big-pickle"
toc_check_page_num: 15
max_page_num_each_node: 8
max_token_num_each_node: 4000
if_add_node_id: "yes"
if_add_node_summary: "yes"
if_add_doc_description: "no"
if_add_node_text: "no"
```

## 💡 Dicas

1. **Modelos grandes são mais lentos** - `big-pickle` pode ser mais rápido que `mimo-v2-pro-free`
2. **Contexto grande** - Use `mimo-v2-pro-free` para documentos com mais de 100 páginas
3. **Documentos multimodais** - Use `mimo-v2-omni-free` se o PDF contiver imagens
4. **Economia** - Todos os modelos listados são atualmente gratuitos

## ⚠️ Limitações

1. **Rate Limits** - Opencode Zen pode ter limites de taxa
2. **Disponibilidade** - Modelos gratuitos podem ter disponibilidade limitada
3. **Privacidade** - Dados podem ser usados para melhorar modelos (durante período gratuito)

## 📁 Arquivos Gerados

- `PageIndex/pageindex/config.yaml` - Configuração PageIndex
- `PageIndex/litellm_config.yaml` - Configuração litellm
- `results_opencode/` - Resultados salvos
- `.env` - Chave API (não commitar)

## 🆘 Solução de Problemas

| Problema | Solução |
|----------|---------|
| **Erro 401 Unauthorized** | Verifique a chave API |
| **Rate limit excedido** | Aguarde ou use outro modelo |
| **Timeout** | Use modelo menor ou documento menor |
| **Modelo não encontrado** | Verifique nome do modelo |

## 🔄 Alternativa: Ollama Local

Se preferir 100% local e offline, use Ollama:

```bash
python run_pageindex_local.py documento.pdf phi3:3.8b
```

Os modelos do Opencode Zen são baseados em API e requerem internet.