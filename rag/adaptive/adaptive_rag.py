"""
Adaptive RAG - Implementação MASWOS Academic
Adapta estratégia conforme complexidade da pergunta.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import re


class RetrievalStrategy(Enum):
    """Estratégias de recuperação."""
    NO_RETRIEVAL = "no_retrieval"           # Conhecimento geral
    SINGLE_STEP = "single_step"             # Fato simples
    MULTI_STEP = "multi_step"               # Análise complexa


@dataclass
class QueryAnalysis:
    """Resultado da análise de query."""
    complexity: str
    strategy: RetrievalStrategy
    requires_citations: bool
    is_comparative: bool
    is_temporal: bool
    keywords: List[str]
    sub_queries: List[str]


class QueryAnalyzer:
    """
    Analisa queries para determinar estratégia de recuperação.
    """
    
    COMPLEXITY_PATTERNS = {
        'simple': [
            r'^o que é\b',
            r'^quem é\b', 
            r'^qual a capital',
            r'^qual o nome',
            r'^quando ocorreu',
            r'^onde fica',
        ],
        'medium': [
            r'^como\b',
            r'^por que\b',
            r'^explique',
            r'^descreva',
            r'^qual a diferença',
        ],
        'complex': [
            r'^compare',
            r'^analise',
            r'^avali',
            r'^qual o impacto',
            r'^quais os efeitos',
            r'^qual a relação',
        ]
    }
    
    def analyze(self, query: str) -> QueryAnalysis:
        """Analisa query e determina estratégia."""
        query_lower = query.lower()
        
        complexity = self._determine_complexity(query_lower)
        
        strategy = self._determine_strategy(complexity, query_lower)
        
        requires_citations = any(word in query_lower for word in [
            'segundo', 'conforme', 'de acordo', 'segundo', 'cite'
        ])
        
        is_comparative = any(word in query_lower for word in [
            'comparar', 'diferença', 'versus', 'vs', 'diferente'
        ])
        
        is_temporal = any(word in query_lower for word in [
            'ano', 'período', 'década', 'quando', 'evolução', 'tempo'
        ])
        
        keywords = self._extract_keywords(query_lower)
        
        sub_queries = self._generate_sub_queries(query, complexity)
        
        return QueryAnalysis(
            complexity=complexity,
            strategy=strategy,
            requires_citations=requires_citations,
            is_comparative=is_comparative,
            is_temporal=is_temporal,
            keywords=keywords,
            sub_queries=sub_queries
        )
    
    def _determine_complexity(self, query: str) -> str:
        """Determina complexidade da query."""
        for complexity, patterns in self.COMPLEXITY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return complexity
        return 'medium'
    
    def _determine_strategy(self, complexity: str, query: str) -> RetrievalStrategy:
        """Determina estratégia de recuperação."""
        general_knowledge = [
            'como você está',
            'quem é você',
            'que dia é hoje',
            'qual o seu nome'
        ]
        
        if any(gk in query for gk in general_knowledge):
            return RetrievalStrategy.NO_RETRIEVAL
        
        if complexity == 'simple':
            return RetrievalStrategy.SINGLE_STEP
        else:
            return RetrievalStrategy.MULTI_STEP
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extrai palavras-chave."""
        stopwords = {
            'o', 'a', 'de', 'da', 'do', 'em', 'um', 'uma', 'para',
            'com', 'não', 'é', 'que', 'os', 'as', 'se', 'na', 'no',
            'mais', 'como', 'por', 'são', 'dos', 'das', 'à', 'entre'
        }
        
        words = query.split()
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        
        return keywords[:5]
    
    def _generate_sub_queries(self, query: str, complexity: str) -> List[str]:
        """Gera sub-queries para análise multi-etapa."""
        if complexity != 'complex':
            return []
        
        sub_queries = []
        
        if 'relação' in query.lower() or 'impacto' in query.lower():
            parts = query.lower().split('relação')
            if len(parts) > 1:
                sub_queries.append(f"O que é{parts[1][:50]}")
                sub_queries.append(f"Impacto{parts[1][:50]}")
        
        return sub_queries[:3]


class AdaptiveRAG:
    """
    Implementação do Adaptive RAG para MASWOS Academic.
    
    Adapta estratégia conforme complexidade da pergunta.
    """
    
    def __init__(
        self,
        vanilla_rag: Any = None,
        no_retrieval_llm: Any = None,
        **kwargs
    ):
        self.vanilla_rag = vanilla_rag
        self.analyzer = QueryAnalyzer()
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize components if needed."""
        if self.vanilla_rag is None:
            from ..classic.vanilla_rag import VanillaRAG, VanillaRAGConfig
            self.vanilla_rag = VanillaRAG(config=VanillaRAGConfig())
        
        if not hasattr(self, 'no_retrieval_llm') or self.no_retrieval_llm is None:
            from ..base.generator import Generator, LLMProvider, GenerationConfig
            self.no_retrieval_llm = Generator(
                provider=LLMProvider.MOCK,
                config=GenerationConfig(temperature=0.7)
            )
    
    def query(
        self,
        query: str,
        override_strategy: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query com estratégia adaptativa.
        
        Args:
            query: Query do usuário
            override_strategy: Forçar estratégia específica
        """
        analysis = self.analyzer.analyze(query)
        
        if override_strategy:
            try:
                strategy = RetrievalStrategy(override_strategy)
            except ValueError:
                strategy = analysis.strategy
        else:
            strategy = analysis.strategy
        
        if strategy == RetrievalStrategy.NO_RETRIEVAL:
            return self._handle_no_retrieval(query, analysis)
        elif strategy == RetrievalStrategy.SINGLE_STEP:
            return self._handle_single_step(query, analysis, **kwargs)
        else:
            return self._handle_multi_step(query, analysis, **kwargs)
    
    def _handle_no_retrieval(
        self,
        query: str,
        analysis: QueryAnalysis
    ) -> Dict[str, Any]:
        """Handle queries that don't need retrieval."""
        prompt = f"""
Você é um assistente acadêmico. Responda à seguinte pergunta
de forma clara e objetiva:

{query}

Resposta:
"""
        result = self.no_retrieval_llm.generate(prompt)
        
        return {
            'answer': result.text,
            'query': query,
            'strategy_used': 'no_retrieval',
            'analysis': {
                'complexity': analysis.complexity,
                'requires_citations': analysis.requires_citations
            },
            'latency_ms': result.latency_ms
        }
    
    def _handle_single_step(
        self,
        query: str,
        analysis: QueryAnalysis,
        **kwargs
    ) -> Dict[str, Any]:
        """Handle simple queries with single retrieval."""
        result = self.vanilla_rag.query(query, **kwargs)
        
        result['strategy_used'] = 'single_step'
        result['analysis'] = {
            'complexity': analysis.complexity,
            'keywords': analysis.keywords,
            'requires_citations': analysis.requires_citations
        }
        
        return result
    
    def _handle_multi_step(
        self,
        query: str,
        analysis: QueryAnalysis,
        **kwargs
    ) -> Dict[str, Any]:
        """Handle complex queries with iterative retrieval."""
        all_chunks = []
        
        if analysis.sub_queries:
            for sub_q in analysis.sub_queries:
                sub_result = self.vanilla_rag.retriever.retrieve(
                    query=sub_q,
                    top_k=3
                )
                all_chunks.extend([
                    {
                        'text': c.text,
                        'score': c.score,
                        'source': c.source,
                        'sub_query': sub_q
                    }
                    for c in sub_result.chunks
                ])
        
        main_result = self.vanilla_rag.retriever.retrieve(
            query=query,
            top_k=kwargs.get('top_k', 5)
        )
        
        all_chunks.extend([
            {
                'text': c.text,
                'score': c.score,
                'source': c.source,
                'sub_query': query
            }
            for c in main_result.chunks
        ])
        
        unique_chunks = self._deduplicate_chunks(all_chunks)
        
        augmented = self.vanilla_rag.augmenter.augment(
            query=query,
            retrieved_chunks=unique_chunks[:kwargs.get('top_k', 5)]
        )
        
        generation_result = self.vanilla_rag.generator.generate(
            prompt=augmented.augmented_prompt
        )
        
        return {
            'answer': generation_result.text,
            'query': query,
            'strategy_used': 'multi_step',
            'sub_queries_executed': len(analysis.sub_queries),
            'total_chunks_retrieved': len(unique_chunks),
            'analysis': {
                'complexity': analysis.complexity,
                'is_comparative': analysis.is_comparative,
                'is_temporal': analysis.is_temporal,
                'requires_citations': analysis.requires_citations,
                'sub_queries': analysis.sub_queries
            },
            'latency_ms': generation_result.latency_ms
        }
    
    def _deduplicate_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """Remove chunks duplicados."""
        seen = set()
        unique = []
        
        for chunk in chunks:
            text_hash = hash(chunk.get('text', '')[:100])
            if text_hash not in seen:
                seen.add(text_hash)
                unique.append(chunk)
        
        return unique
    
    def get_query_analysis(self, query: str) -> QueryAnalysis:
        """Retorna análise de uma query sem executar."""
        return self.analyzer.analyze(query)
