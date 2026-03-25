"""
Encoder - Text to vector embeddings for RAG
Handles conversion of text chunks to vector representations.
"""

from typing import List, Dict, Any, Optional, Union, TYPE_CHECKING, cast
import numpy as np
from dataclasses import dataclass

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer


@dataclass
class EmbeddingResult:
    """Container for embedding results."""
    texts: List[str]
    embeddings: np.ndarray
    model: str
    dimensions: int
    metadata: Optional[Dict[str, Any]] = None


class Encoder:
    """
    Converts text to vector embeddings using sentence transformers.
    
    Supports multiple embedding models and configurations.
    """
    
    DEFAULT_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'
    
    SUPPORTED_MODELS = {
        'mini': 'paraphrase-multilingual-MiniLM-L12-v2',
        'base': 'paraphrase-multilingual-mpnet-base-v2',
        'large': 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
        'e5': 'intfloat/multilingual-e5-base',
        'e5_small': 'intfloat/multilingual-e5-small',
    }
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: Optional[str] = None,
        normalize: bool = True,
        batch_size: int = 32,
        show_progress: bool = False
    ):
        self.model_name = model_name
        self.device = device
        self.normalize = normalize
        self.batch_size = batch_size
        self.show_progress = show_progress
        
        self._model: Optional["SentenceTransformer"] = None
        self._dimensions: Optional[int] = None
    
    def _init_model(self):
        """Lazy initialization of the embedding model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                
                model_key = self.model_name.lower()
                actual_model = self.SUPPORTED_MODELS.get(model_key, self.model_name)
                
                self._model = SentenceTransformer(
                    actual_model,
                    device=self.device
                )
                self._dimensions = self._model.get_sentence_embedding_dimension()
                
            except ImportError:
                raise ImportError(
                    "sentence_transformers is required for Encoder. "
                    "Install with: pip install sentence-transformers"
                )
    
    @property
    def dimensions(self) -> int:
        """Return embedding dimensions."""
        if self._dimensions is None:
            self._init_model()
        assert self._dimensions is not None
        return self._dimensions
    
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encode text(s) to embeddings.
        
        Args:
            texts: Single text or list of texts
            
        Returns:
            Numpy array of embeddings
        """
        self._init_model()
        model = cast("SentenceTransformer", self._model)
        
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=self.show_progress,
            normalize_embeddings=self.normalize,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def encode_with_metadata(
        self, 
        texts: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None
    ) -> EmbeddingResult:
        """
        Encode texts with associated metadata.
        
        Args:
            texts: List of texts to encode
            metadata: Optional metadata for each text
            
        Returns:
            EmbeddingResult with all information
        """
        embeddings = self.encode(texts)
        
        return EmbeddingResult(
            texts=texts,
            embeddings=embeddings,
            model=self.model_name,
            dimensions=self.dimensions,
            metadata={
                'count': len(texts),
                'metadata_provided': metadata is not None
            }
        )
    
    def compute_similarity(
        self, 
        text_a: str, 
        text_b: str
    ) -> float:
        """Compute cosine similarity between two texts."""
        emb_a = self.encode(text_a)
        emb_b = self.encode(text_b)
        
        return float(np.dot(emb_a, emb_b) / (np.linalg.norm(emb_a) * np.linalg.norm(emb_b)))
    
    def compute_similarities(
        self,
        query: str,
        texts: List[str]
    ) -> List[float]:
        """Compute similarity between query and multiple texts."""
        query_emb = self.encode(query)
        text_embs = self.encode(texts)
        
        similarities = np.dot(text_embs, query_emb) / (
            np.linalg.norm(text_embs, axis=1) * np.linalg.norm(query_emb)
        )
        
        return similarities.tolist()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Return information about the current model."""
        self._init_model()
        model = cast("SentenceTransformer", self._model)
        
        return {
            'model_name': self.model_name,
            'dimensions': self.dimensions,
            'max_seq_length': model.get_max_seq_length(),
            'normalize': self.normalize,
            'batch_size': self.batch_size
        }


class AcademicEncoder(Encoder):
    """
    Specialized encoder for academic texts.
    Optimized for scientific terminology and citations.
    """
    
    def __init__(
        self,
        model_name: str = 'paraphrase-multilingual-mpnet-base-v2',
        device: Optional[str] = None
    ):
        super().__init__(
            model_name=model_name,
            device=device,
            normalize=True,
            batch_size=16
        )
        self._citation_pattern = None
    
    def preprocess_academic_text(self, text: str) -> str:
        """Preprocess academic text for better embedding quality."""
        import re
        
        text = re.sub(r'\s+', ' ', text)
        
        text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '[CITATION]', text)
        
        text = re.sub(r'https?://\S+', '[URL]', text)
        
        text = re.sub(r'\b(\d+(?:\.\d+)?)\s*%', r'\1 PERCENT', text)
        
        return text.strip()
    
    def encode_academic(self, text: str) -> np.ndarray:
        """Encode academic text with preprocessing."""
        processed = self.preprocess_academic_text(text)
        return self.encode(processed)


class HybridEncoder(Encoder):
    """
    Hybrid encoder combining multiple embedding models.
    Useful for capturing different aspects of text meaning.
    """
    
    def __init__(
        self,
        semantic_model: str = 'mini',
        keyword_model: Optional[str] = None
    ):
        super().__init__(model_name=semantic_model)
        
        self.keyword_encoder = None
        if keyword_model:
            self.keyword_encoder = Encoder(
                model_name=keyword_model,
                normalize=True
            )
    
    def encode_hybrid(
        self,
        texts: List[str],
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3
    ) -> np.ndarray:
        """
        Combine semantic and keyword embeddings.
        
        Args:
            texts: List of texts to encode
            semantic_weight: Weight for semantic embeddings
            keyword_weight: Weight for keyword embeddings
            
        Returns:
            Combined embedding vectors
        """
        semantic_emb = self.encode(texts)
        
        if self.keyword_encoder:
            keyword_emb = self.keyword_encoder.encode(texts)
            
            combined = (semantic_weight * semantic_emb) + (keyword_weight * keyword_emb)
            
            norms = np.linalg.norm(combined, axis=1, keepdims=True)
            combined = combined / norms
            
            return combined
        else:
            return semantic_emb
