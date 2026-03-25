"""
MASWOS Academic RAG Module - Main Entry Point
"""

from typing import Any

from .base import Chunker, Encoder, Retriever, Augmenter, Generator

from .classic.vanilla_rag import VanillaRAG, VanillaRAGConfig

from .memory.memory_rag import MemoryRAG, MemoryStore, ConversationManager

from .agentic.agentic_rag import AgenticRAG, Dataset, QueryClassifier, DatasetRouter

from .graph.graph_rag import GraphRAG, KnowledgeGraph, Entity, Relation, EntityExtractor, Neo4jConnector

from .hybrid.hybrid_rag import HybridRAG

from .corrective.crag import CRAG, QualityEvaluator, RetrievalCorrector

from .adaptive.adaptive_rag import AdaptiveRAG, QueryAnalyzer

from .fusion.rag_fusion import RAGFusion, RRFScorer

from .hyde.hyde import HyDE, HypotheticalDocumentGenerator

from .orchestrator.rag_orchestrator import (
    RAGOrchestrator,
    MASWOSRAGBuilder,
    RAGType,
    RAGConfig,
    RAGStats
)

__version__ = "1.0.0"

__all__ = [
    # Base components
    'Chunker',
    'Encoder',
    'Retriever', 
    'Augmenter',
    'Generator',
    
    # RAG implementations
    'VanillaRAG',
    'VanillaRAGConfig',
    'MemoryRAG',
    'MemoryStore',
    'ConversationManager',
    'AgenticRAG',
    'Dataset',
    'GraphRAG',
    'KnowledgeGraph',
    'Entity',
    'Relation',
    'HybridRAG',
    'CRAG',
    'AdaptiveRAG',
    'RAGFusion',
    'HyDE',
    
    # Orchestrator
    'RAGOrchestrator',
    'MASWOSRAGBuilder',
    'RAGType',
    'RAGConfig',
    'RAGStats'
]


def create_orchestrator(
    default_type: str = "adaptive",
    vector_store: Any = None,
    neo4j: Any = None,
    enable_correction: bool = True,
    enable_memory: bool = True,
    llm_model: str = "gpt-4"
) -> RAGOrchestrator:
    """
    Factory function to create a configured RAG orchestrator.
    
    Example:
        >>> orchestrator = create_orchestrator(
        ...     default_type="adaptive",
        ...     enable_correction=True
        ... )
        >>> result = orchestrator.query("Qual a capital do Brasil?")
    """
    builder = MASWOSRAGBuilder()
    
    if vector_store:
        builder = builder.with_vector_store(vector_store)
    
    if neo4j:
        builder = builder.with_neo4j(neo4j)
    
    try:
        rag_type = RAGType(default_type)
        builder = builder.with_default_rag(rag_type)
    except ValueError:
        pass
    
    builder = builder.with_correction(enable_correction)
    builder = builder.with_memory(enable_memory)
    builder = builder.with_llm_model(llm_model)
    
    return builder.build()


# Quick usage examples
EXAMPLE_QUERIES = {
    "factual": "Qual a capital do Brasil?",
    "analytical": "Explique a relação entre educação e desenvolvimento econômico.",
    "comparative": "Compare os sistemas educacionais do Brasil e da Finlândia.",
    "complex": "Quais são os impactos de longo prazo da desigualdade educacional no crescimento econômico?"
}
