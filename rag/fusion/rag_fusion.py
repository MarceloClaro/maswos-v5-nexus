"""
RAG-Fusion (Reciprocal Rank Fusion) - Implementação MASWOS Academic
Combina resultados de múltiplos métodos de busca usando RRF.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from collections import defaultdict


class RRFScorer:
    """
    Implementa Reciprocal Rank Fusion para combinação de resultados.
    
    O RRF combina rankings de múltiplos métodos de busca
    para produzir um ranking unificado.
    """
    
    def __init__(self, k: int = 60):
        """
        Args:
            k: Parâmetro de damping (típico: 60)
        """
        self.k = k
    
    def fuse(
        self,
        rankings: List[List[Tuple[str, float]]],
        weights: Optional[List[float]] = None
    ) -> List[Tuple[str, float]]:
        """
        Combina múltiplos rankings usando RRF.
        
        Args:
            rankings: Lista de rankings, cada um é lista de (doc_id, score)
            weights: Pesos opcionais para cada ranking
            
        Returns:
            Lista fundida de (doc_id, fused_score)
        """
        if not rankings:
            return []
        
        if weights is None:
            weights = [1.0] * len(rankings)
        
        weights = self._normalize_weights(weights)
        
        doc_scores = defaultdict(float)
        
        for rank_idx, ranking in enumerate(rankings):
            weight = weights[rank_idx]
            
            for position, (doc_id, original_score) in enumerate(ranking):
                rrf_score = 1.0 / (self.k + position + 1)
                doc_scores[doc_id] += weight * rrf_score
        
        sorted_docs = sorted(
            doc_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_docs
    
    def _normalize_weights(self, weights: List[float]) -> List[float]:
        """Normaliza pesos para somar 1."""
        total = sum(weights)
        if total == 0:
            return [1.0 / len(weights)] * len(weights)
        return [w / total for w in weights]


class MultiSourceRetriever:
    """
    Recuperador que consulta múltiplas fontes.
    """
    
    def __init__(
        self,
        sources: Dict[str, Any],
        default_top_k: int = 10
    ):
        self.sources = sources
        self.default_top_k = default_top_k
    
    def retrieve_from_source(
        self,
        source_name: str,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Tuple[str, float]]:
        """Recupera de uma fonte específica."""
        top_k = top_k or self.default_top_k
        
        if source_name not in self.sources:
            return []
        
        source = self.sources[source_name]
        
        if hasattr(source, 'similarity_search'):
            results = source.similarity_search(
                query=query,
                k=top_k
            )
            return [(r.get('id', f"{source_name}_{i}"), r.get('score', 0))
                    for i, r in enumerate(results)]
        
        return []
    
    def retrieve_all(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> Dict[str, List[Tuple[str, float]]]:
        """Recupera de todas as fontes."""
        top_k = top_k or self.default_top_k
        
        all_results = {}
        
        for source_name in self.sources.keys():
            results = self.retrieve_from_source(
                source_name,
                query,
                top_k
            )
            all_results[source_name] = results
        
        return all_results


class RAGFusion:
    """
    Implementação do RAG-Fusion para MASWOS Academic.
    
    Combina múltiplos métodos de busca para resultados mais robustos.
    Útil para fundir resultados de CAPES, SciELO, tribunais, IBGE, etc.
    """
    
    def __init__(
        self,
        vanilla_rag: Any = None,
        sources: Optional[Dict[str, Any]] = None,
        fusion_method: str = "rrf",
        k_value: int = 60,
        **kwargs
    ):
        self.vanilla_rag = vanilla_rag
        self.fusion_method = fusion_method
        self.k_value = k_value
        
        self.rrf_scorer = RRFScorer(k=k_value)
        self.retriever = MultiSourceRetriever(
            sources=sources or {},
            default_top_k=10
        )
        
        self._encoder = None
        self._augmenter = None
        self._generator = None
    
    def _init_components(self):
        """Initialize components."""
        if self._encoder is None:
            from ..base.encoder import Encoder
            self._encoder = Encoder()
        
        if self._augmenter is None:
            from ..base.augmenter import Augmenter
            self._augmenter = Augmenter()
        
        if self._generator is None:
            from ..base.generator import Generator, AcademicGenerator
            self._generator = AcademicGenerator()
    
    def query(
        self,
        query: str,
        source_names: Optional[List[str]] = None,
        top_k: int = 5,
        weights: Optional[Dict[str, float]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query com fusão de múltiplas fontes.
        
        Args:
            query: Query do usuário
            source_names: Fontes a consultar (None = todas)
            top_k: Número de resultados finais
            weights: Pesos para cada fonte
            
        Returns:
            Resposta com resultados fundidos
        """
        self._init_components()
        
        if source_names is None:
            source_names = list(self.retriever.sources.keys())
        
        if weights is None:
            weights = {s: 1.0 for s in source_names}
        
        rankings = []
        for source_name in source_names:
            source_results = self.retriever.retrieve_from_source(
                source_name,
                query,
                top_k=top_k * 2
            )
            if source_results:
                rankings.append(source_results)
        
        if not rankings:
            return {
                'answer': 'Nenhuma fonte disponível para consulta.',
                'query': query,
                'error': 'No sources configured'
            }
        
        weight_list = [weights.get(source_names[i], 1.0) for i in range(len(rankings))]
        
        fused_results = self.rrf_scorer.fuse(rankings, weight_list)
        
        final_results = []
        for doc_id, score in fused_results[:top_k]:
            final_results.append({
                'id': doc_id,
                'fused_score': score,
                'source': self._extract_source(doc_id)
            })
        
        augmented = self._augmenter.augment(
            query=query,
            retrieved_chunks=final_results
        )
        
        result = self._generator.generate(augmented.augmented_prompt)
        
        return {
            'answer': result.text,
            'query': query,
            'sources_consulted': source_names,
            'fused_results': final_results,
            'total_sources': len(rankings)
        }
    
    def _extract_source(self, doc_id: str) -> str:
        """Extrai nome da fonte do ID do documento."""
        if '_' in doc_id:
            return doc_id.split('_')[0]
        return 'unknown'
    
    def add_source(self, name: str, source: Any):
        """Adiciona nova fonte ao sistema."""
        self.retriever.sources[name] = source
    
    def set_weights(self, weights: Dict[str, float]):
        """Define pesos para as fontes."""
        self.source_weights = weights
