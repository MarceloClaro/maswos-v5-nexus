"""
RAG Orchestrator - Master Controller para MASWOS Academic
Integra todos os tipos de RAG em uma única interface unificada.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import json


class RAGType(Enum):
    """Tipos de RAG disponíveis."""
    VANILLA = "vanilla"
    MEMORY = "memory"
    AGENTIC = "agentic"
    GRAPH = "graph"
    HYBRID = "hybrid"
    CRAG = "crag"
    ADAPTIVE = "adaptive"
    FUSION = "fusion"
    HYDE = "hyde"


@dataclass
class RAGConfig:
    """Configuração global do RAG."""
    default_rag_type: RAGType = RAGType.ADAPTIVE
    top_k: int = 5
    chunk_size: int = 2000
    overlap: int = 500
    llm_model: str = "gpt-4"
    temperature: float = 0.7
    enable_correction: bool = True
    enable_memory: bool = True
    memory_expiration_hours: int = 24


@dataclass
class RAGStats:
    """Estatísticas do sistema RAG."""
    total_queries: int = 0
    queries_by_type: Dict[str, int] = field(default_factory=dict)
    avg_latency_ms: float = 0.0
    sources_used: List[str] = field(default_factory=list)


class RAGOrchestrator:
    """
    Orchestrator master que integra todos os tipos de RAG.
    
    Fornece interface unificada para:
    - Vanilla RAG (busca básica)
    - RAG com Memória (contexto de sessão)
    - Agentic RAG (roteamento dinâmico)
    - GraphRAG (conhecimento estrutural)
    - Hybrid RAG (vetorial + grafo)
    - CRAG (validação de qualidade)
    - Adaptive RAG (estratégia adaptativa)
    - RAG-Fusion (múltiplas fontes)
    - HyDE (documentos hipotéticos)
    """
    
    def __init__(
        self,
        config: Optional[RAGConfig] = None,
        vector_store: Any = None,
        neo4j_connector: Any = None,
        **kwargs
    ):
        self.config = config or RAGConfig()
        self.vector_store = vector_store
        self.neo4j_connector = neo4j_connector
        
        self._rag_instances: Dict[RAGType, Any] = {}
        self._stats = RAGStats()
        
        self._initialize_all_rags()
    
    def _initialize_all_rags(self):
        """Initialize all RAG types."""
        from .classic.vanilla_rag import VanillaRAG, VanillaRAGConfig
        
        vanilla_config = VanillaRAGConfig(
            chunk_size=self.config.chunk_size,
            overlap=self.config.overlap,
            top_k=self.config.top_k,
            llm_model=self.config.llm_model,
            temperature=self.config.temperature
        )
        
        self._rag_instances[RAGType.VANILLA] = VanillaRAG(
            vector_store=self.vector_store,
            config=vanilla_config
        )
        
        if self.config.enable_memory:
            from .memory.memory_rag import MemoryRAG, MemoryStore
            memory_store = MemoryStore(
                use_redis=False,
                expiration_seconds=self.config.memory_expiration_hours * 3600
            )
            self._rag_instances[RAGType.MEMORY] = MemoryRAG(
                vanilla_rag=self._rag_instances[RAGType.VANILLA],
                memory_store=memory_store
            )
        
        self._rag_instances[RAGType.CRAG] = self._create_crag()
        
        self._rag_instances[RAGType.ADAPTIVE] = self._create_adaptive_rag()
        
        self._rag_instances[RAGType.HYDE] = self._create_hyde()
        
        self._rag_instances[RAGType.GRAPH] = self._create_graph_rag()
        
        self._rag_instances[RAGType.HYBRID] = self._create_hybrid_rag()
        
        self._rag_instances[RAGType.FUSION] = self._create_fusion_rag()
    
    def _create_crag(self):
        """Create CRAG instance."""
        from .corrective.crag import CRAG
        return CRAG(
            vanilla_rag=self._rag_instances.get(RAGType.VANILLA),
            enable_correction=self.config.enable_correction,
            enable_external_search=True
        )
    
    def _create_adaptive_rag(self):
        """Create Adaptive RAG instance."""
        from .adaptive.adaptive_rag import AdaptiveRAG
        return AdaptiveRAG(
            vanilla_rag=self._rag_instances.get(RAGType.VANILLA)
        )
    
    def _create_hyde(self):
        """Create HyDE instance."""
        from .hyde.hyde import HyDE
        return HyDE(
            vanilla_rag=self._rag_instances.get(RAGType.VANILLA),
            use_multiple_hypotheses=False
        )
    
    def _create_graph_rag(self):
        """Create GraphRAG instance."""
        from .graph.graph_rag import GraphRAG
        return GraphRAG(
            neo4j_connector=self.neo4j_connector,
            vector_store=self.vector_store
        )
    
    def _create_hybrid_rag(self):
        """Create Hybrid RAG instance."""
        from .hybrid.hybrid_rag import HybridRAG
        return HybridRAG(
            vector_store=self.vector_store,
            graph_rag=self._rag_instances.get(RAGType.GRAPH),
            vanilla_rag=self._rag_instances.get(RAGType.VANILLA),
            alpha=0.5
        )
    
    def _create_fusion_rag(self):
        """Create RAG-Fusion instance."""
        from .fusion.rag_fusion import RAGFusion
        return RAGFusion(
            vanilla_rag=self._rag_instances.get(RAGType.VANILLA),
            sources={}
        )
    
    def query(
        self,
        query: str,
        rag_type: Optional[Union[RAGType, str]] = None,
        session_id: str = "default",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Executa query usando o RAG especificado.
        
        Args:
            query: Query do usuário
            rag_type: Tipo de RAG a usar (None = config.default)
            session_id: ID da sessão (para Memory RAG)
            **kwargs: Parâmetros adicionais
            
        Returns:
            Resposta com metadados
        """
        if rag_type is None:
            rag_type = self.config.default_rag_type
        elif isinstance(rag_type, str):
            try:
                rag_type = RAGType(rag_type.lower())
            except ValueError:
                rag_type = self.config.default_rag_type
        
        if rag_type not in self._rag_instances:
            rag_type = RAGType.VANILLA
        
        self._stats.total_queries += 1
        self._stats.queries_by_type[rag_type.value] = \
            self._stats.queries_by_type.get(rag_type.value, 0) + 1
        
        try:
            if rag_type == RAGType.MEMORY and self.config.enable_memory:
                result = self._rag_instances[rag_type].query(
                    query,
                    session_id=session_id,
                    **kwargs
                )
            else:
                result = self._rag_instances[rag_type].query(query, **kwargs)
            
            result['rag_type_used'] = rag_type.value
            return result
            
        except Exception as e:
            return {
                'answer': f"Erro ao processar query: {str(e)}",
                'query': query,
                'rag_type_used': rag_type.value,
                'error': str(e)
            }
    
    def query_with_fallback(
        self,
        query: str,
        preferred_rag_type: RAGType = RAGType.ADAPTIVE,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query com fallback automático se o tipo principal falhar.
        """
        try:
            return self.query(query, preferred_rag_type, **kwargs)
        except Exception as e:
            print(f"Primary RAG failed: {e}. Falling back to Vanilla.")
            return self.query(query, RAGType.VANILLA, **kwargs)
    
    def query_batch(
        self,
        queries: List[str],
        rag_type: Optional[RAGType] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Executa múltiplas queries."""
        return [self.query(q, rag_type, **kwargs) for q in queries]
    
    def get_rag(self, rag_type: RAGType) -> Any:
        """Obtém instância de RAG específica."""
        return self._rag_instances.get(rag_type)
    
    def get_available_rag_types(self) -> List[Dict[str, Any]]:
        """Lista tipos de RAG disponíveis."""
        available = []
        for rag_type in RAGType:
            if rag_type in self._rag_instances:
                info = {
                    'name': rag_type.value,
                    'available': True,
                    'type': type(self._rag_instances[rag_type]).__name__
                }
                
                if rag_type == RAGType.MEMORY:
                    info['requires_session'] = True
                elif rag_type == RAGType.GRAPH:
                    info['requires_neo4j'] = True
                elif rag_type == RAGType.FUSION:
                    info['requires_sources'] = True
                
                available.append(info)
        
        return available
    
    def get_stats(self) -> RAGStats:
        """Retorna estatísticas do sistema."""
        return self._stats
    
    def set_default_rag(self, rag_type: Union[RAGType, str]):
        """Define tipo de RAG padrão."""
        if isinstance(rag_type, str):
            rag_type = RAGType(rag_type.lower())
        self.config.default_rag_type = rag_type
    
    def add_source_to_fusion(self, name: str, source: Any):
        """Adiciona fonte ao RAG-Fusion."""
        if RAGType.FUSION in self._rag_instances:
            self._rag_instances[RAGType.FUSION].add_source(name, source)
            
            if name not in self._stats.sources_used:
                self._stats.sources_used.append(name)
    
    def create_session(self, session_id: str) -> bool:
        """Cria nova sessão para Memory RAG."""
        if RAGType.MEMORY in self._rag_instances:
            return self._rag_instances[RAGType.MEMORY].memory_store.clear_session(session_id)
        return False
    
    def clear_session(self, session_id: str) -> bool:
        """Limpa sessão."""
        if RAGType.MEMORY in self._rag_instances:
            return self._rag_instances[RAGType.MEMORY].clear_session(session_id)
        return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """Retorna informações completas do sistema."""
        return {
            'config': {
                'default_rag': self.config.default_rag_type.value,
                'top_k': self.config.top_k,
                'chunk_size': self.config.chunk_size,
                'llm_model': self.config.llm_model,
                'enable_correction': self.config.enable_correction,
                'enable_memory': self.config.enable_memory
            },
            'available_rags': self.get_available_rag_types(),
            'stats': {
                'total_queries': self._stats.total_queries,
                'queries_by_type': self._stats.queries_by_type,
                'sources_configured': len(self._stats.sources_used)
            },
            'components': {
                'vector_store': self.vector_store is not None,
                'neo4j': self.neo4j_connector is not None
            }
        }


class MASWOSRAGBuilder:
    """
    Builder para configurar o RAG Orchestrator.
    """
    
    def __init__(self):
        self._config = RAGConfig()
        self._vector_store = None
        self._neo4j_connector = None
        self._sources = {}
    
    def with_vector_store(self, vector_store: Any) -> 'MASWOSRAGBuilder':
        """Adiciona vector store."""
        self._vector_store = vector_store
        return self
    
    def with_neo4j(self, connector: Any) -> 'MASWOSRAGBuilder':
        """Adiciona conector Neo4j."""
        self._neo4j_connector = connector
        return self
    
    def with_default_rag(self, rag_type: RAGType) -> 'MASWOSRAGBuilder':
        """Define RAG padrão."""
        self._config.default_rag_type = rag_type
        return self
    
    def with_correction(self, enabled: bool) -> 'MASWOSRAGBuilder':
        """Habilita correção CRAG."""
        self._config.enable_correction = enabled
        return self
    
    def with_memory(self, enabled: bool) -> 'MASWOSRAGBuilder':
        """Habilita memória."""
        self._config.enable_memory = enabled
        return self
    
    def with_source(self, name: str, source: Any) -> 'MASWOSRAGBuilder':
        """Adiciona fonte para RAG-Fusion."""
        self._sources[name] = source
        return self
    
    def with_llm_model(self, model: str) -> 'MASWOSRAGBuilder':
        """Define modelo LLM."""
        self._config.llm_model = model
        return self
    
    def with_chunking(self, size: int, overlap: int) -> 'MASWOSRAGBuilder':
        """Define parâmetros de chunking."""
        self._config.chunk_size = size
        self._config.overlap = overlap
        return self
    
    def build(self) -> RAGOrchestrator:
        """Constrói o orchestrator."""
        orchestrator = RAGOrchestrator(
            config=self._config,
            vector_store=self._vector_store,
            neo4j_connector=self._neo4j_connector
        )
        
        for name, source in self._sources.items():
            orchestrator.add_source_to_fusion(name, source)
        
        return orchestrator
