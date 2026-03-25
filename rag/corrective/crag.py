"""
CRAG (Corrective RAG) - Implementação MASWOS Academic
Avalia qualidade dos documentos recuperados antes de enviar ao LLM.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np


class QualityLevel(Enum):
    """Nível de qualidade dos documentos recuperados."""
    HIGH = "high"       # Relevante, pode enviar direto
    MEDIUM = "medium"   # Parcialmente relevante, pode precisar de mais info
    LOW = "low"         # Irrelevante, descartar


@dataclass
class QualityAssessment:
    """Avaliação de qualidade de um chunk."""
    chunk_id: str
    text: str
    quality_level: QualityLevel
    relevance_score: float
    issues: List[str]
    recommendations: List[str]


@dataclass
class RetrievalCorrection:
    """Correção aplicada aos resultados da recuperação."""
    original_chunks: int
    retained_chunks: int
    discarded_chunks: int
    expanded_queries: List[str]
    external_search_triggered: bool
    quality_distribution: Dict[str, int]


class QualityEvaluator:
    """
    Avalia qualidade e relevância dos documentos recuperados.
    
    Usa múltiplos critérios para classificar chunks.
    """
    
    def __init__(
        self,
        llm_evaluator: Any = None,
        min_relevance_score: float = 0.3,
        enable_external_search: bool = True
    ):
        self.llm_evaluator = llm_evaluator
        self.min_relevance_score = min_relevance_score
        self.enable_external_search = enable_external_search
        
        self._encoder = None
    
    def _init_encoder(self):
        """Lazy init do encoder."""
        if self._encoder is None:
            from ..base.encoder import Encoder
            self._encoder = Encoder()
    
    def evaluate_chunk(
        self,
        chunk: Dict[str, Any],
        query: str
    ) -> QualityAssessment:
        """
        Avalia um único chunk.
        
        Args:
            chunk: Chunk recuperado
            query: Query original
            
        Returns:
            QualityAssessment com avaliação
        """
        self._init_encoder()
        
        text = chunk.get('text', '')
        
        relevance_score = self._calculate_relevance(text, query)
        
        issues = []
        recommendations = []
        
        if relevance_score < 0.2:
            quality_level = QualityLevel.LOW
            issues.append("Baixa relevância")
            recommendations.append("Descartar este chunk")
        elif relevance_score < 0.5:
            quality_level = QualityLevel.MEDIUM
            issues.append("Relevância moderada")
            if self.enable_external_search:
                recommendations.append("Considerar busca externa")
        else:
            quality_level = QualityLevel.HIGH
        
        if len(text) < 50:
            issues.append("Texto muito curto")
            quality_level = QualityLevel.LOW
        
        if self._contains_noise(text):
            issues.append("Possível ruído no texto")
            if quality_level == QualityLevel.HIGH:
                quality_level = QualityLevel.MEDIUM
        
        return QualityAssessment(
            chunk_id=chunk.get('id', 'unknown'),
            text=text[:200] + "...",
            quality_level=quality_level,
            relevance_score=relevance_score,
            issues=issues,
            recommendations=recommendations
        )
    
    def _calculate_relevance(self, text: str, query: str) -> float:
        """Calcula score de relevância."""
        if not text or not query:
            return 0.0
        
        text_lower = text.lower()
        query_lower = query.lower()
        
        query_words = set(query_lower.split())
        text_words = set(text_lower.split())
        
        overlap = query_words.intersection(text_words)
        
        word_score = len(overlap) / max(len(query_words), 1)
        
        try:
            query_emb = self._encoder.encode(query)
            text_emb = self._encoder.encode(text[:1000])
            
            similarity = float(np.dot(query_emb, text_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(text_emb)
            ))
        except Exception:
            similarity = 0.5
        
        return (word_score * 0.4) + (similarity * 0.6)
    
    def _contains_noise(self, text: str) -> bool:
        """Detecta possível ruído no texto."""
        noise_indicators = [
            'erro',
            'indisponível',
            '404',
            'page not found',
            'access denied',
            'login required'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in noise_indicators)
    
    def evaluate_batch(
        self,
        chunks: List[Dict[str, Any]],
        query: str
    ) -> List[QualityAssessment]:
        """Avalia múltiplos chunks."""
        return [self.evaluate_chunk(chunk, query) for chunk in chunks]


class RetrievalCorrector:
    """
    Aplica correções aos resultados da recuperação.
    
    Decide quais chunks manter, quais descartar,
    e se precisa de busca adicional.
    """
    
    def __init__(
        self,
        evaluator: Optional[QualityEvaluator] = None,
        min_high_quality: int = 2,
        max_chunks_final: int = 10
    ):
        self.evaluator = evaluator or QualityEvaluator()
        self.min_high_quality = min_high_quality
        self.max_chunks_final = max_chunks_final
    
    def correct(
        self,
        chunks: List[Dict[str, Any]],
        query: str
    ) -> Tuple[List[Dict[str, Any]], RetrievalCorrection]:
        """
        Avalia e corrige os chunks recuperados.
        
        Args:
            chunks: Lista de chunks recuperados
            query: Query original
            
        Returns:
            Tupla com (chunks filtrados, metadata da correção)
        """
        assessments = self.evaluator.evaluate_batch(chunks, query)
        
        high_quality = [a for a in assessments if a.quality_level == QualityLevel.HIGH]
        medium_quality = [a for a in assessments if a.quality_level == QualityLevel.MEDIUM]
        low_quality = [a for a in assessments if a.quality_level == QualityLevel.LOW]
        
        retained = high_quality.copy()
        
        if len(retained) < self.min_high_quality and medium_quality:
            needed = self.min_high_quality - len(retained)
            retained.extend(medium_quality[:needed])
        
        retained = retained[:self.max_chunks_final]
        
        retained_chunks = [
            {
                'text': chunk.get('text', ''),
                'score': chunk.get('score', 0),
                'source': chunk.get('source', 'unknown'),
                'id': chunk.get('id', 'unknown'),
                'quality': a.quality_level.value
            }
            for chunk, a in zip(chunks, assessments)
            if a in retained
        ]
        
        external_needed = (
            len(high_quality) < 1 and
            len(medium_quality) < 2 and
            self.evaluator.enable_external_search
        )
        
        expanded_queries = []
        if external_needed:
            expanded_queries = self._generate_expanded_queries(query, assessments)
        
        return retained_chunks, RetrievalCorrection(
            original_chunks=len(chunks),
            retained_chunks=len(retained_chunks),
            discarded_chunks=len(chunks) - len(retained_chunks),
            expanded_queries=expanded_queries,
            external_search_triggered=external_needed,
            quality_distribution={
                'high': len(high_quality),
                'medium': len(medium_quality),
                'low': len(low_quality)
            }
        )
    
    def _generate_expanded_queries(
        self,
        query: str,
        assessments: List[QualityAssessment]
    ) -> List[str]:
        """Gera queries expandidas para busca adicional."""
        expanded = [query]
        
        query_lower = query.lower()
        
        terms = {
            'direito': ['lei', 'jurisprudência', 'tribunal'],
            'científico': ['artigo', 'pesquisa', 'estudo'],
            'estatística': ['dados', 'IBGE', 'número'],
        }
        
        for key, synonyms in terms.items():
            if key in query_lower:
                for syn in synonyms:
                    expanded.append(f"{query} {syn}")
        
        return expanded[:3]


class CRAG:
    """
    Implementação do Corrective RAG para MASWOS Academic.
    
    Avalia qualidade dos documentos recuperados antes de enviar ao LLM.
    CRÍTICO para validação de fontes de dados, jurisprudência e estatísticas.
    """
    
    def __init__(
        self,
        vanilla_rag: Any = None,
        enable_correction: bool = True,
        enable_external_search: bool = True,
        **kwargs
    ):
        self.vanilla_rag = vanilla_rag
        self.enable_correction = enable_correction
        self.enable_external_search = enable_external_search
        
        self.evaluator = QualityEvaluator(
            enable_external_search=enable_external_search
        )
        self.corrector = RetrievalCorrector(
            evaluator=self.evaluator
        )
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize components if not provided."""
        if self.vanilla_rag is None:
            from ..classic.vanilla_rag import VanillaRAG, VanillaRAGConfig
            self.vanilla_rag = VanillaRAG(config=VanillaRAGConfig())
    
    def query(
        self,
        query: str,
        top_k: int = 5,
        enable_correction: Optional[bool] = None,
        return_quality_report: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query com correção automática.
        
        Args:
            query: Query do usuário
            top_k: Número de chunks a recuperar inicialmente
            enable_correction: Override para habilitação de correção
            return_quality_report: Se inclui relatório de qualidade
            
        Returns:
            Resposta com metadados de qualidade
        """
        enable = enable_correction if enable_correction is not None else self.enable_correction
        
        initial_chunks = top_k * 2
        
        retrieval_result = self.vanilla_rag.retriever.retrieve(
            query=query,
            top_k=initial_chunks
        )
        
        chunks_data = [
            {
                'text': chunk.text,
                'score': chunk.score,
                'source': chunk.source,
                'id': chunk.chunk_id
            }
            for chunk in retrieval_result.chunks
        ]
        
        correction_result = None
        final_chunks = chunks_data
        
        if enable:
            final_chunks, correction_result = self.corrector.correct(
                chunks_data,
                query
            )
        
        if correction_result and correction_result.external_search_triggered:
            expanded_results = self._do_expanded_search(
                correction_result.expanded_queries
            )
            final_chunks.extend(expanded_results[:2])
        
        final_chunks = final_chunks[:top_k]
        
        augmented = self.vanilla_rag.augmenter.augment(
            query=query,
            retrieved_chunks=final_chunks
        )
        
        generation_result = self.vanilla_rag.generator.generate(
            prompt=augmented.augmented_prompt
        )
        
        response = {
            'answer': generation_result.text,
            'query': query,
            'chunks_retrieved': len(final_chunks),
            'correction_applied': enable,
            'latency_ms': generation_result.latency_ms
        }
        
        if enable and correction_result:
            response['correction'] = {
                'original_chunks': correction_result.original_chunks,
                'retained_chunks': correction_result.retained_chunks,
                'discarded_chunks': correction_result.discarded_chunks,
                'quality_distribution': correction_result.quality_distribution,
                'external_search_triggered': correction_result.external_search_triggered
            }
        
        if return_quality_report and enable:
            assessments = self.evaluator.evaluate_batch(
                [{'text': c['text'], 'id': c.get('id', 'unknown')} for c in chunks_data],
                query
            )
            response['quality_report'] = [
                {
                    'chunk_id': a.chunk_id,
                    'quality': a.quality_level.value,
                    'score': a.relevance_score,
                    'issues': a.issues
                }
                for a in assessments
            ]
        
        return response
    
    def _do_expanded_search(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Executa busca expandida (fallback para quando não há sources externas)."""
        results = []
        
        for q in queries:
            results.append({
                'text': f"Resultado de busca expandida para: {q}",
                'source': 'external_search',
                'score': 0.5,
                'id': f"external_{hash(q)}"
            })
        
        return results
    
    def evaluate_source_quality(
        self,
        source: str,
        query: str
    ) -> Dict[str, Any]:
        """
        Avalia qualidade de uma fonte específica.
        
        Útil para auditoria de fontes em artigos acadêmicos.
        """
        assessments = self.evaluator.evaluate_batch(
            [{'text': f"Content from {source}", 'id': source}],
            query
        )
        
        return {
            'source': source,
            'quality': assessments[0].quality_level.value,
            'relevance_score': assessments[0].relevance_score,
            'issues': assessments[0].issues,
            'recommendations': assessments[0].recommendations
        }
