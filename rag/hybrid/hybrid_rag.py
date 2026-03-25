"""
Hybrid RAG - Implementação MASWOS Academic
Combina busca vetorial com busca em grafos.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np


class HybridRAG:
    """
    Implementação do Hybrid RAG para MASWOS Academic.
    
    Combina busca vetorial com busca em grafos para resultados
    mais completos e estruturalmente conectados.
    """
    
    def __init__(
        self,
        vector_store: Any = None,
        graph_rag: Any = None,
        vanilla_rag: Any = None,
        alpha: float = 0.5,
        **kwargs
    ):
        self.vector_store = vector_store
        self.graph_rag = graph_rag
        self.vanilla_rag = vanilla_rag
        self.alpha = alpha  # Balance: 0 = vector, 1 = graph
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize components."""
        if self.vanilla_rag is None:
            from ..classic.vanilla_rag import VanillaRAG, VanillaRAGConfig
            self.vanilla_rag = VanillaRAG(
                vector_store=self.vector_store,
                config=VanillaRAGConfig()
            )
        
        if self.graph_rag is None:
            from ..graph.graph_rag import GraphRAG
            self.graph_rag = GraphRAG(
                vector_store=self.vector_store
            )
    
    def query(
        self,
        query: str,
        top_k: int = 5,
        alpha: Optional[float] = None,
        include_graph_context: bool = True,
        return_separate_results: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query híbrida vetorial + grafo.
        
        Args:
            query: Query do usuário
            top_k: Número de resultados
            alpha: Override para peso de equilíbrio
            include_graph_context: Se inclui contexto do grafo
            return_separate_results: Se retorna resultados separadamente
            
        Returns:
            Resposta com contexto híbrido
        """
        alpha = alpha or self.alpha
        
        vector_results = self._get_vector_results(query, top_k)
        
        graph_context = []
        if include_graph_context:
            graph_context = self._get_graph_context(query, top_k)
        
        combined_context = self._combine_contexts(
            vector_results,
            graph_context,
            alpha
        )
        
        augmented = self.vanilla_rag.augmenter.augment(
            query=query,
            retrieved_chunks=combined_context[:top_k]
        )
        
        generation_result = self.vanilla_rag.generator.generate(
            prompt=augmented.augmented_prompt
        )
        
        response = {
            'answer': generation_result.text,
            'query': query,
            'method': 'hybrid',
            'alpha': alpha,
            'vector_results_count': len(vector_results),
            'graph_context_count': len(graph_context),
            'latency_ms': generation_result.latency_ms
        }
        
        if return_separate_results:
            response['separate_results'] = {
                'vector': vector_results,
                'graph': graph_context
            }
        
        return response
    
    def _get_vector_results(
        self,
        query: str,
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Executa busca vetorial."""
        if not self.vector_store:
            return []
        
        try:
            from ..base.encoder import Encoder
            encoder = Encoder()
            query_emb = encoder.encode(query)
            
            results = self.vector_store.similarity_search(
                query_embedding=query_emb,
                k=top_k
            )
            
            return [
                {
                    'text': r.get('text', ''),
                    'score': r.get('score', 0),
                    'source': r.get('source', 'unknown'),
                    'type': 'vector'
                }
                for r in results
            ]
        except Exception as e:
            print(f"Vector search error: {e}")
            return []
    
    def _get_graph_context(
        self,
        query: str,
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Executa busca em grafo."""
        try:
            graph_stats = self.graph_rag.get_graph_statistics()
            
            if graph_stats['total_entities'] == 0:
                return []
            
            entities = []
            if hasattr(self.graph_rag, 'neo4j') and self.graph_rag.neo4j:
                entities = self.graph_rag.neo4j.find_entities(query, limit=top_k)
            
            context = []
            for ent_record in entities[:top_k]:
                entity = ent_record.get('e', {})
                context.append({
                    'text': f"{entity.get('name')}: {entity.get('description', '')}",
                    'type': 'entity',
                    'entity_type': entity.get('type'),
                    'source': 'knowledge_graph'
                })
            
            return context
            
        except Exception as e:
            print(f"Graph search error: {e}")
            return []
    
    def _combine_contexts(
        self,
        vector_results: List[Dict],
        graph_context: List[Dict],
        alpha: float
    ) -> List[Dict]:
        """Combina resultados vetoriais com contexto de grafo."""
        combined = []
        
        vec_weight = 1 - alpha
        graph_weight = alpha
        
        for i, r in enumerate(vector_results):
            adjusted_score = r.get('score', 0) * vec_weight
            combined.append({
                **r,
                'adjusted_score': adjusted_score,
                'weight': vec_weight
            })
        
        for r in graph_context:
            combined.append({
                **r,
                'score': 0.5 * graph_weight,
                'adjusted_score': 0.5 * graph_weight,
                'weight': graph_weight
            })
        
        combined.sort(key=lambda x: x.get('adjusted_score', 0), reverse=True)
        
        return combined
    
    def query_with_communities(
        self,
        query: str,
        top_k: int = 5,
        include_community_summaries: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Query que inclui resumos de comunidades do grafo."""
        vector_results = self._get_vector_results(query, top_k)
        
        community_context = []
        
        if include_community_summaries and hasattr(self.graph_rag, 'neo4j') and self.graph_rag.neo4j:
            try:
                communities = self.graph_rag.neo4j.get_communities()
                
                for comm in communities[:3]:
                    summary = self.graph_rag.neo4j.get_community_summary(
                        comm.get('community')
                    )
                    if summary:
                        community_context.append({
                            'text': summary,
                            'type': 'community_summary',
                            'community_id': comm.get('community'),
                            'source': 'knowledge_graph'
                        })
            except Exception as e:
                print(f"Community summary error: {e}")
        
        all_context = vector_results + community_context
        
        augmented = self.vanilla_rag.augmenter.augment(
            query=query,
            retrieved_chunks=all_context[:top_k]
        )
        
        generation_result = self.vanilla_rag.generator.generate(
            prompt=augmented.augmented_prompt
        )
        
        return {
            'answer': generation_result.text,
            'query': query,
            'method': 'hybrid_with_communities',
            'community_summaries_used': len(community_context),
            'vector_results': len(vector_results)
        }
    
    def set_alpha(self, alpha: float):
        """Ajusta equilíbrio entre busca vetorial e grafo."""
        if 0 <= alpha <= 1:
            self.alpha = alpha
    
    def get_hybrid_info(self) -> Dict[str, Any]:
        """Retorna informações da configuração híbrida."""
        return {
            'alpha': self.alpha,
            'vector_weight': 1 - self.alpha,
            'graph_weight': self.alpha,
            'vector_store_configured': self.vector_store is not None,
            'graph_rag_configured': self.graph_rag is not None,
            'vanilla_rag_configured': self.vanilla_rag is not None
        }
