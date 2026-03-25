"""
RAG Clássico (Vanilla RAG) - Implementação MASWOS Academic
Fluxo básico: Retriever → Augmentation → Generation
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..base.chunker import Chunker, SemanticChunker
from ..base.encoder import Encoder, AcademicEncoder
from ..base.retriever import Retriever, RetrievalResult, RetrievalStrategy
from ..base.augmenter import Augmenter, AugmentedPrompt
from ..base.generator import Generator, GenerationResult, GenerationConfig, AcademicGenerator


@dataclass
class VanillaRAGConfig:
    """Configuration for Vanilla RAG."""
    chunk_size: int = 2000
    overlap: int = 500
    top_k: int = 5
    model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"
    llm_model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    use_semantic_chunking: bool = False


class VanillaRAG:
    """
    Implementação do RAG Clássico para MASWOS Academic.
    
    Fluxo:
    1. Query → Encoder → Embedding
    2. Embedding → Vector Store → Similarity Search → Chunks
    3. Query + Chunks → Augmenter → Prompt
    4. Prompt → LLM → Generation
    """
    
    def __init__(
        self,
        vector_store: Any = None,
        config: Optional[VanillaRAGConfig] = None,
        **kwargs
    ):
        self.config = config or VanillaRAGConfig()
        self.vector_store = vector_store
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all RAG components."""
        if self.config.use_semantic_chunking:
            self.chunker = SemanticChunker(
                chunk_size=self.config.chunk_size,
                overlap=self.config.overlap
            )
        else:
            self.chunker = Chunker(
                chunk_size=self.config.chunk_size,
                overlap=self.config.overlap
            )
        
        self.encoder = AcademicEncoder(
            model_name=self.config.model_name
        )
        
        self.retriever = Retriever(
            vector_store=self.vector_store,
            default_top_k=self.config.top_k,
            default_strategy=RetrievalStrategy.SIMILARITY
        )
        
        self.augmenter = Augmenter(
            template=Augmenter.ACADEMIC_TEMPLATE,
            max_context_length=6000
        )
        
        self.generator = AcademicGenerator(
            model=self.config.llm_model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
    
    def index_documents(
        self,
        documents: Dict[str, str],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Index documents for retrieval.
        
        Args:
            documents: Dictionary mapping source names to text content
            
        Returns:
            Index statistics
        """
        if show_progress:
            print(f"Indexando {len(documentos)} documentos...")
        
        all_chunks = self.chunker.chunk_documents(documents)
        
        if show_progress:
            print(f"Criados {len(all_chunks)} chunks")
        
        texts = [chunk.text for chunk in all_chunks]
        metadatas = [
            {
                'source': chunk.source,
                'chunk_id': chunk.id,
                'index': i
            }
            for i, chunk in enumerate(all_chunks)
        ]
        
        embeddings = self.encoder.encode(texts)
        
        if self.vector_store:
            self.vector_store.add_documents(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
        
        return {
            'documents_indexed': len(documents),
            'chunks_created': len(all_chunks),
            'embedding_dimensions': embeddings.shape[1],
            'index_name': getattr(self.vector_store, 'collection_name', 'unknown')
        }
    
    def query(
        self,
        query: str,
        top_k: Optional[int] = None,
        return_chunks: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process a query through the full RAG pipeline.
        
        Args:
            query: User query
            top_k: Number of chunks to retrieve
            return_chunks: Whether to include retrieved chunks in response
            
        Returns:
            Dictionary with answer and metadata
        """
        top_k = top_k or self.config.top_k
        
        retrieval_result = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            **kwargs
        )
        
        chunks_data = [
            {
                'text': chunk.text,
                'score': chunk.score,
                'source': chunk.source,
                'rank': chunk.rank
            }
            for chunk in retrieval_result.chunks
        ]
        
        augmented = self.augmenter.augment(
            query=query,
            retrieved_chunks=chunks_data
        )
        
        generation_result = self.generator.generate(
            prompt=augmented.augmented_prompt
        )
        
        response = {
            'answer': generation_result.text,
            'query': query,
            'strategy': retrieval_result.strategy.value,
            'chunks_retrieved': retrieval_result.total_results,
            'latency_ms': retrieval_result.execution_time_ms + generation_result.latency_ms,
            'tokens_used': generation_result.token_count
        }
        
        if return_chunks:
            response['retrieved_chunks'] = chunks_data
        
        return response
    
    def query_with_citations(
        self,
        query: str,
        top_k: Optional[int] = None,
        citation_style: str = "abnt"
    ) -> Dict[str, Any]:
        """
        Query with proper citation handling.
        
        Args:
            query: User query
            top_k: Number of chunks to retrieve
            citation_style: Citation format (abnt, apa, etc.)
            
        Returns:
            Dictionary with answer, citations, and metadata
        """
        top_k = top_k or self.config.top_k
        
        retrieval_result = self.retriever.retrieve(
            query=query,
            top_k=top_k
        )
        
        chunks_data = [
            {
                'text': chunk.text,
                'score': chunk.score,
                'source': chunk.source,
                'rank': chunk.rank
            }
            for chunk in retrieval_result.chunks
        ]
        
        augmented = self.augmenter.augment(
            query=query,
            retrieved_chunks=chunks_data
        )
        
        generation_result = self.generator.generate_with_citations(
            prompt=augmented.augmented_prompt,
            context_chunks=chunks_data
        )
        
        return {
            'answer': generation_result.text,
            'citations': generation_result.citations,
            'sources': list(set([c['source'] for c in chunks_data])),
            'query': query,
            'metadata': {
                'chunks_retrieved': retrieval_result.total_results,
                'latency_ms': generation_result.latency_ms,
                'citation_style': citation_style
            }
        }
    
    def batch_query(
        self,
        queries: List[str],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Process multiple queries."""
        return [self.query(q, **kwargs) for q in queries]
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """Return pipeline configuration and status."""
        return {
            'type': 'Vanilla RAG',
            'config': {
                'chunk_size': self.config.chunk_size,
                'overlap': self.config.overlap,
                'top_k': self.config.top_k,
                'model_name': self.config.model_name,
                'llm_model': self.config.llm_model,
                'use_semantic_chunking': self.config.use_semantic_chunking
            },
            'components': {
                'chunker': type(self.chunker).__name__,
                'encoder': type(self.encoder).__name__,
                'retriever': type(self.retriever).__name__,
                'augmenter': type(self.augmenter).__name__,
                'generator': type(self.generator).__name__
            },
            'vector_store_configured': self.vector_store is not None
        }
