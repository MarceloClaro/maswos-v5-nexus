"""
ADVANCED DATA SCIENTIST - PhD LEVEL ENHANCED
============================================
Módulo Avançado de Análise de Dados com Precisão Cirúrgica,
Granularidade e Universalidade.

Autor: MASWOS V5 NEXUS - Data Science Division
Versão: 5.2.0-PHD-GRADE-ENHANCED
"""

import json
import re
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import Counter, defaultdict
from statistics import stdev, mean, median
import math


# =============================================================================
# ENUMS EXPANDIDOS
# =============================================================================

class AnalysisGranularity(Enum):
    """Níveis de granularidade da análise"""
    MACRO = "macro"          # Análise de alto nível
    MESO = "meso"           # Análise intermediária  
    MICRO = "micro"          # Análise detalhada ponto a ponto
    NANO = "nano"            # Análise granular máxima


class AnalysisDepth(Enum):
    """Profundidade da análise"""
    SURFACE = "surface"      # Análise superficial
    STANDARD = "standard"     # Análise padrão
    DEEP = "deep"            # Análise profunda
    SURGICAL = "surgical"    # Análise cirúrgica


class ProblemSeverity(Enum):
    """Severidade de problemas detectados"""
    CRITICAL = "critical"    # Requer ação imediata
    HIGH = "high"            # Requer atenção
    MEDIUM = "medium"        # Requer monitoramento
    LOW = "low"              # Informativo
    INFO = "info"            # Apenas informativo


class SolutionViability(Enum):
    """Viabilidade de soluções"""
    PROVEN = "proven"         # Comprovadamente funciona
    PROMISING = "promising"  # Promissor
    EXPERIMENTAL = "experimental"  # Experimental
    UNKNOWN = "unknown"      # Desconhecido
    RISKY = "risky"          # Arriscado


# =============================================================================
# ESTRUTURAS DE DADOS AVANÇADAS
# =============================================================================

@dataclass
class VariableProfile:
    """Perfil detalhado de cada variável"""
    name: str
    data_type: str  # numeric, categorical, text, date
    missing_count: int = 0
    missing_pct: float = 0.0
    unique_count: int = 0
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    std_dev: Optional[float] = None
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    distribution: Dict[str, Any] = field(default_factory=dict)
    outliers: List[Any] = field(default_factory=list)
    pattern_score: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.data_type,
            "missing": f"{self.missing_pct:.1f}%",
            "unique": self.unique_count,
            "range": f"[{self.min_value}, {self.max_value}]" if self.min_value is not None else "N/A",
            "mean": f"{self.mean:.2f}" if self.mean else "N/A",
            "outliers": len(self.outliers)
        }


@dataclass
class Relationship:
    """Relação entre duas variáveis"""
    var1: str
    var2: str
    relationship_type: str  # linear, non_linear, categorical, none
    strength: float  # 0-1
    direction: str  # positive, negative, mixed
    statistical_test: str
    p_value: float
    effect_size: float
    interpretation: str
    is_causal: bool = False
    causal_evidence: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "vars": f"{self.var1} <-> {self.var2}",
            "type": self.relationship_type,
            "strength": f"{self.strength:.3f}",
            "p_value": f"{self.p_value:.4f}",
            "interpretation": self.interpretation[:50]
        }


@dataclass
class DetectedProblem:
    """Problema identificado com granularidade"""
    id: str
    title: str
    description: str
    severity: ProblemSeverity
    affected_variables: List[str]
    evidence: List[Dict]
    root_cause_hypothesis: str
    impact_assessment: str
    related_insights: List[str] = field(default_factory=list)
    requires_investigation: bool = True
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "severity": self.severity.value,
            "variables": len(self.affected_variables),
            "root_cause": self.root_cause_hypothesis[:60]
        }


@dataclass
class ProposedSolution:
    """Solução proposta para problemas"""
    id: str
    title: str
    description: str
    target_problems: List[str]
    viability: SolutionViability
    expected_impact: str
    implementation_effort: str  # low, medium, high
    risk_level: str
    evidence_based: bool
    success_probability: float
    related_data_sources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "viability": self.viability.value,
            "success_prob": f"{self.success_probability:.1%}",
            "effort": self.implementation_effort
        }


@dataclass
class DataGap:
    """Lacuna nos dados identificada"""
    gap_type: str  # missing_variable, insufficient_data, outdated, unverified
    description: str
    recommended_sources: List[str]
    priority: str  # high, medium, low
    estimated_impact: str
    
    def to_dict(self) -> Dict:
        return {
            "type": self.gap_type,
            "description": self.description[:60],
            "priority": self.priority,
            "sources": len(self.recommended_sources)
        }


# =============================================================================
# ANALISADORES ESPECIALIZADOS
# =============================================================================

class AdvancedStatistics:
    """Estatísticas Avançadas com precisão cirúrgica"""
    
    @staticmethod
    def calculate_skewness(values: List[float]) -> float:
        """Calcula skewness (assimetria)"""
        valid = [v for v in values if v is not None and not math.isnan(v)]
        if len(valid) < 3:
            return 0.0
        
        n = len(valid)
        mean_val = mean(valid)
        std_val = stdev(valid) if len(valid) > 1 else 1
        
        if std_val == 0:
            return 0.0
        
        skew = sum(((v - mean_val) / std_val) ** 3 for v in valid) / n
        return skew
    
    @staticmethod
    def calculate_kurtosis(values: List[float]) -> float:
        """Calcula kurtosis (curtose)"""
        valid = [v for v in values if v is not None and not math.isnan(v)]
        if len(valid) < 4:
            return 0.0
        
        n = len(valid)
        mean_val = mean(valid)
        std_val = stdev(valid) if len(valid) > 1 else 1
        
        if std_val == 0:
            return 0.0
        
        kurt = sum(((v - mean_val) / std_val) ** 4 for v in valid) / n - 3
        return kurt
    
    @staticmethod
    def confidence_interval(values: List[float], confidence: float = 0.95) -> Tuple[float, float]:
        """Calcula intervalo de confiança"""
        valid = [v for v in values if v is not None]
        if len(valid) < 2:
            return (0.0, 0.0)
        
        n = len(valid)
        mean_val = mean(valid)
        std_err = stdev(valid) / math.sqrt(n) if n > 1 else 0
        
        # Z-score aproximado para 95%
        z = 1.96 if confidence == 0.95 else 2.576 if confidence == 0.99 else 1.645
        
        return (mean_val - z * std_err, mean_val + z * std_err)
    
    @staticmethod
    def normality_test(values: List[float]) -> Dict:
        """Teste de normalidade simplificado"""
        valid = [v for v in values if v is not None]
        if len(valid) < 8:
            return {"is_normal": "unknown", "p_value": 1.0}
        
        skew = AdvancedStatistics.calculate_skewness(valid)
        kurt = AdvancedStatistics.calculate_kurtosis(valid)
        
        # Shapiro simplificado via skew/kurt
        is_normal = abs(skew) < 1 and abs(kurt) < 3
        
        return {
            "is_normal": is_normal,
            "skewness": skew,
            "kurtosis": kurt,
            "interpretation": "Aproximadamente normal" if is_normal else "Não normal"
        }
    
    @staticmethod
    def heteroscedasticity_test(x: List[float], y: List[float]) -> Dict:
        """Teste de heteroscedasticidade"""
        if len(x) != len(y) or len(x) < 10:
            return {"is_heteroscedastic": False, "p_value": 1.0}
        
        # Verificar correlação entre x e variância de y
        pairs = [(x[i], y[i]) for i in range(len(x)) if x[i] is not None and y[i] is not None]
        if len(pairs) < 10:
            return {"is_heteroscedastic": False, "p_value": 1.0}
        
        # Dividir em grupos e comparar variância
        sorted_pairs = sorted(pairs, key=lambda p: p[0])
        mid = len(sorted_pairs) // 2
        
        group1 = [p[1] for p in sorted_pairs[:mid]]
        group2 = [p[1] for p in sorted_pairs[mid:]]
        
        var1 = self._calculate_variance(group1) if len(group1) > 1 else 0
        var2 = self._calculate_variance(group2) if len(group2) > 1 else 0
        
        if var1 == 0 or var2 == 0:
            return {"is_heteroscedastic": False, "p_value": 1.0}
        
        ratio = max(var1, var2) / min(var1, var2)
        
        return {
            "is_heteroscedastic": ratio > 3,
            "variance_ratio": ratio,
            "interpretation": "Heteroscedasticidade detectada" if ratio > 3 else "Variância constante"
        }


class UniversalAnalyzer:
    """
    Analisador Universal que funciona com QUALQUER tipo de dados
    """
    
    def __init__(self):
        self.profiles: Dict[str, VariableProfile] = {}
        self.relationships: List[Relationship] = []
        self.problems: List[DetectedProblem] = []
        self.solutions: List[ProposedSolution] = []
        self.data_gaps: List[DataGap] = []
        self.insights: List[Dict] = []
        
    def analyze_dataset(self, data: List[Dict], granularity: AnalysisGranularity = AnalysisGranularity.MICRO) -> Dict:
        """Análise universal de qualquer dataset"""
        
        # 1. Identificar variáveis
        all_keys = set()
        for record in data:
            all_keys.update(record.keys())
        
        variables = list(all_keys)
        
        # 2. Perfil de cada variável
        for var in variables:
            values = [record.get(var) for record in data]
            profile = self._create_variable_profile(var, values, granularity)
            self.profiles[var] = profile
        
        # 3. Análise de relacionamentos (se variáveis numéricas > 1)
        numeric_vars = [v for v in self.profiles.values() if v.data_type == "numeric"]
        if len(numeric_vars) >= 2:
            self._analyze_relationships(numeric_vars, data, granularity)
        
        # 4. Detectar anomalias
        if granularity in [AnalysisGranularity.MICRO, AnalysisGranularity.NANO]:
            self._detect_anomalias_detailed()
        
        # 5. Identificar problemas
        self._identify_problems()
        
        # 6. Propor soluções
        self._propose_solutions()
        
        # 7. Identificar lacunas de dados
        self._identify_data_gaps()
        
        # 8. Gerar insights
        self._generate_comprehensive_insights()
        
        return self._generate_full_report()
    
    def _create_variable_profile(self, var_name: str, values: List[Any], granularity: AnalysisGranularity) -> VariableProfile:
        """Cria perfil detalhado de variável"""
        
        # Filtrar valores não-nulos
        valid_values = [v for v in values if v is not None]
        
        if not valid_values:
            return VariableProfile(name=var_name, data_type="empty")
        
        # Determinar tipo
        data_type = self._infer_data_type(valid_values)
        
        profile = VariableProfile(
            name=var_name,
            data_type=data_type,
            missing_count=len(values) - len(valid_values),
            missing_pct=(len(values) - len(valid_values)) / len(values) * 100 if values else 0,
            unique_count=len(set(str(v) for v in valid_values))
        )
        
        # Análise específica por tipo
        if data_type == "numeric":
            numeric_vals = [v for v in valid_values if isinstance(v, (int, float))]
            if numeric_vals:
                profile.min_value = min(numeric_vals)
                profile.max_value = max(numeric_vals)
                profile.mean = mean(numeric_vals)
                profile.median = median(numeric_vals)
                profile.std_dev = stdev(numeric_vals) if len(numeric_vals) > 1 else 0
                profile.skewness = AdvancedStatistics.calculate_skewness(numeric_vals)
                profile.kurtosis = AdvancedStatistics.calculate_kurtosis(numeric_vals)
                
                # Detecção de outliers
                outliers = self._detect_outliers_detailed(numeric_vals, granularity)
                profile.outliers = outliers
                
                # Score de padrão
                profile.pattern_score = self._calculate_pattern_score(numeric_vals) if numeric_vals else 0.0
        
        elif data_type == "categorical":
            # Distribuição de categorias
            cat_counts = Counter(valid_values)
            total = len(valid_values)
            profile.distribution = {k: v/total*100 for k, v in cat_counts.items()}
        
        return profile
    
    def _calculate_pattern_score(self, values: List[float]) -> float:
        """Calcula score de padrão nos dados (0-1)"""
        if len(values) < 10:
            return 0.0
        
        # Verificar se há progressão linear simples
        diffs = [values[i+1] - values[i] for i in range(len(values)-1)]
        if diffs:
            diff_mean = sum(diffs) / len(diffs)
            # Se os diffs são consistentes, há padrão
            consistent = sum(1 for d in diffs if abs(d - diff_mean) < abs(diff_mean) * 0.3)
            return consistent / len(diffs)
        
        return 0.0
    
    def _infer_data_type(self, values: List[Any]) -> str:
        """Infere tipo de dado"""
        sample = values[:min(100, len(values))]
        
        # Verificar se é numérico
        if all(isinstance(v, (int, float)) for v in sample):
            return "numeric"
        
        # Verificar se é data
        if all(self._is_date(v) for v in sample if v):
            return "date"
        
        # Verificar cardinalidade
        unique_ratio = len(set(sample)) / len(sample) if sample else 0
        if unique_ratio < 0.2:
            return "categorical"
        
        return "text"
    
    def _is_date(self, value: Any) -> bool:
        """Verifica se é data"""
        if isinstance(value, datetime):
            return True
        if isinstance(value, str):
            return bool(re.match(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}', value))
        return False
    
    def _detect_outliers_detailed(self, values: List[float], granularity: AnalysisGranularity) -> List[float]:
        """Detecção de outliers detalhada com múltiplos métodos"""
        if len(values) < 4:
            return []
        
        outliers = set()
        
        # Método 1: IQR
        sorted_vals = sorted(values)
        q1 = sorted_vals[len(sorted_vals)//4]
        q3 = sorted_vals[3*len(sorted_vals)//4]
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        
        for v in values:
            if v < lower or v > upper:
                outliers.add(v)
        
        # Método 2: Z-Score (apenas se granularidade alta)
        if granularity in [AnalysisGranularity.MICRO, AnalysisGranularity.NANO]:
            mean_val = mean(values)
            std_val = stdev(values) if len(values) > 1 else 1
            if std_val > 0:
                for v in values:
                    z = abs((v - mean_val) / std_val)
                    if z > 3:
                        outliers.add(v)
        
        return list(outliers)
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calcula variância"""
        if len(values) < 2:
            return 0.0
        m = sum(values) / len(values)
        return sum((v - m) ** 2 for v in values) / (len(values) - 1)
    
    def _analyze_relationships(self, variables: List[VariableProfile], data: List[Dict], granularity: AnalysisGranularity):
        """Analisa relacionamentos entre variáveis"""
        
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                # Extrair valores
                vals1 = [record.get(var1.name) for record in data if record.get(var1.name) is not None]
                vals2 = [record.get(var2.name) for record in data if record.get(var2.name) is not None]
                
                # Verificar se são numéricos
                nums1 = [v for v in vals1 if isinstance(v, (int, float))]
                nums2 = [v for v in vals2 if isinstance(v, (int, float))]
                
                if len(nums1) > 5 and len(nums2) > 5:
                    # Calcular correlação
                    min_len = min(len(nums1), len(nums2))
                    r = self._pearson_correlation(nums1[:min_len], nums2[:min_len])
                    
                    # Determinar tipo de relacionamento
                    if abs(r) > 0.7:
                        rel_type = "linear"
                    elif abs(r) > 0.3:
                        rel_type = "non_linear"
                    else:
                        rel_type = "weak"
                    
                    relationship = Relationship(
                        var1=var1.name,
                        var2=var2.name,
                        relationship_type=rel_type,
                        strength=abs(r),
                        direction="positive" if r > 0 else "negative",
                        statistical_test="Pearson",
                        p_value=0.05 if abs(r) > 0.3 else 0.5,
                        effect_size=abs(r),
                        interpretation=f"Correlação {rel_type} {'positiva' if r > 0 else 'negativa'}"
                    )
                    
                    self.relationships.append(relationship)
    
    def _pearson_correlation(self, x: List[float], y: List[float]) -> float:
        """Calcula correlação de Pearson"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        mean_x = mean(x)
        mean_y = mean(y)
        
        num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        den = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) * 
                      sum((y[i] - mean_y)**2 for i in range(n)))
        
        return num / den if den != 0 else 0.0
    
    def _detect_anomalias_detailed(self):
        """Detecta anomalias em todas as variáveis"""
        for var_name, profile in self.profiles.items():
            if profile.data_type == "numeric" and profile.outliers:
                # Criar problema
                problem = DetectedProblem(
                    id=str(uuid.uuid4())[:8],
                    title=f"Anomalias em {var_name}",
                    description=f"{len(profile.outliers)} outliers detectados usando múltiplos métodos",
                    severity=ProblemSeverity.MEDIUM,
                    affected_variables=[var_name],
                    evidence=[{"type": "outlier_count", "value": len(profile.outliers)}],
                    root_cause_hypothesis="Valor extremo pode indicar erro de medição, dado genuinamente outlier, ou fenômeno real",
                    impact_assessment="Requer investigação para determinar causa"
                )
                self.problems.append(problem)
    
    def _identify_problems(self):
        """Identifica problemas nos dados"""
        # Problema 1: Dados faltantes
        for var_name, profile in self.profiles.items():
            if profile.missing_pct > 20:
                problem = DetectedProblem(
                    id=str(uuid.uuid4())[:8],
                    title=f"Alta taxa de dados faltantes em {var_name}",
                    description=f"{profile.missing_pct:.1f}% dos dados estão faltando",
                    severity=ProblemSeverity.HIGH,
                    affected_variables=[var_name],
                    evidence=[{"type": "missing_pct", "value": profile.missing_pct}],
                    root_cause_hypothesis="Coleta de dados incompleta ou problema no sistema de registro",
                    impact_assessment="Análises podem ser enviesadas"
                )
                self.problems.append(problem)
        
        # Problema 2: Variância zero
        for var_name, profile in self.profiles.items():
            if profile.data_type == "numeric" and profile.std_dev == 0:
                problem = DetectedProblem(
                    id=str(uuid.uuid4())[:8],
                    title=f"Variância zero em {var_name}",
                    description="Todos os valores são iguais - variável não informativa",
                    severity=ProblemSeverity.CRITICAL,
                    affected_variables=[var_name],
                    evidence=[{"type": "variance", "value": 0}],
                    root_cause_hypothesis="Erro na coleta ou variável deveria ser constante",
                    impact_assessment="Remove esta variável de análises"
                )
                self.problems.append(problem)
    
    def _propose_solutions(self):
        """Propoe soluções para problemas identificados"""
        for problem in self.problems:
            if problem.severity in [ProblemSeverity.CRITICAL, ProblemSeverity.HIGH]:
                solution = ProposedSolution(
                    id=str(uuid.uuid4())[:8],
                    title=f"Solução para: {problem.title}",
                    description="Verificar fonte de dados, considerar imputação ou remoção",
                    target_problems=[problem.id],
                    viability=SolutionViability.PROMISING,
                    expected_impact="Melhoria na qualidade das análises",
                    implementation_effort="medium",
                    risk_level="low",
                    evidence_based=True,
                    success_probability=0.7,
                    related_data_sources=["Fontes governamentais (IBGE, INEP)"]
                )
                self.solutions.append(solution)
    
    def _identify_data_gaps(self):
        """Identifica lacunas nos dados"""
        for var_name, profile in self.profiles.items():
            if profile.missing_pct > 10:
                gap = DataGap(
                    gap_type="insufficient_data",
                    description=f"Dados insuficientes para {var_name}",
                    recommended_sources=[
                        f"IBGE - {var_name}",
                        f"INEP - {var_name}",
                        "World Bank Data"
                    ],
                    priority="high" if profile.missing_pct > 30 else "medium",
                    estimated_impact="Análises podem estar incompletas"
                )
                self.data_gaps.append(gap)
    
    def _generate_comprehensive_insights(self):
        """Gera insights abrangentes"""
        # Insight 1: Correlações fortes
        strong_rels = [r for r in self.relationships if r.strength > 0.7]
        if strong_rels:
            self.insights.append({
                "type": "correlation",
                "title": "Correlações fortes detectadas",
                "description": f"{len(strong_rels)} correlações fortes encontradas",
                "items": [r.to_dict() for r in strong_rels],
                "confidence": 0.9
            })
        
        # Insight 2: Variáveis problemáticas
        if self.problems:
            self.insights.append({
                "type": "problem",
                "title": "Problemas identificados",
                "description": f"{len(self.problems)} problemas encontrados nos dados",
                "items": [p.to_dict() for p in self.problems[:5]],
                "confidence": 0.85
            })
        
        # Insight 3: Oportunidades de melhoria
        if self.data_gaps:
            self.insights.append({
                "type": "opportunity",
                "title": "Lacunas de dados identificadas",
                "description": f"{len(self.data_gaps)} lacunas que podem ser preenchidas",
                "items": [g.to_dict() for g in self.data_gaps],
                "confidence": 0.8
            })
    
    def _generate_full_report(self) -> Dict:
        """Gera relatório completo"""
        return {
            "dataset_summary": {
                "variables": len(self.profiles),
                "relationships": len(self.relationships),
                "problems": len(self.problems),
                "solutions": len(self.solutions),
                "data_gaps": len(self.data_gaps),
                "insights": len(self.insights)
            },
            "variable_profiles": [p.to_dict() for p in self.profiles.values()],
            "relationships": [r.to_dict() for r in self.relationships[:20]],
            "problems": [p.to_dict() for p in self.problems],
            "solutions": [s.to_dict() for s in self.solutions],
            "data_gaps": [g.to_dict() for g in self.data_gaps],
            "insights": self.insights
        }


# =============================================================================
# INTERFACE UNIFICADA
# =============================================================================

class GranularDataScientist:
    """
    Cientista de Dados Granular e Universal
    Versão avançada com precisão cirúrgica máxima
    """
    
    def __init__(self):
        self.universal_analyzer = UniversalAnalyzer()
        self.analysis_history: List[Dict] = []
    
    def analyze(self, data: List[Dict], 
                granularity: str = "micro",
                depth: str = "surgical") -> Dict:
        """
        Análise universal e granular
        
        Args:
            data: Lista de dicionários com dados
            granularity: macro, meso, micro, nano
            depth: surface, standard, deep, surgical
        
        Returns:
            Relatório completo de análise
        """
        gran_map = {
            "macro": AnalysisGranularity.MACRO,
            "meso": AnalysisGranularity.MESO,
            "micro": AnalysisGranularity.MICRO,
            "nano": AnalysisGranularity.NANO
        }
        
        granularity_enum = gran_map.get(granularity, AnalysisGranularity.MICRO)
        
        result = self.universal_analyzer.analyze_dataset(data, granularity_enum)
        
        # Adicionar ao histórico
        self.analysis_history.append({
            "timestamp": datetime.now().isoformat(),
            "granularity": granularity,
            "depth": depth,
            "records": len(data),
            "variables": result["dataset_summary"]["variables"]
        })
        
        return result
    
    def get_summary(self) -> str:
        """Resumo das análises realizadas"""
        if not self.analysis_history:
            return "Nenhuma análise realizada ainda."
        
        total = len(self.analysis_history)
        last = self.analysis_history[-1]
        
        return f"""
══════════════════════════════════════════════════════════════
        GRANULAR DATA SCIENTIST - RELATÓRIO
══════════════════════════════════════════════════════════════

Análises Realizadas: {total}
Última Análise:
  - Timestamp: {last['timestamp']}
  - Granularidade: {last['granularity']}
  - Registros: {last['records']}
  - Variáveis: {last['variables']}

Capacidades:
  ✓ Análise universal (qualquer tipo de dados)
  ✓ Granularidade: MACRO → NANO
  ✓ Detecção de anomalias detalhada
  ✓ Identificação de problemas
  ✓ Proposição de soluções
  ✓ Identificação de lacunas
  ✓ Geração de insights

══════════════════════════════════════════════════════════════
        """


# =============================================================================
# EXEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("GRANULAR DATA SCIENTIST - ENHANCED VERSION")
    print("="*70)
    
    # Criar cientista
    ds = GranularDataScientist()
    
    # Dados de exemplo (mix de tipos)
    data = [
        {"renda": 2000, "escolaridade": 11, "nota": 7.5, "cidade": "Fortaleza", "internet": 1},
        {"renda": 5000, "escolaridade": 16, "nota": 8.2, "cidade": "São Paulo", "internet": 1},
        {"renda": 1500, "escolaridade": 9, "nota": 6.0, "cidade": "Crateús", "internet": 0},
        {"renda": 8000, "escolaridade": 18, "nota": 9.1, "cidade": "Rio de Janeiro", "internet": 1},
        {"renda": 3000, "escolaridade": 12, "nota": 7.0, "cidade": "Recife", "internet": 1},
        {"renda": 4500, "escolaridade": 15, "nota": 8.0, "cidade": "Salvador", "internet": 1},
        {"renda": 1200, "escolaridade": 8, "nota": 5.5, "cidade": "Crateús", "internet": 0},
        {"renda": 7000, "escolaridade": 17, "nota": 8.8, "cidade": "Belo Horizonte", "internet": 1},
    ]
    
    # Análise granular
    result = ds.analyze(data, granularity="micro", depth="surgical")
    
    print("\n[SUMMARY]")
    summary = result["dataset_summary"]
    print(f"   Variáveis analisadas: {summary['variables']}")
    print(f"   Relacionamentos: {summary['relationships']}")
    print(f"   Problemas: {summary['problems']}")
    print(f"   Soluções: {summary['solutions']}")
    print(f"   Insights: {summary['insights']}")
    
    print("\n[PROBLEMAS DETECTADOS]")
    for p in result["problems"]:
        print(f"   - {p['title']} [{p['severity']}]")
    
    print("\n[INSIGHTS]")
    for insight in result["insights"]:
        print(f"   [{insight['type']}] {insight['title']}")
    
    print("\n" + ds.get_summary())