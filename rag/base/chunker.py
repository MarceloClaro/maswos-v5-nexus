"""
Chunker - Text segmentation for RAG
Handles splitting documents into manageable chunks with overlap.
"""

import re
import numpy as np
from typing import List, Dict, Any, Optional, TYPE_CHECKING, cast
from dataclasses import dataclass

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer


@dataclass
class Chunk:
    """Represents a text chunk with metadata."""
    id: str
    text: str
    start_index: int
    end_index: int
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Chunker:
    """
    Segments documents into overlapping chunks for RAG processing.
    
    Parameters:
        chunk_size: Maximum size of each chunk in characters
        overlap: Number of overlapping characters between chunks
        separators: List of separators to use for splitting (in priority order)
    """
    
    DEFAULT_SEPARATORS = [
        '\n\n\n',  # Triple newline (paragraphs)
        '\n\n',    # Double newline  
        '\n',      # Single newline
        '. ',      # Sentence end
        '; ',      # Semicolon
        ', ',      # Comma
        ' ',       # Space
    ]
    
    def __init__(
        self,
        chunk_size: int = 2000,
        overlap: int = 500,
        separators: Optional[List[str]] = None,
        min_chunk_size: int = 100
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separators = separators or self.DEFAULT_SEPARATORS
        self.min_chunk_size = min_chunk_size
        
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk_size")
    
    def chunk_text(self, text: str, source: str = "unknown") -> List[Chunk]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            source: Source document identifier
            
        Returns:
            List of Chunk objects
        """
        if not text or not text.strip():
            return []
        
        chunks = []
        text_length = len(text)
        current_pos = 0
        chunk_id = 0
        
        while current_pos < text_length:
            chunk_end = min(current_pos + self.chunk_size, text_length)
            
            if chunk_end < text_length:
                chunk_end = self._find_best_split_point(text, current_pos, chunk_end)
            
            chunk_text = text[current_pos:chunk_end].strip()
            
            if len(chunk_text) >= self.min_chunk_size:
                chunk = Chunk(
                    id=f"chunk_{source}_{chunk_id}",
                    text=chunk_text,
                    start_index=current_pos,
                    end_index=chunk_end,
                    source=source,
                    metadata={
                        'chunk_size': len(chunk_text),
                        'chunk_index': chunk_id,
                        'total_chunks_estimate': (text_length // (self.chunk_size - self.overlap)) + 1
                    }
                )
                chunks.append(chunk)
                chunk_id += 1
            
            current_pos = chunk_end - self.overlap
            
            if current_pos <= (chunks[-1].start_index if chunks else 0):
                current_pos = (chunks[-1].end_index if chunks else 0) + 1
                if current_pos >= text_length:
                    break
        
        return chunks
    
    def _find_best_split_point(self, text: str, start: int, end: int) -> int:
        """Find the best position to split text to maintain semantic boundaries."""
        for separator in self.separators:
            split_pos = text.rfind(separator, start, end)
            if split_pos > start + self.min_chunk_size:
                return split_pos + len(separator)
        
        return end
    
    def chunk_documents(self, documents: Dict[str, str]) -> List[Chunk]:
        """
        Chunk multiple documents.
        
        Args:
            documents: Dictionary mapping source names to text content
            
        Returns:
            Flat list of all chunks from all documents
        """
        all_chunks = []
        for source, text in documents.items():
            chunks = self.chunk_text(text, source)
            all_chunks.extend(chunks)
        return all_chunks
    
    def chunk_with_metadata(
        self, 
        text: str, 
        source: str,
        extra_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """Chunk text with additional metadata."""
        chunks = self.chunk_text(text, source)
        
        if extra_metadata:
            for chunk in chunks:
                if chunk.metadata:
                    chunk.metadata.update(extra_metadata)
                else:
                    chunk.metadata = extra_metadata
        
        return chunks
    
    def get_chunk_info(self) -> Dict[str, Any]:
        """Return current chunking configuration."""
        return {
            'chunk_size': self.chunk_size,
            'overlap': self.overlap,
            'step': self.chunk_size - self.overlap,
            'min_chunk_size': self.min_chunk_size,
            'separators_count': len(self.separators)
        }
    
    def update_settings(
        self, 
        chunk_size: Optional[int] = None,
        overlap: Optional[int] = None
    ):
        """Update chunking parameters dynamically."""
        if chunk_size is not None:
            if chunk_size < self.min_chunk_size:
                raise ValueError(f"chunk_size must be at least {self.min_chunk_size}")
            self.chunk_size = chunk_size
        
        if overlap is not None:
            if overlap >= self.chunk_size:
                raise ValueError("overlap must be smaller than chunk_size")
            self.overlap = overlap


class SemanticChunker(Chunker):
    """
    Enhanced chunker that uses semantic boundaries for better splits.
    Uses embeddings to identify topic shifts within text.
    """
    
    def __init__(
        self,
        chunk_size: int = 2000,
        overlap: int = 500,
        min_chunk_size: int = 100,
        similarity_threshold: float = 0.3
    ):
        super().__init__(chunk_size, overlap, min_chunk_size=min_chunk_size)
        self.similarity_threshold = similarity_threshold
        self._encoder: Optional["SentenceTransformer"] = None
    
    def _init_encoder(self):
        """Lazy initialization of encoder."""
        if self._encoder is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._encoder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            except ImportError:
                raise ImportError("sentence_transformers required for SemanticChunker")
    
    def semantic_chunk_text(self, text: str, source: str = "unknown") -> List[Chunk]:
        """
        Split text using semantic similarity to detect topic boundaries.
        
        This creates more coherent chunks by detecting when the topic changes.
        """
        self._init_encoder()
        encoder = cast("SentenceTransformer", self._encoder)
        
        sentences = self._split_into_sentences(text)
        if not sentences:
            return self.chunk_text(text, source)
        
        embeddings = encoder.encode(sentences)
        
        chunk_boundaries = [0]
        for i in range(1, len(sentences)):
            similarity = self._cosine_similarity(embeddings[i-1], embeddings[i])
            
            if similarity < self.similarity_threshold:
                chunk_boundaries.append(i)
        
        chunks = []
        chunk_id = 0
        for idx, boundary in enumerate(chunk_boundaries):
            next_boundary = chunk_boundaries[idx + 1] if idx + 1 < len(chunk_boundaries) else len(sentences)
            
            chunk_text = ' '.join(sentences[boundary:next_boundary])
            
            if len(chunk_text.strip()) >= self.min_chunk_size:
                start_pos = sum(len(s) + 1 for s in sentences[:boundary])
                end_pos = start_pos + len(chunk_text)
                
                chunk = Chunk(
                    id=f"semantic_chunk_{source}_{chunk_id}",
                    text=chunk_text,
                    start_index=start_pos,
                    end_index=end_pos,
                    source=source,
                    metadata={
                        'chunk_type': 'semantic',
                        'chunk_size': len(chunk_text),
                        'chunk_index': chunk_id,
                        'sentence_count': next_boundary - boundary
                    }
                )
                chunks.append(chunk)
                chunk_id += 1
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        sentence_pattern = r'(?<=[.!?])\s+'
        sentences = re.split(sentence_pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _cosine_similarity(self, a, b) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
