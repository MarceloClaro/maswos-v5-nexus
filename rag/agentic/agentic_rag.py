"""
Agentic RAG - Implementação MASWOS Academic
Agentes que decidem dinamicamente qual base de dados usar.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import re


class QueryComplexity(Enum):
    """Classificação de complexidade de query."""
    SIMPLE = "simple"           # Fato único
    MEDIUM = "medium"           # Múltiplos fatos
    COMPLEX = "complex"         # Análise multi-dimensional
    COMPARATIVE = "comparative" # Comparação


@dataclass
class Dataset:
    """Representa uma base de dados disponível para o RAG."""
    name: str
    description: str
    locale: str
    vector_store: Any = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentDecision:
    """Decisão do agente sobre qual dataset usar."""
    dataset_name: str
    translated_query: str
    confidence: float
    reasoning: str
    complexity: QueryComplexity


class QueryClassifier:
    """
    Classificador de queries para determinar complexidade e intent.
    """
    
    COMPLEXITY_KEYWORDS = {
        QueryComplexity.SIMPLE: [
            'o que é', 'quem é', 'quando', 'onde', 'qual', 'quantos',
            'defina', 'liste', 'nome'
        ],
        QueryComplexity.MEDIUM: [
            'como', 'por que', 'explique', 'descreva', 'analise',
            'porque', 'diferença'
        ],
        QueryComplexity.COMPLEX: [
            'compare', 'avali', 'impacto', 'efeito', 'relação',
            'correlação', 'influência', 'implicação'
        ],
        QueryComplexity.COMPARATIVE: [
            'comparar', 'versus', 'vs', 'diferença entre',
            'qual é melhor', 'vantagens', 'desvantagens'
        ]
    }
    
    def classify(self, query: str) -> QueryComplexity:
        """Classifica complexidade da query."""
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in self.COMPLEXITY_KEYWORDS[QueryComplexity.COMPARATIVE]):
            return QueryComplexity.COMPARATIVE
        elif any(kw in query_lower for kw in self.COMPLEXITY_KEYWORDS[QueryComplexity.COMPLEX]):
            return QueryComplexity.COMPLEX
        elif any(kw in query_lower for kw in self.COMPLEXITY_KEYWORDS[QueryComplexity.MEDIUM]):
            return QueryComplexity.MEDIUM
        else:
            return QueryComplexity.SIMPLE
    
    def extract_entities(self, query: str) -> List[str]:
        """Extrai entidades mencionadas na query."""
        entities = []
        
        patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',  # Proper nouns
            r'\b(\d{4})\b',  # Years
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query)
            entities.extend(matches)
        
        return entities


class DatasetRouter:
    """
    Roteador que decide qual dataset usar baseado na query.
    """
    
    def __init__(self, datasets: List[Dataset], **kwargs):
        self.datasets = {ds.name: ds for ds in datasets if ds.enabled}
        self.classifier = QueryClassifier()
        
        self._llm = kwargs.get('llm', None)
        self._encoder = None
    
    def _init_encoder(self):
        """Lazy init do encoder."""
        if self._encoder is None:
            from ..base.encoder import Encoder
            self._encoder = Encoder()
    
    def route(self, query: str) -> AgentDecision:
        """
        Decide qual dataset usar para a query.
        
        Args:
            query: Query do usuário
            
        Returns:
            Decisão do agente com dataset recomendado
        """
        complexity = self.classifier.classify(query)
        
        dataset_scores = self._score_datasets(query)
        
        if not dataset_scores:
            return AgentDecision(
                dataset_name="default",
                translated_query=query,
                confidence=0.5,
                reasoning="Nenhum dataset específico encontrado",
                complexity=complexity
            )
        
        best_dataset = max(dataset_scores.items(), key=lambda x: x[1]['score'])
        
        return AgentDecision(
            dataset_name=best_dataset[0],
            translated_query=query,
            confidence=best_dataset[1]['score'],
            reasoning=best_dataset[1]['reasoning'],
            complexity=complexity
        )
    
    def _score_datasets(self, query: str) -> Dict[str, Dict[str, Any]]:
        """Calcula score de relevância para cada dataset."""
        scores = {}
        
        query_lower = query.lower()
        
        for name, dataset in self.datasets.items():
            score = 0
            reasons = []
            
            desc_lower = dataset.description.lower()
            
            query_words = set(query_lower.split())
            desc_words = set(desc_lower.split())
            
            overlap = query_words.intersection(desc_words)
            
            if overlap:
                score += len(overlap) * 0.3
                reasons.append(f"Palavras relevantes: {overlap}")
            
            for keyword in ['direito', 'jurídico', 'lei', 'tribunal']:
                if keyword in query_lower and keyword in desc_lower:
                    score += 0.5
                    reasons.append(f"Match em tema jurídico")
            
            for keyword in ['científico', 'artigo', 'pesquisa', 'estudo']:
                if keyword in query_lower and keyword in desc_lower:
                    score += 0.5
                    reasons.append(f"Match em tema acadêmico")
            
            for keyword in ['estatística', 'dado', 'número', 'IBGE']:
                if keyword in query_lower and keyword in desc_lower:
                    score += 0.5
                    reasons.append(f"Match em dados")
            
            scores[name] = {
                'score': min(score, 1.0),
                'reasoning': '; '.join(reasons) if reasons else 'Sem match específico'
            }
        
        return scores
    
    def route_with_llm(self, query: str) -> AgentDecision:
        """Roteamento assistido por LLM para decisões mais precisas."""
        if not self._llm:
            return self.route(query)
        
        dataset_info = "\n".join([
            f"- {ds.name}: {ds.description} (locale: {ds.locale})"
            for ds in self.datasets.values()
        ])
        
        prompt = f"""Analise a query e escolha o dataset mais apropriado.

Datasets disponíveis:
{dataset_info}

Query: {query}

Escolha apenas um dataset e retorne JSON:
{{
    "dataset_name": "nome do dataset",
    "translated_query": "query traduzida para o idioma do dataset",
    "confidence": 0.0-1.0,
    "reasoning": "explicação breve"
}}

Resposta:"""
        
        try:
            response = self._llm.generate(prompt)
            
            decision_data = json.loads(response.text)
            
            return AgentDecision(
                dataset_name=decision_data.get('dataset_name', 'default'),
                translated_query=decision_data.get('translated_query', query),
                confidence=decision_data.get('confidence', 0.5),
                reasoning=decision_data.get('reasoning', 'LLM decision'),
                complexity=self.classifier.classify(query)
            )
        except Exception as e:
            print(f"LLM routing failed: {e}. Falling back to keyword matching.")
            return self.route(query)


class AgenticRAG:
    """
    Implementação do Agentic RAG para MASWOS Academic.
    
    Usa agentes para decidir dinamicamente qual base de dados usar.
    """
    
    def __init__(
        self,
        datasets: List[Dataset],
        vanilla_rag_template: Any = None,
        use_llm_routing: bool = False,
        **kwargs
    ):
        self.datasets = datasets
        self.use_llm_routing = use_llm_routing
        
        self.router = DatasetRouter(datasets, **kwargs)
        
        self.rag_instances: Dict[str, Any] = {}
        
        self.vanilla_rag_template = vanilla_rag_template
        
        if use_llm_routing:
            from ..base.generator import Generator, LLMProvider
            self.router._llm = Generator(provider=LLMProvider.MOCK)
    
    def _get_rag_for_dataset(self, dataset: Dataset):
        """Obtém ou cria instância de RAG para o dataset."""
        if dataset.name not in self.rag_instances:
            if self.vanilla_rag_template:
                from ..classic.vanilla_rag import VanillaRAG, VanillaRAGConfig
                
                config = VanillaRAGConfig(
                    top_k=5,
                    chunk_size=self.vanilla_rag_template.get('chunk_size', 2000),
                    llm_model=self.vanilla_rag_template.get('llm_model', 'gpt-4')
                )
                
                self.rag_instances[dataset.name] = VanillaRAG(
                    vector_store=dataset.vector_store,
                    config=config
                )
            else:
                raise ValueError("vanilla_rag_template required for creating RAG instances")
        
        return self.rag_instances[dataset.name]
    
    def query(
        self,
        query: str,
        routing_method: str = "auto",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Processa query com roteamento inteligente.
        
        Args:
            query: Query do usuário
            routing_method: 'auto', 'llm', ou 'keyword'
            
        Returns:
            Resposta com metadados de roteamento
        """
        if routing_method == "llm" or (routing_method == "auto" and self.use_llm_routing):
            decision = self.router.route_with_llm(query)
        else:
            decision = self.router.route(query)
        
        dataset = self.datasets.get(decision.dataset_name)
        
        if dataset is None or dataset.vector_store is None:
            return {
                'answer': f"Dataset '{decision.dataset_name}' não disponível.",
                'query': query,
                'decision': {
                    'dataset': decision.dataset_name,
                    'confidence': decision.confidence,
                    'reasoning': decision.reasoning
                },
                'error': 'Dataset not configured'
            }
        
        try:
            rag = self._get_rag_for_dataset(dataset)
            
            result = rag.query(decision.translated_query, **kwargs)
            
            result['routing'] = {
                'dataset': decision.dataset_name,
                'confidence': decision.confidence,
                'reasoning': decision.reasoning,
                'complexity': decision.complexity.value,
                'routing_method': routing_method
            }
            
            return result
            
        except Exception as e:
            return {
                'answer': f"Erro ao processar query: {str(e)}",
                'query': query,
                'decision': {
                    'dataset': decision.dataset_name,
                    'confidence': decision.confidence,
                    'reasoning': decision.reasoning
                },
                'error': str(e)
            }
    
    def add_dataset(self, dataset: Dataset):
        """Adiciona novo dataset ao sistema."""
        self.datasets[dataset.name] = dataset
        self.router.datasets[dataset.name] = dataset
    
    def get_available_datasets(self) -> List[Dict[str, Any]]:
        """Lista datasets disponíveis."""
        return [
            {
                'name': ds.name,
                'description': ds.description,
                'locale': ds.locale,
                'enabled': ds.enabled
            }
            for ds in self.datasets.values()
        ]
