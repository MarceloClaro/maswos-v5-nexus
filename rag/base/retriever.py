"""
Retriever - Document retrieval for RAG
Handles similarity search and document retrieval from vector stores.
"""

import time
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING, cast
import numpy as np
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from .encoder import Encoder


class RetrievalStrategy(Enum):
    """Available retrieval strategies."""
    SIMILARITY = "similarity"
    MMR = "mmr"  # Maximum Marginal Relevance
    SIMILARITY_THRESHOLD = "similarity_threshold"
    HYBRID = "hybrid"


@dataclass
class RetrievedChunk:
    """Represents a retrieved chunk with score and metadata."""
    text: str
    score: float
    source: str
    chunk_id: str
    metadata: Optional[Dict[str, Any]] = None
    rank: Optional[int] = None


@dataclass
class RetrievalResult:
    """Container for retrieval results."""
    query: str
    chunks: List[RetrievedChunk]
    strategy: RetrievalStrategy
    total_results: int
    execution_time_ms: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class Retriever:
    """
    Retrieves relevant documents from vector store.
    
    Supports multiple retrieval strategies including:
    - Similarity search
    - Maximum Marginal Relevance (MMR)
    - Threshold-based retrieval
    - Hybrid retrieval
    """
    
    def __init__(
        self,
        vector_store: Any = None,
        default_top_k: int = 5,
        default_strategy: RetrievalStrategy = RetrievalStrategy.SIMILARITY,
        similarity_threshold: float = 0.5,
        mmr_lambda: float = 0.5  # Balance relevance vs diversity
    ):
        self.vector_store = vector_store
        self.default_top_k = default_top_k
        self.default_strategy = default_strategy
        self.similarity_threshold = similarity_threshold
        self.mmr_lambda = mmr_lambda
        
        self._encoder: Optional["Encoder"] = None
    
    def _init_encoder(self):
        """Lazy initialization of encoder."""
        if self._encoder is None:
            from .encoder import Encoder
            self._encoder = Encoder()
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        strategy: Optional[RetrievalStrategy] = None,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> RetrievalResult:
        """
        Retrieve relevant chunks for a query.
        
        Args:
            query: Search query
            top_k: Number of results to return
            strategy: Retrieval strategy to use
            filters: Metadata filters
            **kwargs: Additional strategy-specific parameters
            
        Returns:
            RetrievalResult with ranked chunks
        """
        import time
        start_time = time.time()
        
        top_k = top_k or self.default_top_k
        strategy = strategy or self.default_strategy
        
        if self.vector_store is None:
            raise ValueError("Vector store not configured")
        
        if strategy == RetrievalStrategy.SIMILARITY:
            return self._retrieve_similarity(query, top_k, filters, start_time)
        elif strategy == RetrievalStrategy.MMR:
            return self._retrieve_mmr(query, top_k, filters, start_time, **kwargs)
        elif strategy == RetrievalStrategy.SIMILARITY_THRESHOLD:
            return self._retrieve_threshold(query, filters, start_time)
        elif strategy == RetrievalStrategy.HYBRID:
            return self._retrieve_hybrid(query, top_k, filters, start_time, **kwargs)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _retrieve_similarity(
        self,
        query: str,
        top_k: int,
        filters: Optional[Dict[str, Any]],
        start_time: float
    ) -> RetrievalResult:
        """Standard similarity-based retrieval."""
        self._init_encoder()
        encoder = cast("Encoder", self._encoder)
        
        query_embedding = encoder.encode(query)
        
        results = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            k=top_k,
            filters=filters
        )
        
        chunks = []
        for rank, result in enumerate(results):
            chunk = RetrievedChunk(
                text=result.get('text', ''),
                score=result.get('score', 0.0),
                source=result.get('source', 'unknown'),
                chunk_id=result.get('id', f'rank_{rank}'),
                metadata=result.get('metadata'),
                rank=rank + 1
            )
            chunks.append(chunk)
        
        execution_time = (time.time() - start_time) * 1000
        
        return RetrievalResult(
            query=query,
            chunks=chunks,
            strategy=RetrievalStrategy.SIMILARITY,
            total_results=len(chunks),
            execution_time_ms=execution_time
        )
    
    def _retrieve_mmr(
        self,
        query: str,
        top_k: int,
        filters: Optional[Dict[str, Any]],
        start_time: float,
        fetch_k: int = 20,
        **kwargs
    ) -> RetrievalResult:
        """
        Maximum Marginal Relevance retrieval.
        Balances relevance with diversity in results.
        """
        self._init_encoder()
        encoder = cast("Encoder", self._encoder)
        
        mmr_lambda = kwargs.get('mmr_lambda', self.mmr_lambda)
        
        query_embedding = encoder.encode(query)
        
        results = self.vector_store.max_marginal_relevance_search(
            query_embedding=query_embedding,
            k=top_k,
            fetch_k=fetch_k,
            lambda_mult=mmr_lambda,
            filters=filters
        )
        
        chunks = []
        for rank, result in enumerate(results):
            chunk = RetrievedChunk(
                text=result.get('text', ''),
                score=result.get('score', 0.0),
                source=result.get('source', 'unknown'),
                chunk_id=result.get('id', f'rank_{rank}'),
                metadata=result.get('metadata'),
                rank=rank + 1
            )
            chunks.append(chunk)
        
        execution_time = (time.time() - start_time) * 1000
        
        return RetrievalResult(
            query=query,
            chunks=chunks,
            strategy=RetrievalStrategy.MMR,
            total_results=len(chunks),
            execution_time_ms=execution_time,
            metadata={'mmr_lambda': mmr_lambda}
        )
    
    def _retrieve_threshold(
        self,
        query: str,
        filters: Optional[Dict[str, Any]],
        start_time: float,
        threshold: Optional[float] = None
    ) -> RetrievalResult:
        """Threshold-based retrieval."""
        self._init_encoder()
        encoder = cast("Encoder", self._encoder)
        
        threshold = threshold or self.similarity_threshold
        
        query_embedding = encoder.encode(query)
        
        results = self.vector_store.similarity_search_with_score(
            query_embedding=query_embedding,
            k=100,  # Get more to filter
            filters=filters
        )
        
        chunks = []
        for rank, result in enumerate(results):
            score = result.get('score', 0.0)
            if score >= threshold:
                chunk = RetrievedChunk(
                    text=result.get('text', ''),
                    score=score,
                    source=result.get('source', 'unknown'),
                    chunk_id=result.get('id', f'rank_{rank}'),
                    metadata=result.get('metadata'),
                    rank=len(chunks) + 1
                )
                chunks.append(chunk)
        
        execution_time = (time.time() - start_time) * 1000
        
        return RetrievalResult(
            query=query,
            chunks=chunks,
            strategy=RetrievalStrategy.SIMILARITY_THRESHOLD,
            total_results=len(chunks),
            execution_time_ms=execution_time,
            metadata={'threshold': threshold}
        )
    
    def _retrieve_hybrid(
        self,
        query: str,
        top_k: int,
        filters: Optional[Dict[str, Any]],
        start_time: float,
        alpha: float = 0.5,
        **kwargs
    ) -> RetrievalResult:
        """
        Hybrid retrieval combining semantic and keyword search.
        """
        self._init_encoder()
        encoder = cast("Encoder", self._encoder)
        
        alpha = kwargs.get('alpha', alpha)
        
        query_embedding = encoder.encode(query)
        
        results = self.vector_store.hybrid_search(
            query=query,
            query_embedding=query_embedding,
            k=top_k,
            alpha=alpha,
            filters=filters
        )
        
        chunks = []
        for rank, result in enumerate(results):
            chunk = RetrievedChunk(
                text=result.get('text', ''),
                score=result.get('score', 0.0),
                source=result.get('source', 'unknown'),
                chunk_id=result.get('id', f'rank_{rank}'),
                metadata=result.get('metadata'),
                rank=rank + 1
            )
            chunks.append(chunk)
        
        execution_time = (time.time() - start_time) * 1000
        
        return RetrievalResult(
            query=query,
            chunks=chunks,
            strategy=RetrievalStrategy.HYBRID,
            total_results=len(chunks),
            execution_time_ms=execution_time,
            metadata={'alpha': alpha}
        )
    
    def get_retriever_info(self) -> Dict[str, Any]:
        """Return retriever configuration."""
        return {
            'default_top_k': self.default_top_k,
            'default_strategy': self.default_strategy.value,
            'similarity_threshold': self.similarity_threshold,
            'mmr_lambda': self.mmr_lambda,
            'vector_store_configured': self.vector_store is not None
        }


class AcademicRetriever(Retriever):
    """
    Specialized retriever for academic documents.
    Optimized for scholarly articles, citations, and technical content.
    """
    
    def __init__(self, vector_store: Any = None, **kwargs):
        super().__init__(vector_store, **kwargs)
        
        self.citation_boost = kwargs.get('citation_boost', 1.2)
        self.recency_boost = kwargs.get('recency_boost', 1.1)
    
    def retrieve_academic(
        self,
        query: str,
        top_k: Optional[int] = None,
        include_citations: bool = True,
        year_range: Optional[Tuple[int, int]] = None,
        **kwargs
    ) -> RetrievalResult:
        """
        Retrieve academic documents with specialized ranking.
        
        Args:
            query: Search query
            top_k: Number of results
            include_citations: Boost documents with citations
            year_range: Filter by publication year (start, end)
        """
        filters = {}
        
        if year_range:
            filters['year'] = {'$gte': year_range[0], '$lte': year_range[1]}
        
        result = self.retrieve(
            query=query,
            top_k=top_k or self.default_top_k,
            filters=filters if filters else None,
            **kwargs
        )
        
        if include_citations:
            if result.metadata is None:
                result.metadata = {}
            result.metadata['citation_boost_applied'] = True
        
        return result
    
    def retrieve_by_citation_network(
        self,
        seed_documents: List[str],
        top_k: int = 10,
        depth: int = 2
    ) -> List[str]:
        """
        Retrieve documents through citation network expansion.
        
        Starts from seed documents and expands through citations.
        """
        visited = set(seed_documents)
        frontier = list(seed_documents)
        results = []
        
        while frontier and len(results) < top_k * depth:
            current = frontier.pop(0)
            
            cited_by = self.vector_store.get_cited_by(current)
            
            for doc in cited_by:
                if doc not in visited:
                    visited.add(doc)
                    frontier.append(doc)
                    results.append(doc)
        
        return results[:top_k]
