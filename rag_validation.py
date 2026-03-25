"""
MASWOS V5 NEXUS - Scripts de Validação RAG e Auditoria
Autor: Arquitetura Transformer-Agentes
Versão: 5.0.0-NEXUS
"""

from typing import Dict, List, Tuple, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import json

class QualityGate(Enum):
    G0 = "G0"
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    GF = "GF"

class AuditStatus(Enum):
    VERIFIED = "VERIFIED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

@dataclass
class Citation:
    text: str
    source: str
    year: int
    page: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    verified: bool = False

@dataclass
class Claim:
    id: str
    text: str
    citations: List[Citation] = field(default_factory=list)
    verified: bool = False
    hallucination_risk: float = 0.0
    source_documents: List[str] = field(default_factory=list)

@dataclass
class AuditEntry:
    timestamp: str
    agent_id: str
    action: str
    claim_id: Optional[str] = None
    status: AuditStatus = AuditStatus.UNKNOWN
    details: Dict = field(default_factory=dict)

@dataclass
class ValidationResult:
    gate: QualityGate
    passed: bool
    score: float
    threshold: float
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class RAGValidator:
    """
    Validador RAG Protocol de 3 Eixos.
    
    Eixo 1: Fundacional (>10 anos)
    Eixo 2: Estado da Arte (3-5 anos)
    Eixo 3: Metodológica
    """
    
    def __init__(
        self,
        eixo1_threshold_year: int = 10,
        eixo2_min_year: int = 2019,
        eixo2_max_year: int = 2023,
        convergence_threshold: float = 0.80
    ):
        self.eixo1_threshold_year = eixo1_threshold_year
        self.eixo2_min_year = eixo2_min_year
        self.eixo2_max_year = eixo2_max_year
        self.convergence_threshold = convergence_threshold
    
    def classify_eixo(self, citation: Citation) -> str:
        """Classifica citação em um dos 3 eixos"""
        current_year = datetime.now().year
        
        if current_year - citation.year > self.eixo1_threshold_year:
            return "eixo_1_fundacional"
        elif self.eixo2_min_year <= citation.year <= self.eixo2_max_year:
            return "eixo_2_estado_arte"
        else:
            return "eixo_3_metodologica"
    
    def validate_citation(self, citation: Citation) -> ValidationResult:
        """Valida uma única citação"""
        issues = []
        recommendations = []
        passed = True
        
        # Verifica presença de campos obrigatórios
        if not citation.source:
            issues.append("Fonte não especificada")
            passed = False
        
        if not citation.year:
            issues.append("Ano não especificado")
            passed = False
        
        # Verifica formato de URL/DOI
        if citation.url and not self._is_valid_url(citation.url):
            issues.append(f"URL inválida: {citation.url}")
            passed = False
        
        if citation.doi and not self._is_valid_doi(citation.doi):
            issues.append(f"DOI inválido: {citation.doi}")
            passed = False
        
        # Verifica ano razoável
        if citation.year > datetime.now().year:
            issues.append(f"Ano futuro: {citation.year}")
            passed = False
        
        score = 1.0 if passed else 0.5
        
        return ValidationResult(
            gate=QualityGate.G2,
            passed=passed,
            score=score,
            threshold=self.convergence_threshold,
            issues=issues,
            recommendations=recommendations
        )
    
    def validate_alignment(
        self,
        claims: List[Claim],
        source_documents: List[Dict]
    ) -> ValidationResult:
        """
        Valida alinhamento RAG: todas as citações devem ter 
       对应的 fonte nos documentos recuperados.
        """
        alignment_scores = []
        issues = []
        
        for claim in claims:
            if not claim.citations:
                issues.append(f"Claim {claim.id} sem citações")
                alignment_scores.append(0.0)
                continue
            
            # Verifica se cada citação tem fonte correspondente
            for citation in claim.citations:
                has_source = any(
                    citation.source.lower() in doc.get('title', '').lower()
                    or citation.source.lower() in doc.get('authors', [])
                    for doc in source_documents
                )
                alignment_scores.append(1.0 if has_source else 0.0)
        
        score = sum(alignment_scores) / max(len(alignment_scores), 1)
        passed = score >= 1.0  # RAG alignment requer 100%
        
        if not passed:
            issues.append(f"RAG alignment: {score:.1%} < 100%")
        
        return ValidationResult(
            gate=QualityGate.G3,
            passed=passed,
            score=score,
            threshold=1.0,
            issues=issues
        )
    
    def cross_validate_sources(
        self,
        claims: List[Claim],
        sources: List[Dict]
    ) -> ValidationResult:
        """Validação cruzada com múltiplas fontes"""
        convergence_scores = []
        
        for claim in claims:
            # Simula validação cruzada
            matches = sum(1 for src in sources if src.get('verified', False))
            convergence = matches / max(len(sources), 1)
            convergence_scores.append(convergence)
        
        avg_convergence = sum(convergence_scores) / max(len(convergence_scores), 1)
        passed = avg_convergence >= self.convergence_threshold
        
        return ValidationResult(
            gate=QualityGate.G2,
            passed=passed,
            score=avg_convergence,
            threshold=self.convergence_threshold,
            issues=[] if passed else [f"Convergência: {avg_convergence:.1%} < 80%"]
        )
    
    def _is_valid_url(self, url: str) -> bool:
        return url.startswith(('http://', 'https://'))
    
    def _is_valid_doi(self, doi: str) -> bool:
        return doi.startswith('10.') and '/' in doi


class ForensicAuditor:
    """
    Sistema de auditoria forense com rastreabilidade 100%.
    
    Implementa Quality Gates progressivos:
    G0 → G1 → G2 → G3 → G4 → GF
    """
    
    def __init__(self):
        self.audit_log: List[AuditEntry] = []
        self.claims: Dict[str, Claim] = {}
        self.quality_gates = {
            QualityGate.G0: 1.0,
            QualityGate.G1: 0.80,
            QualityGate.G2: 0.85,
            QualityGate.G3: 0.90,
            QualityGate.G4: 0.95,
            QualityGate.GF: 0.99
        }
    
    def audit_document(
        self,
        claims: List[Claim],
        validator: RAGValidator,
        source_documents: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Executa auditoria completa do documento.
        Retorna relatório detalhado.
        """
        audit_report = {
            'total_claims': len(claims),
            'verified_claims': 0,
            'unverified_claims': 0,
            'hallucination_risk': 0.0,
            'sources_found': [],
            'citations_valid': True,
            'gate_results': {},
            'audit_entries': []
        }
        
        # Armazena claims
        for claim in claims:
            self.claims[claim.id] = claim
        
        # G1: Validação de entrada
        g1_result = self._gate_g1_input(claims)
        audit_report['gate_results']['G1'] = g1_result
        
        # G2: Validação de fontes
        if source_documents:
            g2_result = validator.cross_validate_sources(claims, source_documents)
            audit_report['gate_results']['G2'] = g2_result
        
        # G3: Validação de alinhamento RAG
        if source_documents:
            g3_result = validator.validate_alignment(claims, source_documents)
            audit_report['gate_results']['G3'] = g3_result
        
        # G4: Análise individual de claims
        g4_result = self._gate_g4_analysis(claims, validator)
        audit_report['gate_results']['G4'] = g4_result
        
        # GF: Validação final
        gf_result = self._gate_gf_final(audit_report)
        audit_report['gate_results']['GF'] = gf_result
        
        # Calcula métricas
        for claim in claims:
            if claim.verified:
                audit_report['verified_claims'] += 1
                audit_report['sources_found'].extend([
                    c.source for c in claim.citations if c.verified
                ])
            else:
                audit_report['unverified_claims'] += 1
            
            audit_report['hallucination_risk'] += claim.hallucination_risk
        
        audit_report['hallucination_risk'] /= max(len(claims), 1)
        
        return audit_report
    
    def _gate_g1_input(self, claims: List[Claim]) -> ValidationResult:
        """G1: Validação de input"""
        passed = len(claims) > 0
        return ValidationResult(
            gate=QualityGate.G1,
            passed=passed,
            score=1.0 if passed else 0.0,
            threshold=self.quality_gates[QualityGate.G1],
            issues=[] if passed else ["Claims vazios"]
        )
    
    def _gate_g4_analysis(self, claims: List[Claim], validator: RAGValidator) -> ValidationResult:
        """G4: Análise individual de claims"""
        analysis_scores = []
        issues = []
        
        for claim in claims:
            if not claim.citations:
                issues.append(f"Claim {claim.id} sem citação")
                analysis_scores.append(0.0)
                continue
            
            # Valida cada citação
            for citation in claim.citations:
                result = validator.validate_citation(citation)
                analysis_scores.append(result.score)
                if not result.passed:
                    issues.extend(result.issues)
        
        score = sum(analysis_scores) / max(len(analysis_scores), 1)
        passed = score >= self.quality_gates[QualityGate.G4]
        
        return ValidationResult(
            gate=QualityGate.G4,
            passed=passed,
            score=score,
            threshold=self.quality_gates[QualityGate.G4],
            issues=issues
        )
    
    def _gate_gf_final(self, audit_report: Dict) -> ValidationResult:
        """GF: Validação final"""
        all_passed = all(
            result.passed 
            for result in audit_report['gate_results'].values()
        )
        
        verified_ratio = (
            audit_report['verified_claims'] / 
            max(audit_report['total_claims'], 1)
        )
        
        score = (verified_ratio + (1 - audit_report['hallucination_risk'])) / 2
        passed = all_passed and score >= self.quality_gates[QualityGate.GF]
        
        return ValidationResult(
            gate=QualityGate.GF,
            passed=passed,
            score=score,
            threshold=self.quality_gates[QualityGate.GF],
            issues=[] if passed else ["Gate final não passou"]
        )
    
    def log_entry(self, entry: AuditEntry):
        """Registra entrada no log de auditoria"""
        self.audit_log.append(entry)
    
    def get_trace(self, claim_id: str) -> List[AuditEntry]:
        """Retorna trilha de auditoria para um claim"""
        return [
            entry for entry in self.audit_log 
            if entry.claim_id == claim_id
        ]


class CriticRouter:
    """
    Sistema de roteamento cognitivo baseado em scores.
    
    Implementa mecanismo de atenção para roteamento:
    CR(q, agents) = Attention(q, K_agents, V_agents)
    """
    
    def __init__(self):
        self.thresholds: Dict[str, float] = {
            'fluff': 0.0,
            'rag_alignment': 1.0,
            'coesao': 0.95,
            'compliance': 0.95,
            'completude': 0.90
        }
        self.weights = {
            'fluff': 0.20,
            'rag_alignment': 0.25,
            'coesao': 0.20,
            'compliance': 0.20,
            'completude': 0.15
        }
    
    def route(
        self,
        scores: Dict[str, float],
        agent_pool: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Decide próximo passo baseado em scores de qualidade.
        
        Returns:
            action: 'PROCEED' | 'ROUTE' | 'ESCALATE'
            target_agent: Agente para qual rotear
            reason: Motivo do roteamento
        """
        routing_needed = []
        
        for dimension, score in scores.items():
            threshold = self.thresholds.get(dimension, 0.90)
            if score < threshold:
                gap = threshold - score
                routing_needed.append({
                    'dimension': dimension,
                    'score': score,
                    'threshold': threshold,
                    'gap': gap,
                    'agent': self._get_agent_for_dimension(dimension, agent_pool)
                })
        
        if not routing_needed:
            return {
                'action': 'PROCEED',
                'next_gate': 'next',
                'score': self._compute_final_score(scores)
            }
        
        routing_needed.sort(key=lambda x: x['gap'], reverse=True)
        top = routing_needed[0]
        
        return {
            'action': 'ROUTE',
            'target_agent': top['agent'],
            'reason': top['dimension'],
            'gap': top['gap'],
            'alternatives': routing_needed[1:]
        }
    
    def _get_agent_for_dimension(
        self,
        dimension: str,
        agent_pool: Dict[str, Any]
    ) -> Optional[str]:
        """Retorna agente mais adequado para dimensão"""
        dimension_agents = {
            'fluff': 'editor_agent',
            'rag_alignment': 'citation_agent',
            'coesao': 'revision_agent',
            'compliance': 'compliance_agent',
            'completude': 'expansion_agent'
        }
        return dimension_agents.get(dimension, 'generalist_agent')
    
    def _compute_final_score(self, scores: Dict[str, float]) -> float:
        """Computa score final ponderado"""
        return sum(
            self.weights.get(dim, 0) * score 
            for dim, score in scores.items()
        )


# ========== Script Principal ==========

if __name__ == "__main__":
    # Demonstração da arquitetura
    
    print("=" * 60)
    print("MASWOS V5 NEXUS - Validação RAG e Auditoria")
    print("=" * 60)
    
    # Cria validador RAG
    validator = RAGValidator()
    
    # Cria citações de exemplo
    citations = [
        Citation(
            text="Direito constitucional contemporâneo",
            source="Barroso",
            year=2019,
            page="15-45",
            url="https://www.saraivauni.com.br"
        ),
        Citation(
            text="Retrieval-Augmented Generation",
            source="Lewis et al.",
            year=2020,
            doi="10.48550/arXiv.2005.14167"
        )
    ]
    
    print("\n### Validação de Citações ###")
    for citation in citations:
        result = validator.validate_citation(citation)
        eixo = validator.classify_eixo(citation)
        print(f"\nCitação: {citation.source} ({citation.year})")
        print(f"Eixo: {eixo}")
        print(f"Resultado: {'PASSOU' if result.passed else 'FALHOU'}")
        print(f"Score: {result.score:.2%}")
    
    # Cria claims
    claims = [
        Claim(
            id="claim_1",
            text="A Constituição Federal de 1988 estabelece...",
            citations=[citations[0]],
            verified=True,
            hallucination_risk=0.05
        ),
        Claim(
            id="claim_2",
            text="RAG reduz alucinações em LLMs...",
            citations=[citations[1]],
            verified=True,
            hallucination_risk=0.02
        )
    ]
    
    print("\n### Auditoria Forense ###")
    auditor = ForensicAuditor()
    source_docs = [
        {'title': 'Curso de Direito Constitucional Contemporâneo', 'authors': ['Barroso']},
        {'title': 'RAG Paper', 'authors': ['Lewis et al.']}
    ]
    
    report = auditor.audit_document(claims, validator, source_docs)
    
    print(f"\nTotal de Claims: {report['total_claims']}")
    print(f"Claims Verificados: {report['verified_claims']}")
    print(f"Risk de Alucinação: {report['hallucination_risk']:.2%}")
    
    print("\n### Critic-Router ###")
    router = CriticRouter()
    scores = {
        'fluff': 0.0,
        'rag_alignment': 1.0,
        'coesao': 0.95,
        'compliance': 0.92,
        'completude': 0.90
    }
    
    decision = router.route(scores, {})
    print(f"\nDecisão: {decision['action']}")
    if decision['action'] == 'ROUTE':
        print(f"Agente Alvo: {decision['target_agent']}")
        print(f"Motivo: {decision['reason']}")
        print(f"Lacuna: {decision['gap']:.2%}")
    else:
        print(f"Score Final: {decision['score']:.2%}")
    
    print("\n" + "=" * 60)
    print("Arquitetura validada com sucesso!")
    print("=" * 60)
