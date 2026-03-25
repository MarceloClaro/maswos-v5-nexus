# Data Scientist PhD Skill

> Módulo de análise de dados para produção acadêmica com precisão cirúrgica e minuciosa.

## Quando Usar

Use este skill quando precisar de:
- Análise estatística clássica (correlação, regressão, testes de hipótese)
- Detecção de anomalias e outliers
- Análise de tendências
- Insights qualitativos e quantitativos
- Varredura de dados para descoberta de padrões
- Sugestão de novas fontes de dados

## Capabilidades

### Análises Estatísticas Clássicas

| Técnica | Descrição | Aplicação |
|---------|-----------|------------|
| Correlação Pearson | Correlação linear | Variáveis contínuas |
| Correlação Spearman | Correlação por posto | Dados ordinais |
| Teste t | Comparação de médias | Duas amostras |
| Chi-Quadrado | Associção de categorias | Tabelas de contingência |
| Regressão Linear | Relação funcional | Previsão |

### Análises Modernas

| Técnica | Descrição | Aplicação |
|---------|-----------|------------|
| K-Means | Clustering | Segmentação |
| Detecção IQR | Outliers pelo IQR | Anomalias |
| Detecção Z-Score | Outliers padronizados | Anomalias extremas |
| Análise de Tendência | Série temporal | Evolução temporal |

### Análise Qualitativa

| Técnica | Descrição | Aplicação |
|---------|-----------|------------|
| Extração de Keywords | Palavras mais frequentes | Temas principais |
| Análise de Sentimento | Indicador emocional | Tom do texto |
| Análise Temática | Agrupamento por temas | Categorização |

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA SCIENTIST PhD                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │ CLASSICAL      │    │    MODERN        │    │  QUALITATIVE │  │
│  │ STATISTICS    │    │    STATISTICS    │    │  ANALYSIS    │  │
│  ├─────────────────┤    ├──────────────────┤    ├───────────────┤  │
│  │ • Mean/Median   │    │ • K-Means       │    │ • Keywords    │  │
│  │ • Variance     │    │ • Outliers IQR  │    │ • Sentiment  │  │
│  │ • Pearson      │    │ • Outliers Z    │    │ • Themes     │  │
│  │ • Spearman     │    │ • Trend Detect  │    │              │  │
│  │ • Chi-Square  │    │                  │    │              │  │
│  │ • t-test      │    │                  │    │              │  │
│  └─────────────────┘    └──────────────────┘    └───────────────┘  │
│            │                    │                    │              │
│            └────────────────────┼────────────────────┘              │
│                                 ▼                                   │
│                    ┌──────────────────────┐                        │
│                    │  INSIGHT DETECTION  │                        │
│                    ├──────────────────────┤                        │
│                    │ • Correlation       │                        │
│                    │ • Causation         │                        │
│                    │ • Anomaly           │                        │
│                    │ • Pattern           │                        │
│                    │ • Trend             │                        │
│                    │ • Problem           │                        │
│                    │ • Solution          │                        │
│                    └──────────────────────┘                        │
│                                 │                                   │
│                                 ▼                                   │
│                    ┌──────────────────────┐                        │
│                    │  DATA SOURCES       │                        │
│                    │  SUGGESTION         │                        │
│                    └──────────────────────┘                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Uso

```python
from data_scientist_analyst import DataScientistPhD, Dataset

# Criar cientista
ds = DataScientistPhD()

# Adicionar dataset (fonte validada)
dataset = Dataset(
    id="my_data",
    name="Meus Dados",
    variables=["var1", "var2", "var3"],
    observations=100,
    data_points=[...],  # Seus dados
    source="IBGE",  # Fonte validada
    is_verified=True
)
ds.add_dataset(dataset)

# Análises
corr = ds.analyze_correlations("var1", "var2", "pearson")
anomalies = ds.detect_anomalies("var3", "iqr")
trends = ds.analyze_trends("var1")

# Encontrar insights
insights = ds.find_insights(text_data="Seu texto...")

# Sugerir novas fontes
new_sources = ds.suggest_new_data_sources(insights)

# Gerar relatório
print(ds.generate_analysis_report())
```

## Métricas de Qualidade

| Métrica | Target | Descrição |
|---------|--------|-----------|
| Correlação detectada | > 0.5 | r > 0.5 com p < 0.1 |
| Anomalias identificadas | > 0 | Outliers no dataset |
| Insights gerados | > 3 | Insights acionáveis |
| Fontes sugeridas | > 5 | Novas fontes viáveis |

## Arquivos

- `data_scientist_analyst.py` - Módulo principal
- `academic_thesis_orchestrator.py` - Orquestrador de tese
- `academic_source_validator.py` - Validador de fontes

## Integração com Production System

O Cientista de Dados PhD pode ser usado em conjunto com o sistema de produção acadêmica para:
1. Analisar dados coletados via MCPs
2. Validar hipóteses estatisticamente
3. Gerar insights para discussão
4. Detectar anomalias nos resultados
5. Sugerir novas variáveis para investigação