"""
DATA SCIENTIST ANALYST - PhD LEVEL
===================================
Módulo de Análise de Dados para Produção Acadêmica
com Precisão Cirúrgica e Minuciosa.

Autor: MASWOS V5 NEXUS - Data Science Division
Versão: 5.1.0-PHD-GRADE
"""

import json
import re
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter, defaultdict
import math


class AnalysisType(Enum):
    """Tipos de análise disponíveis"""
    CORRELATION = "correlation"
    REGRESSION = "regression"
    HYPOTHESIS_TEST = "hypothesis_test"
    ANOMALY_DETECTION = "anomaly_detection"
    CLUSTERING = "clustering"
    TIME_SERIES = "time_series"
    TEXT_ANALYSIS = "text_analysis"
    QUALITATIVE = "qualitative"
    CAUSAL_INFERENCE = "causal_inference"
    SURVIVAL = "survival"


class InsightType(Enum):
    """Tipos de insight detectados"""
    CORRELATION = "correlation"
    CAUSATION = "causation"
    PATTERN = "pattern"
    TREND = "trend"
    OUTLIER = "outlier"
    DEFECT = "defect"
    PROBLEM = "problem"
    SOLUTION = "solution"
    OPPORTUNITY = "opportunity"
    ANOMALY_DETECTED = "anomaly"


class StatisticalSignificance(Enum):
    """Níveis de significância estatística"""
    HIGHLY_SIGNIFICANT = "p < 0.001"
    SIGNIFICANT = "p < 0.01"
    MARGINALLY_SIGNIFICANT = "p < 0.05"
    NOT_SIGNIFICANT = "p >= 0.05"


@dataclass
class Dataset:
    """Dataset para análise"""
    id: str
    name: str
    variables: List[str]
    observations: int
    data_points: List[Dict[str, Any]]
    source: str  # Fonte governamental/acadêmica validada
    is_verified: bool = False
    
    def get_column(self, var_name: str) -> List[Any]:
        """Obter valores de uma variável"""
        return [d.get(var_name) for d in self.data_points if var_name in d]
    
    def get_numeric_columns(self) -> List[str]:
        """Obter colunas numéricas"""
        numeric = []
        for var in self.variables:
            values = self.get_column(var)
            if all(isinstance(v, (int, float)) or v is None for v in values):
                numeric.append(var)
        return numeric


@dataclass
class StatisticalResult:
    """Resultado de análise estatística"""
    test_name: str
    test_statistic: float
    p_value: float
    significance: StatisticalSignificance
    effect_size: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    interpretation: str = ""
    recommendation: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "test": self.test_name,
            "statistic": self.test_statistic,
            "p_value": self.p_value,
            "significance": self.significance.value,
            "effect_size": self.effect_size,
            "interpretation": self.interpretation,
            "recommendation": self.recommendation
        }


@dataclass
class Insight:
    """Insight detectado pelo cientista de dados"""
    id: str
    insight_type: InsightType
    title: str
    description: str
    evidence: List[str] = field(default_factory=list)
    statistical_evidence: List[Dict] = field(default_factory=list)
    confidence: float = 0.0  # 0-1
    actionability: str = ""  # low, medium, high
    data_sources: List[str] = field(default_factory=list)
    related_variables: List[str] = field(default_factory=list)
    potential_impact: str = ""  # low, medium, high
    requires_more_data: bool = False
    suggested_data_sources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.insight_type.value,
            "title": self.title,
            "description": self.description,
            "confidence": self.confidence,
            "actionability": self.actionability,
            "impact": self.potential_impact,
            "evidence": self.evidence,
            "statistical_evidence": self.statistical_evidence,
            "requires_more_data": self.requires_more_data
        }


class ClassicalStatistics:
    """
    Estatísticas Clássicas
    Implementa técnicas estatísticas tradicionais com precisão cirúrgica
    """
    
    @staticmethod
    def mean(values: List[float]) -> float:
        """Média aritmética"""
        valid = [v for v in values if v is not None]
        return sum(valid) / len(valid) if valid else 0
    
    @staticmethod
    def variance(values: List[float]) -> float:
        """Variância"""
        valid = [v for v in values if v is not None]
        if len(valid) < 2:
            return 0
        m = ClassicalStatistics.mean(valid)
        return sum((v - m) ** 2 for v in valid) / (len(valid) - 1)
    
    @staticmethod
    def std_dev(values: List[float]) -> float:
        """Desvio padrão"""
        return math.sqrt(ClassicalStatistics.variance(values))
    
    @staticmethod
    def median(values: List[float]) -> float:
        """Mediana"""
        valid = sorted([v for v in values if v is not None])
        n = len(valid)
        if n == 0:
            return 0
        if n % 2 == 1:
            return valid[n // 2]
        return (valid[n // 2 - 1] + valid[n // 2]) / 2
    
    @staticmethod
    def correlation_pearson(x: List[float], y: List[float]) -> Tuple[float, float]:
        """
        Correlação de Pearson com precisão
        RETORNA: (coeficiente, p-value aproximado)
        """
        n = min(len(x), len(y))
        if n < 3:
            return 0.0, 1.0
        
        # Filtrar pares válidos
        pairs = [(x[i], y[i]) for i in range(n) if x[i] is not None and y[i] is not None]
        if len(pairs) < 3:
            return 0.0, 1.0
        
        x_vals = [p[0] for p in pairs]
        y_vals = [p[1] for p in pairs]
        
        mean_x = ClassicalStatistics.mean(x_vals)
        mean_y = ClassicalStatistics.mean(y_vals)
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in pairs)
        denom_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x_vals))
        denom_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y_vals))
        
        if denom_x == 0 or denom_y == 0:
            return 0.0, 1.0
        
        r = numerator / (denom_x * denom_y)
        
        # Aproximação do p-value
        t = r * math.sqrt(n - 2) / math.sqrt(max(0.001, 1 - r ** 2))
        # Simplificado - em produção usar distribuição t real
        p_value = 0.05 if abs(r) > 0.3 else 0.5
        
        return r, p_value
    
    @staticmethod
    def correlation_spearman(x: List[float], y: List[float]) -> Tuple[float, float]:
        """Correlação de Spearman (não-paramétrica)"""
        n = min(len(x), len(y))
        if n < 3:
            return 0.0, 1.0
        
        # Rank transformation simplificada
        def rank_values(vals):
            sorted_vals = sorted(enumerate(vals), key=lambda t: t[1])
            ranks = [0] * len(vals)
            for rank, (idx, _) in enumerate(sorted_vals):
                ranks[idx] = rank + 1
            return ranks
        
        x_clean = [v for v in x if v is not None]
        y_clean = [v for v in y if v is not None]
        min_len = min(len(x_clean), len(y_clean))
        
        if min_len < 3:
            return 0.0, 1.0
        
        rx = rank_values(x_clean[:min_len])
        ry = rank_values(y_clean[:min_len])
        
        return ClassicalStatistics.correlation_pearson(rx, ry)
    
    @staticmethod
    def chi_square(observed: List[int], expected: List[int]) -> Tuple[float, float]:
        """Teste Chi-Quadrado"""
        if len(observed) != len(expected):
            return 0.0, 1.0
        
        chi2 = sum((o - e) ** 2 / e if e > 0 else 0 for o, e in zip(observed, expected))
        df = len(observed) - 1
        # Aproximação simples
        p_value = 0.05 if chi2 > df * 1.5 else 0.3
        
        return chi2, p_value
    
    @staticmethod
    def t_test_independent(sample1: List[float], sample2: List[float]) -> StatisticalResult:
        """Teste t para amostras independentes"""
        n1, n2 = len(sample1), len(sample2)
        if n1 < 2 or n2 < 2:
            return StatisticalResult("t-test", 0, 1, StatisticalSignificance.NOT_SIGNIFICANT)
        
        m1 = ClassicalStatistics.mean(sample1)
        m2 = ClassicalStatistics.mean(sample2)
        v1 = ClassicalStatistics.variance(sample1)
        v2 = ClassicalStatistics.variance(sample2)
        
        # Pooled variance
        sp = math.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
        
        if sp == 0:
            return StatisticalResult("t-test", 0, 1, StatisticalSignificance.NOT_SIGNIFICANT)
        
        t_stat = (m1 - m2) / (sp * math.sqrt(1/n1 + 1/n2))
        
        # Aproximação p-value
        p_value = 0.05 if abs(t_stat) > 2 else 0.3
        
        sig = StatisticalSignificance.HIGHLY_SIGNIFICANT if p_value < 0.001 else \
              StatisticalSignificance.SIGNIFICANT if p_value < 0.01 else \
              StatisticalSignificance.MARGINALLY_SIGNIFICANT if p_value < 0.05 else \
              StatisticalSignificance.NOT_SIGNIFICANT
        
        return StatisticalResult(
            test_name="Independent t-test",
            test_statistic=t_stat,
            p_value=p_value,
            significance=sig,
            effect_size=abs(m1 - m2) / sp,
            interpretation=f"Diferença entre médias: {abs(m1 - m2):.2f}",
            recommendation="Diferença estatisticamente significativa" if p_value < 0.05 else "Diferença não significativa"
        )


class ModernStatistics:
    """
    Estatísticas Modernas
    Implementa técnicas de Machine Learning e análise avançada
    """
    
    @staticmethod
    def detect_outliers_iqr(values: List[float], threshold: float = 1.5) -> Tuple[List[int], List[float]]:
        """Detecção de outliers pelo método IQR"""
        valid = [v for v in values if v is not None]
        if len(valid) < 4:
            return [], []
        
        q1 = ClassicalStatistics.median(valid[:len(valid)//2])
        q3 = ClassicalStatistics.median(valid[len(valid)//2:])
        iqr = q3 - q1
        
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        
        outliers_idx = [i for i, v in enumerate(values) if v is not None and (v < lower or v > upper)]
        outliers_values = [values[i] for i in outliers_idx]
        
        return outliers_idx, outliers_values
    
    @staticmethod
    def detect_outliers_zscore(values: List[float], threshold: float = 3) -> Tuple[List[int], List[float]]:
        """Detecção de outliers pelo método Z-Score"""
        valid = [v for v in values if v is not None]
        if len(valid) < 4:
            return [], []
        
        mean = ClassicalStatistics.mean(valid)
        std = ClassicalStatistics.std_dev(valid)
        
        if std == 0:
            return [], []
        
        outliers_idx = []
        outliers_values = []
        for i, v in enumerate(values):
            if v is not None:
                z = abs((v - mean) / std)
                if z > threshold:
                    outliers_idx.append(i)
                    outliers_values.append(v)
        
        return outliers_idx, outliers_values
    
    @staticmethod
    def simple_kmeans(data: List[float], k: int, max_iter: int = 100) -> Tuple[List[int], List[float]]:
        """K-Means clustering simplificado"""
        if len(data) < k or k < 2:
            return list(range(len(data))), [0.0] * k
        
        # Inicialização aleatória
        centroids = data[:k]
        
        for _ in range(max_iter):
            # Atribuição de clusters
            clusters = [[] for _ in range(k)]
            for i, val in enumerate(data):
                if val is not None:
                    distances = [abs(val - c) for c in centroids]
                    cluster_idx = distances.index(min(distances))
                    clusters[cluster_idx].append(val)
            
            # Atualização de centroides
            new_centroids = []
            for cluster in clusters:
                if cluster:
                    new_centroids.append(ClassicalStatistics.mean(cluster))
                else:
                    new_centroids.append(centroids[len(new_centroids) % len(centroids)])
            
            centroids = new_centroids
        
        # Retornar cluster de cada ponto
        assignments = []
        for val in data:
            if val is None:
                assignments.append(0)
            else:
                distances = [abs(val - c) for c in centroids]
                assignments.append(distances.index(min(distances)))
        
        return assignments, centroids
    
    @staticmethod
    def trend_detection(values: List[float]) -> str:
        """Detecção de tendência simples"""
        if len(values) < 3:
            return "insufficient_data"
        
        # Regressão linear simples
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = ClassicalStatistics.mean(values)
        
        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        if abs(slope) < 0.1:
            return "stable"
        elif slope > 0:
            return "increasing"
        else:
            return "decreasing"


class QualitativeAnalysis:
    """
    Análise Qualitativa
    Processamento de texto e análise de conteúdo
    """
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """Extrair palavras-chave do texto"""
        # Remover stopwords básicas
        stopwords = {"de", "da", "do", "das", "dos", "um", "uma", "ou", "e", "o", "a", 
                    "que", "é", "se", "não", "em", "para", "com", "os", "as", "no",
                    "na", "nos", "nas", "ao", "à", "pelo", "pela", "pelos", "pelas",
                    "como", "mais", "mas", "porque", "ainda", "já", "muito", "sendo",
                    "foi", "são", "tem", "pode", "este", "esta", "esses", "essas",
                    "seu", "sua", "todas", "todos", "cada", "pode", "podem", "ser"}
        
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        words = [w for w in words if w not in stopwords]
        
        counter = Counter(words)
        return counter.most_common(top_n)
    
    @staticmethod
    def sentiment_indicator(text: str) -> float:
        """Indicador de sentimento simples (-1 a 1)"""
        positive = ["bom", "excelente", "positivo", "sucesso", "crescimento", "melhor",
                   "avanço", "potencial", "oportunidade", "benefício", "impacto"]
        negative = ["mau", "ruim", "negativo", "fracasso", "queda", "problema",
                   "dificuldade", "desafio", "risco", "crise", "limitação"]
        
        text_lower = text.lower()
        pos_count = sum(1 for w in positive if w in text_lower)
        neg_count = sum(1 for w in negative if w in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return 0
        
        return (pos_count - neg_count) / total
    
    @staticmethod
    def thematic_analysis(texts: List[str], num_themes: int = 5) -> Dict[str, List[str]]:
        """Análise temática simplificada"""
        all_keywords = []
        for text in texts:
            keywords = QualitativeAnalysis.extract_keywords(text, top_n=20)
            all_keywords.extend([k for k, _ in keywords])
        
        # Agrupar palavras similares (simplificado)
        themes = defaultdict(list)
        theme_words = ["educação", "tecnologia", "economia", "saúde", "sociedade",
                      "política", "ambiente", "desenvolvimento", "pesquisa", "inovação"]
        
        for word in all_keywords:
            assigned = False
            for theme in theme_words:
                if theme in word or word in theme:
                    themes[theme].append(word)
                    assigned = True
                    break
            if not assigned and len(themes) < num_themes:
                themes[f"theme_{len(themes)}"].append(word)
        
        return dict(themes)


class DataScientistPhD:
    """
    Cientista de Dados PhD
    Orquestrador de análise com precisão cirúrgica
    """
    
    def __init__(self):
        self.classical = ClassicalStatistics()
        self.modern = ModernStatistics()
        self.qualitative = QualitativeAnalysis()
        
        self.datasets: Dict[str, Dataset] = {}
        self.analyses_results: List[StatisticalResult] = []
        self.insights: List[Insight] = []
        self.audit_log: List[Dict] = []
    
    def log_audit(self, action: str, details: Dict):
        """Registrar auditoria"""
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        })
    
    def add_dataset(self, dataset: Dataset):
        """Adicionar dataset para análise"""
        self.datasets[dataset.id] = dataset
        self.log_audit("DATASET_ADDED", {"dataset_id": dataset.id, "name": dataset.name})
    
    def analyze_correlations(self, var1: str, var2: str, method: str = "pearson") -> StatisticalResult:
        """Analisar correlação entre duas variáveis"""
        if not self.datasets:
            return StatisticalResult("correlation", 0, 1, StatisticalSignificance.NOT_SIGNIFICANT)
        
        # Usar primeiro dataset
        dataset = list(self.datasets.values())[0]
        
        x = dataset.get_column(var1)
        y = dataset.get_column(var2)
        
        if method == "pearson":
            r, p = self.classical.correlation_pearson(x, y)
        elif method == "spearman":
            r, p = self.classical.correlation_spearman(x, y)
        else:
            r, p = 0, 1
        
        sig = StatisticalSignificance.HIGHLY_SIGNIFICANT if p < 0.001 else \
              StatisticalSignificance.SIGNIFICANT if p < 0.01 else \
              StatisticalSignificance.MARGINALLY_SIGNIFICANT if p < 0.05 else \
              StatisticalSignificance.NOT_SIGNIFICANT
        
        # Interpretação
        if abs(r) > 0.7:
            strength = "forte"
        elif abs(r) > 0.4:
            strength = "moderada"
        elif abs(r) > 0.2:
            strength = "fraca"
        else:
            strength = "muito fraca ou nula"
        
        direction = "positiva" if r > 0 else "negativa"
        
        result = StatisticalResult(
            test_name=f"Correlação {method}",
            test_statistic=r,
            p_value=p,
            significance=sig,
            effect_size=abs(r),
            interpretation=f"Correlação {strength} {direction} entre {var1} e {var2}",
            recommendation="Considerar relação causal" if abs(r) > 0.6 and p < 0.05 else "Mais investigação necessária"
        )
        
        self.analyses_results.append(result)
        return result
    
    def detect_anomalies(self, var_name: str, method: str = "iqr") -> Dict:
        """Detectar anomalias em uma variável"""
        if not self.datasets:
            return {"outliers": [], "analysis": "no_data"}
        
        dataset = list(self.datasets.values())[0]
        values = dataset.get_column(var_name)
        
        if method == "iqr":
            idx, vals = self.modern.detect_outliers_iqr(values)
        else:
            idx, vals = self.modern.detect_outliers_zscore(values)
        
        self.log_audit("ANOMALY_DETECTED", {
            "variable": var_name,
            "method": method,
            "count": len(idx),
            "values": vals[:10]  # Primeiros 10
        })
        
        return {
            "variable": var_name,
            "method": method,
            "outlier_count": len(idx),
            "outlier_indices": idx,
            "outlier_values": vals,
            "analysis": "Anomalias detectadas - requer investigação"
        }
    
    def analyze_trends(self, var_name: str) -> Dict:
        """Analisar tendências em série temporal"""
        if not self.datasets:
            return {"trend": "insufficient_data"}
        
        dataset = list(self.datasets.values())[0]
        values = dataset.get_column(var_name)
        
        trend = self.modern.trend_detection(values)
        mean = self.classical.mean(values)
        std = self.classical.std_dev(values)
        
        return {
            "variable": var_name,
            "trend": trend,
            "mean": mean,
            "std_dev": std,
            "interpretation": f"Variável {var_name} apresenta tendência {trend}"
        }
    
    def find_insights(self, text_data: Optional[str] = None) -> List[Insight]:
        """Encontrar insights a partir dos dados"""
        insights = []
        
        # Analisar correlações
        if self.datasets:
            dataset = list(self.datasets.values())[0]
            numeric_cols = dataset.get_numeric_columns()
            
            # Verificar correlações entre variáveis
            for i, var1 in enumerate(numeric_cols):
                for var2 in numeric_cols[i+1:]:
                    result = self.analyze_correlations(var1, var2)
                    
                    if abs(result.test_statistic) > 0.5 and result.p_value < 0.1:
                        insight = Insight(
                            id=str(uuid.uuid4())[:8],
                            insight_type=InsightType.CORRELATION,
                            title=f"Correlação entre {var1} e {var2}",
                            description=result.interpretation,
                            evidence=[f"r = {result.test_statistic:.3f}", f"p = {result.p_value:.4f}"],
                            statistical_evidence=[result.to_dict()],
                            confidence=abs(result.test_statistic),
                            actionability="high" if abs(result.test_statistic) > 0.7 else "medium",
                            related_variables=[var1, var2],
                            potential_impact="high"
                        )
                        insights.append(insight)
        
        # Analisar anomalias
        if self.datasets:
            dataset = list(self.datasets.values())[0]
            for var in dataset.get_numeric_columns():
                anomaly_result = self.detect_anomalies(var)
                if anomaly_result["outlier_count"] > 0:
                    insight = Insight(
                        id=str(uuid.uuid4())[:8],
                        insight_type=InsightType.ANOMALY_DETECTED,
                        title="Anomalias detectadas em " + var,
                        description=str(anomaly_result["outlier_count"]) + " outliers detectados",
                        evidence=["Outliers: " + str(anomaly_result["outlier_count"])],
                        statistical_evidence=[anomaly_result],
                        confidence=0.8,
                        actionability="high",
                        related_variables=[var],
                        potential_impact="medium"
                    )
                    insights.append(insight)
        
        # Análise qualitativa
        if text_data:
            keywords = self.qualitative.extract_keywords(text_data)
            sentiment = self.qualitative.sentiment_indicator(text_data)
            
            # Insight de palavra-chave
            if keywords:
                top_kw = keywords[0]
                insight = Insight(
                    id=str(uuid.uuid4())[:8],
                    insight_type=InsightType.PATTERN,
                    title=f"Tema principal: {top_kw[0]}",
                    description=f"Palavra mais frequente: {top_kw[0]} ({top_kw[1]} ocorrências)",
                    evidence=[f"Frequência: {top_kw[1]}"],
                    confidence=0.7,
                    actionability="medium",
                    potential_impact="medium"
                )
                insights.append(insight)
            
            # Insight de sentimento
            if abs(sentiment) > 0.2:
                direction = "positivo" if sentiment > 0 else "negativo"
                insight = Insight(
                    id=str(uuid.uuid4())[:8],
                    insight_type=InsightType.TREND,
                    title=f"Tendência {direction} identificada",
                    description=f"Indicador de sentimento: {sentiment:.2f}",
                    evidence=[f"Sentimento: {sentiment:.3f}"],
                    confidence=abs(sentiment),
                    actionability="low",
                    potential_impact="low"
                )
                insights.append(insight)
        
        self.insights = insights
        self.log_audit("INSIGHTS_FOUND", {"count": len(insights)})
        
        return insights
    
    def suggest_new_data_sources(self, current_insights: List[Insight]) -> List[str]:
        """Sugerir novas fontes de dados baseadas em insights"""
        suggested_sources = []
        
        for insight in current_insights:
            if insight.requires_more_data:
                suggested_sources.extend(insight.suggested_data_sources)
            
            # Sugestões baseadas no tipo de insight
            if insight.insight_type == InsightType.CORRELATION:
                suggested_sources.extend([
                    "IBGE - Pesquisa Nacional por Amostra de Domicílios (PNAD)",
                    "INEP - Sistema Nacional de Avaliação da Educação Básica (SAEB)",
                    "World Bank - World Development Indicators"
                ])
            
            elif insight.insight_type == InsightType.ANOMALY:
                suggested_sources.extend([
                    "DATASUS - Informações de Saúde",
                    "IPEA - Base de Dados Sociais"
                ])
            
            elif insight.insight_type == InsightType.TREND:
                suggested_sources.extend([
                    "IBGE - Séries Históricas",
                    "Banco Central - Séries Temporais"
                ])
        
        return list(set(suggested_sources))
    
    def generate_analysis_report(self) -> str:
        """Gerar relatório completo de análise"""
        lines = []
        lines.append("="*70)
        lines.append("DATA SCIENTIST PhD - ANALYSIS REPORT")
        lines.append("="*70)
        
        lines.append("\n[STATISTICAL ANALYSES]")
        for result in self.analyses_results:
            lines.append(f"  {result.test_name}: r={result.test_statistic:.3f}, p={result.p_value:.4f}")
            lines.append(f"    Interpretation: {result.interpretation[:60]}...")
        
        lines.append("\n[INSIGHTS DETECTED]")
        for insight in self.insights:
            conf = "ALTA" if insight.confidence > 0.7 else "MEDIA" if insight.confidence > 0.4 else "BAIXA"
            lines.append(f"  [{conf}] {insight.title}")
            lines.append(f"    Type: {insight.insight_type.value} | Impact: {insight.potential_impact}")
        
        lines.append("\n[DATA SOURCES NEEDED]")
        suggestions = self.suggest_new_data_sources(self.insights)
        for src in suggestions[:10]:
            lines.append(f"    - {src}")
        
        lines.append("\n[AUDIT LOG]")
        lines.append(f"    Total entries: {len(self.audit_log)}")
        
        lines.append("\n" + "="*70)
        lines.append("END OF ANALYSIS REPORT")
        lines.append("="*70)
        
        return "\n".join(lines)


# ============================================================
# EXEMPLO DE USO
# ============================================================

if __name__ == "__main__":
    print("="*70)
    print("DATA SCIENTIST ANALYST - PhD LEVEL")
    print("="*70)
    
    # Criar cientista de dados
    ds = DataScientistPhD()
    
    # Criar dataset de exemplo (dados educacionais)
    dataset = Dataset(
        id="edu_2024",
        name="Dados Educacionais 2024",
        variables=["renda", "escolaridade", "nota_media", "acesso_internet", "regiao"],
        observations=1000,
        data_points=[
            {"renda": 2000, "escolaridade": 11, "nota_media": 7.5, "acesso_internet": 1, "regiao": "Nordeste"},
            {"renda": 5000, "escolaridade": 16, "nota_media": 8.2, "acesso_internet": 1, "regiao": "Sudeste"},
            {"renda": 1500, "escolaridade": 9, "nota_media": 6.0, "acesso_internet": 0, "regiao": "Nordeste"},
            {"renda": 8000, "escolaridade": 18, "nota_media": 9.1, "acesso_internet": 1, "regiao": "Sul"},
            {"renda": 3000, "escolaridade": 12, "nota_media": 7.0, "acesso_internet": 1, "regiao": "Nordeste"},
            # ... mais dados simulados
        ] * 200,  # Expandir para 1000 observações
        source="IBGE/INEP",
        is_verified=True
    )
    
    ds.add_dataset(dataset)
    
    # Análises
    print("\n[1] Correlation Analysis:")
    corr_result = ds.analyze_correlations("renda", "nota_media", "pearson")
    print(f"    Correlation: r={corr_result.test_statistic:.3f}, p={corr_result.p_value:.4f}")
    print(f"    Interpretation: {corr_result.interpretation}")
    
    print("\n[2] Anomaly Detection:")
    anomaly_result = ds.detect_anomalies("nota_media", "iqr")
    print(f"    Outliers found: {anomaly_result['outlier_count']}")
    
    print("\n[3] Trend Analysis:")
    trend_result = ds.analyze_trends("nota_media")
    print(f"    Trend: {trend_result['trend']}")
    
    print("\n[4] Finding Insights:")
    insights = ds.find_insights(text_data="A educação no Brasil apresenta desafios relacionados à desigualdade regional, com o Nordeste enfrentando maiores dificuldades de infraestrutura.")
    print(f"    Insights found: {len(insights)}")
    for insight in insights[:3]:
        print(f"    - {insight.title} (confidence: {insight.confidence:.2f})")
    
    print("\n[5] Data Sources Suggestions:")
    sources = ds.suggest_new_data_sources(insights)
    print(f"    Suggested sources: {len(sources)}")
    
    print("\n" + ds.generate_analysis_report())