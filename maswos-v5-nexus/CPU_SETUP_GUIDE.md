# Guia de Configuração para CPU - MCP Academic Transform

## ⚠️ Configuração para Usuários SEM GPU

Se você tem apenas **CPU**, este guia é para você. O MCP Academic Transform pode funcionar perfeitamente em CPU com as configurações adequadas.

## 📋 Requisitos Mínimos de Sistema

### CPU
- **Mínimo**: 4 cores (recomendado 8+)
- **Arquitetura**: x86_64 (Intel/AMD)
- **Velocidade**: 2.0 GHz+

### Memória RAM
- **Mínimo**: 8 GB
- **Recomendado**: 16 GB
- **Ideal**: 32 GB+

### Armazenamento
- **Mínimo**: 10 GB livres
- **Recomendado**: 20 GB+ (para modelos)

## 🚀 Instalação Otimizada para CPU

### 1. Instalar Dependências Leves

```bash
# Instalar PyTorch para CPU (sem CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Instalar Transformers (versão leve)
pip install transformers[cpu]

# Dependências adicionais
pip install psutil accelerate
```

### 2. Modelos Recomendados para CPU

#### **Para Text Generation (geração de texto)**
```python
# Modelos pequenos (recomendado para CPU)
MODELS = {
    "tiny": "Qwen/Qwen2.5-0.5B-Instruct",      # 0.5B params - Muito leve
    "small": "TinyLlama/TinyLlama-1.1B-Chat",   # 1.1B params - Leve
    "medium": "microsoft/Phi-3-mini-4k-instruct", # 3.8B params - Moderado
}
```

#### **Para Classificação**
```python
MODELS = {
    "tiny": "distilbert-base-uncased",      # 66M params
    "small": "bert-base-uncased",           # 110M params
}
```

#### **Para Embeddings**
```python
MODELS = {
    "tiny": "sentence-transformers/all-MiniLM-L6-v2",  # 22M params
    "small": "sentence-transformers/all-MiniLM-L12-v2", # 33M params
}
```

## ⚙️ Configurações Otimizadas

### Configuração Automática (Recomendado)

```python
from mcp_cpu_optimized import get_cpu_profile, CPU_PROFILES

# Detecta automaticamente o melhor perfil
profile = get_cpu_profile()
config = CPU_PROFILES[profile]

print(f"Perfil detectado: {profile}")
print(f"Configuração: {config}")
```

### Perfis por Tipo de CPU

#### **CPU Antigo/Lento (2-4 cores)**
```python
CPU_CONFIG_LOW = {
    "torch_threads": 2,
    "model_size": "tiny",
    "max_length": 256,
    "batch_size": 1,
    "use_quantization": True,
    "use_llm_agents": False  # Desativa agentes LLM
}
```

#### **CPU Moderno (4-8 cores)**
```python
CPU_CONFIG_MID = {
    "torch_threads": 4,
    "model_size": "small",
    "max_length": 512,
    "batch_size": 2,
    "use_quantization": True,
    "use_llm_agents": True
}
```

#### **CPU Potente (8+ cores)**
```python
CPU_CONFIG_HIGH = {
    "torch_threads": 8,
    "model_size": "medium",
    "max_length": 1024,
    "batch_size": 4,
    "use_quantization": False,
    "use_llm_agents": True
}
```

## 🔧 Otimizações Específicas para CPU

### 1. Quantização (Reduz Memória)

```python
# Ativar quantização INT8
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0
)
```

### 2. Reduzir Uso de Memória

```python
# Configurações para baixo uso de memória
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,  # CPU usa float32
    device_map="cpu",
    low_cpu_mem_usage=True,     # Importante para CPU
    max_memory={"cpu": "8GB"}   # Limita memória
)
```

### 3. Processamento em Lotes (Batching)

```python
# Para múltiplas queries
batch_size = 2  # Ajuste conforme memória disponível
for i in range(0, len(queries), batch_size):
    batch = queries[i:i+batch_size]
    results = process_batch(batch)
```

### 4. Lazy Loading (Carregar sob Demanda)

```python
# Carrega modelo apenas quando necessário
def get_model(model_name):
    if not hasattr(get_model, '_cache'):
        get_model._cache = {}
    
    if model_name not in get_model._cache:
        get_model._cache[model_name] = load_model(model_name)
    
    return get_model._cache[model_name]
```

## 📊 Monitoramento de Recursos

### Verificar Uso de Memória

```python
import psutil

def check_resources():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count(logical=False)
    
    # Memória
    memory = psutil.virtual_memory()
    memory_gb = memory.total / (1024**3)
    memory_used = memory.used / (1024**3)
    memory_percent = memory.percent
    
    print(f"CPU: {cpu_percent}% ({cpu_cores} cores)")
    print(f"RAM: {memory_used:.1f}/{memory_gb:.1f} GB ({memory_percent}%)")
    
    return {
        "cpu_percent": cpu_percent,
        "cpu_cores": cpu_cores,
        "memory_used_gb": memory_used,
        "memory_total_gb": memory_gb,
        "memory_percent": memory_percent
    }
```

### Limpar Memória

```python
import gc
import torch

def clear_memory():
    # Limpa Python garbage collector
    gc.collect()
    
    # Limpa cache PyTorch (se existir GPU)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    print("✅ Memória limpa")
```

## 🚀 Exemplo Completo para CPU

```python
#!/usr/bin/env python3
"""
Exemplo completo MCP Academic para CPU
"""

import asyncio
from mcp_cpu_optimized import CPUMCPPipeline, get_cpu_profile, CPU_PROFILES

async def main():
    # 1. Detecta perfil do CPU
    profile = get_cpu_profile()
    config = CPU_PROFILES[profile]
    
    print(f"🖥️ Perfil detectado: {profile}")
    print(f"⚙️ Configuração: {config}")
    print()
    
    # 2. Cria pipeline
    pipeline = CPUMCPPipeline(config)
    
    # 3. Executa pesquisa
    query = "Pesquisar artigos sobre machine learning aplicado à saúde"
    result = await pipeline.execute(query)
    
    print()
    print("📊 Resultado:")
    print(f"Status: {result['status']}")
    print(f"Memória usada: {result['memory_usage_mb']:.2f} MB")
    
    return result

if __name__ == "__main__":
    asyncio.run(main())
```

## ⚡ Dicas de Performance para CPU

### 1. Fechar Outros Programas
- Feche navegadores com muitas abas
- Desative extensões pesadas
- Pause atualizações em segundo plano

### 2. Configurar Threads
```python
import os
os.environ["OMP_NUM_THREADS"] = "4"  # Ajuste conforme seu CPU
os.environ["MKL_NUM_THREADS"] = "4"
```

### 3. Usar Modelos Menores
- Prefira modelos de 0.5B a 1.5B parâmetros
- Evite modelos >3B em CPU
- Use quantização 8-bit

### 4. Processamento Assíncrono
```python
# Use asyncio para não bloquear
async def process_queries(queries):
    tasks = [process_query(q) for q in queries]
    return await asyncio.gather(*tasks)
```

## 📈 Benchmarks Estimados para CPU

| Perfil | Modelo | Tempo por Query | Memória |
|--------|--------|-----------------|---------|
| Low-end | 0.5B | 30-60s | 2-3 GB |
| Mid-range | 1.1B | 15-30s | 4-6 GB |
| High-end | 3.8B | 10-20s | 8-12 GB |

## 🔍 Solução de Problemas

### Erro: "Out of Memory"
```python
# Reduza o batch size
config["batch_size"] = 1

# Use modelo menor
config["model_size"] = "tiny"

# Ative quantização
config["use_quantization"] = True
```

### Erro: "Processo Muito Lento"
```python
# Reduza threads (se competindo por recursos)
config["torch_threads"] = 2

# Desative agentes LLM
config["use_llm_agents"] = False

# Use análise baseada em regras
use_llm = False
```

### Erro: "Modelo Não Carrega"
```python
# Use modelo mais leve
model_name = "Qwen/Qwen2.5-0.5B-Instruct"  # 0.5B

# Carregue em.float32 (CPU)
torch_dtype=torch.float32
```

## 📦 Arquivos Necessários

```
maswos-v5-nexus-dist/
├── mcp_cpu_optimized.py      # Pipeline otimizado para CPU
├── CPU_SETUP_GUIDE.md        # Este arquivo
├── examples/
│   └── mcp_integration/
│       └── academic_research.py
└── MCP_INTEGRATION_GUIDE.md
```

## ✅ Checklist de Configuração

- [ ] PyTorch para CPU instalado
- [ ] Transformers para CPU instalado
- [ ] psutil instalado
- [ ] Modelos baixados (0.5B ou 1.1B)
- [ ] Memória RAM suficiente (8GB+)
- [ ] Configuração de threads ajustada

## 🆘 Suporte

Se tiver problemas com configuração em CPU:
1. Verifique se tem PyTorch para CPU: `python -c "import torch; print(torch.__version__)"`
2. Verifique memória disponível: `python -c "import psutil; print(f'{psutil.virtual_memory().total/(1024**3):.1f} GB')"`
3. Use modelo mais leve: `model_name = "Qwen/Qwen2.5-0.5B-Instruct"`

---

**Nota**: O MCP Academic Transform funciona em CPU, mas será mais lento que com GPU. Para melhor experiência, use modelos de até 1.5B parâmetros e ative quantização.