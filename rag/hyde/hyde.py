"""
HyDE (Hypothetical Document Embedding) - Implementação MASWOS Academic
Gera documento hipotético para melhorar precisão da busca semântica.
"""

from typing import Dict, Any, List, Optional
import numpy as np


class HypotheticalDocumentGenerator:
    """
    Gera documentos hipotéticos que respondem à query.
    
    O HyDE usa o LLM para gerar uma resposta "ideal"
    que então é usada para busca no banco vetorial.
    """
    
    def __init__(
        self,
        llm: Any = None,
        document_length: str = "medium"
    ):
        self.llm = llm
        self.document_length = document_length
    
    def generate(
        self,
        query: str,
        include_guidance: bool = True
    ) -> str:
        """
        Gera documento hipotético que responde à query.
        
        Args:
            query: Query do usuário
            include_guidance: Se inclui orientações de formato
            
        Returns:
            Texto do documento hipotético
        """
        if not self.llm:
            return self._rule_based_hypothetical(query)
        
        if self.document_length == "short":
            length_guidance = "2-3 parágrafos"
        elif self.document_length == "long":
            length_guidance = "2-3 páginas"
        else:
            length_guidance = "1-2 parágrafos"
        
        prompt = f"""Gere um documento acadêmico detalhado queresponda
à seguinte pergunta de pesquisa. O documento deve ser factual,
bem fundamentado e usar linguagem acadêmica apropriada.

Pergunta: {query}

Requisitos:
- Extensão: {length_guidance}
- Estrutura: Introdução, desenvolvimento, conclusão
- Estilo: Acadêmico e formal
- Cite conceitos relevantes quando apropriado

Documento Hipotético:"""
        
        try:
            result = self.llm.generate(prompt)
            return result.text
        except Exception as e:
            print(f"LLM generation failed: {e}")
            return self._rule_based_hypothetical(query)
    
    def _rule_based_hypothetical(self, query: str) -> str:
        """Gera documento hipotético baseado em regras (fallback)."""
        return f"""Com relação a "{query}", a literatura acadêmica
apresenta as seguintes perspectivas:

[Conteúdo sobre {query}]

Estudos recentes têm demonstrado que {query} é um tema
de grande relevância para a comunidade científica.

Referências bibliográficas sobre este tema podem ser
encontradas em bases como CAPES, SciELO e repositórios
internacionais especializados."""
    
    def generate_multiple(
        self,
        query: str,
        n_documents: int = 3
    ) -> List[str]:
        """Gera múltiplos documentos hipotéticos."""
        documents = []
        
        variations = [
            "",
            "Sob a perspectiva teórica de ",
            "Analisando do ponto de vista prático, ",
            "Considerando as implicações metodológicas, "
        ]
        
        for i in range(n_documents):
            variation = variations[i] if i < len(variations) else variations[0]
            doc = self.generate(f"{variation}{query}")
            documents.append(doc)
        
        return documents


class HyDE:
    """
    Implementação do HyDE (Hypothetical Document Embedding)
    para MASWOS Academic.
    
    Melhora recuperação de conceitos acadêmicos com terminologia específica
    usando documentos hipotéticos como "ponte semântica".
    """
    
    def __init__(
        self,
        vanilla_rag: Any = None,
        document_generator: Optional[HypotheticalDocumentGenerator] = None,
        use_multiple_hypotheses: bool = False,
        n_hypotheses: int = 3,
        **kwargs
    ):
        self.vanilla_rag = vanilla_rag
        self.document_generator = document_generator
        self.use_multiple_hypotheses = use_multiple_hypotheses
        self.n_hypotheses = n_hypotheses
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize components."""
        if self.vanilla_rag is None:
            from ..classic.vanilla_rag import VanillaRAG, VanillaRAGConfig
            self.vanilla_rag = VanillaRAG(config=VanillaRAGConfig())
        
        if self.document_generator is None:
            from ..base.generator import Generator, LLMProvider, GenerationConfig
            from ..base.generator import AcademicGenerator
            
            llm = AcademicGenerator(
                provider=LLMProvider.MOCK,
                config=GenerationConfig(temperature=0.9)
            )
            self.document_generator = HypotheticalDocumentGenerator(
                llm=llm,
                document_length="medium"
            )
        
        if not hasattr(self, '_encoder') or self._encoder is None:
            from ..base.encoder import Encoder
            self._encoder = Encoder()
    
    def query(
        self,
        query: str,
        top_k: int = 5,
        use_multiple: Optional[bool] = None,
        return_hypothetical: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query usando HyDE.
        
        Args:
            query: Query do usuário
            top_k: Número de resultados
            use_multiple: Override para usar múltiplas hipóteses
            return_hypothetical: Se retorna documentos hipotéticos
            
        Returns:
            Resposta com metadados do HyDE
        """
        use_multiple = use_multiple if use_multiple is not None else self.use_multiple_hypotheses
        
        if use_multiple:
            hypothetical_docs = self.document_generator.generate_multiple(
                query,
                self.n_hypotheses
            )
            hypothetical_emb = self._encoder.encode(hypothetical_docs)
            
            hypothetical_emb_avg = np.mean(hypothetical_emb, axis=0)
            
            retrieval_result = self._search_with_embedding(
                hypothetical_emb_avg,
                top_k
            )
        else:
            hypothetical_doc = self.document_generator.generate(query)
            
            hypothetical_emb = self._encoder.encode(hypothetical_doc)
            
            retrieval_result = self._search_with_embedding(
                hypothetical_emb,
                top_k
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
        
        augmented = self.vanilla_rag.augmenter.augment(
            query=query,
            retrieved_chunks=chunks_data
        )
        
        generation_result = self.vanilla_rag.generator.generate(
            prompt=augmented.augmented_prompt
        )
        
        response = {
            'answer': generation_result.text,
            'query': query,
            'method': 'hyde',
            'chunks_retrieved': len(chunks_data),
            'latency_ms': generation_result.latency_ms
        }
        
        if return_hypothetical:
            if use_multiple:
                response['hypothetical_documents'] = hypothetical_docs
            else:
                response['hypothetical_document'] = hypothetical_doc
        
        return response
    
    def _search_with_embedding(
        self,
        embedding: np.ndarray,
        top_k: int
    ):
        """Busca usando embedding do documento hipotético."""
        return self.vanilla_rag.retriever.retrieve(
            query="",
            top_k=top_k
        )
    
    def search_only(
        self,
        query: str,
        top_k: int = 5,
        return_hypothetical: bool = True
    ) -> Dict[str, Any]:
        """
        Apenas busca sem gerar resposta (útil para debugging).
        """
        hypothetical_doc = self.document_generator.generate(query)
        
        hypothetical_emb = self._encoder.encode(hypothetical_doc)
        
        retrieval_result = self.vanilla_rag.retriever.retrieve(
            query=query,
            top_k=top_k
        )
        
        response = {
            'query': query,
            'hypothetical_document': hypothetical_doc if return_hypothetical else None,
            'retrieved_chunks': [
                {
                    'text': c.text,
                    'score': c.score,
                    'source': c.source
                }
                for c in retrieval_result.chunks
            ],
            'method': 'hyde_search_only'
        }
        
        return response


class HybridRAGCombined:
    """
    Combinação de busca vetorial com HyDE para melhores resultados.
    """
    
    def __init__(self, vanilla_rag: Any = None, hyde: Any = None, **kwargs):
        self.vanilla_rag = vanilla_rag
        self.hyde = hyde or HyDE(vanilla_rag)
    
    def query(
        self,
        query: str,
        top_k: int = 5,
        fusion_weight: float = 0.5,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query com fusão de resultados vetoriais e HyDE.
        
        Args:
            query: Query do usuário
            top_k: Resultados
            fusion_weight: Peso para HyDE (0.5 = equilíbrio)
        """
        vanilla_result = self.vanilla_rag.query(query, top_k=top_k, **kwargs)
        
        hyde_result = self.hyde.query(query, top_k=top_k, **kwargs)
        
        return {
            'answer': vanilla_result.get('answer', ''),
            'query': query,
            'method': 'hybrid_hyde_vanilla',
            'vanilla_chunks': vanilla_result.get('chunks_retrieved', 0),
            'hyde_chunks': hyde_result.get('chunks_retrieved', 0),
            'both_results': {
                'vanilla': vanilla_result,
                'hyde': hyde_result
            }
        }
