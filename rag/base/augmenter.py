"""
Augmenter - Prompt augmentation for RAG
Combines query with retrieved context to create prompts for generation.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re


@dataclass
class AugmentedPrompt:
    """Container for augmented prompt."""
    original_query: str
    augmented_prompt: str
    context_chunks: List[Dict[str, Any]]
    token_count: int
    metadata: Optional[Dict[str, Any]] = None


class Augmenter:
    """
    Augments queries with retrieved context for LLM generation.
    
    Handles prompt construction with various templates and strategies.
    """
    
    DEFAULT_TEMPLATE = """Responda à pergunta do usuário usando apenas as informações fornecidas no contexto abaixo.

Contexto:
{context}

Pergunta: {query}

Instruções:
- Use apenas informações do contexto fornecido
- Se o contexto não contém informação suficiente, responda: "Não tenho informação suficiente no contexto fornecido."
- Forneça respostas detalhadas e bem fundamentadas
- Mantenha objetividade e clareza
- Cite as fontes quando relevante

Resposta:"""

    ACADEMIC_TEMPLATE = """Você é um assistente acadêmico especializado em pesquisa científica.
Sua tarefa é responder à pergunta abaixo utilizando EXCLUSIVAMENTE as informações do contexto acadêmico fornecido.

Contexto Acadêmico:
{context}

Pergunta de Pesquisa: {query}

Diretrizes:
1. Utilize apenas informações presentes no contexto
2. Quando relevante, inclua referências bibliográficas no formato (Autor, Ano)
3. Mantenha rigor científico na resposta
4. Distinja entre fatos apresentados e inferências
5. Se a informação não estiver disponível, indique claramente

Resposta Acadêmica:"""

    CONCISE_TEMPLATE = """Pergunta: {query}

Contexto relevante:
{context}

Resposta direta:"""

    def __init__(
        self,
        template: Optional[str] = None,
        max_context_length: int = 8000,
        include_sources: bool = True,
        source_format: str = "footnote"
    ):
        self.template = template or self.DEFAULT_TEMPLATE
        self.max_context_length = max_context_length
        self.include_sources = include_sources
        self.source_format = source_format
    
    def augment(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        template: Optional[str] = None,
        **kwargs
    ) -> AugmentedPrompt:
        """
        Create augmented prompt from query and retrieved chunks.
        
        Args:
            query: Original user query
            retrieved_chunks: List of retrieved document chunks
            template: Optional custom template override
            
        Returns:
            AugmentedPrompt with formatted prompt and metadata
        """
        template = template or self.template
        
        context_parts = []
        total_length = 0
        
        for chunk in retrieved_chunks:
            text = chunk.get('text', '')
            source = chunk.get('source', 'Unknown')
            
            if self.include_sources:
                if self.source_format == "footnote":
                    formatted_text = f"{text}\n[Fonte: {source}]"
                elif self.source_format == "inline":
                    formatted_text = f"({source}) {text}"
                else:
                    formatted_text = text
            else:
                formatted_text = text
            
            if total_length + len(formatted_text) <= self.max_context_length:
                context_parts.append(formatted_text)
                total_length += len(formatted_text)
            else:
                break
        
        context = "\n\n---\n\n".join(context_parts)
        
        augmented_prompt = template.format(
            query=query,
            context=context
        )
        
        return AugmentedPrompt(
            original_query=query,
            augmented_prompt=augmented_prompt,
            context_chunks=retrieved_chunks,
            token_count=self._estimate_tokens(augmented_prompt),
            metadata={
                'template_used': template[:50] + '...',
                'chunks_included': len(context_parts),
                'total_context_length': total_length,
                'source_format': self.source_format
            }
        )
    
    def augment_with_history(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        conversation_history: List[Dict[str, str]],
        **kwargs
    ) -> AugmentedPrompt:
        """
        Create augmented prompt including conversation history.
        
        Useful for RAG with memory.
        """
        history_text = self._format_conversation_history(conversation_history)
        
        template = kwargs.get('template', self.template)
        
        context_parts = [history_text] if history_text else []
        
        for chunk in retrieved_chunks:
            text = chunk.get('text', '')
            source = chunk.get('source', 'Unknown')
            
            if self.include_sources:
                formatted_text = f"{text}\n[Fonte: {source}]"
            else:
                formatted_text = text
            
            context_parts.append(formatted_text)
        
        context = "\n\n---\n\n".join(context_parts)
        
        full_context = context[:self.max_context_length]
        
        augmented_prompt = template.format(
            query=query,
            context=full_context
        )
        
        return AugmentedPrompt(
            original_query=query,
            augmented_prompt=augmented_prompt,
            context_chunks=retrieved_chunks,
            token_count=self._estimate_tokens(augmented_prompt),
            metadata={
                'includes_history': True,
                'history_turns': len(conversation_history)
            }
        )
    
    def _format_conversation_history(
        self,
        history: List[Dict[str, str]]
    ) -> str:
        """Format conversation history for inclusion in prompt."""
        if not history:
            return ""
        
        formatted = ["Histórico da Conversa:"]
        
        for turn in history[-5:]:  # Last 5 turns
            role = turn.get('role', 'user')
            content = turn.get('content', '')
            formatted.append(f"{role.upper()}: {content}")
        
        return "\n".join(formatted)
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (avg 4 chars per token)."""
        return len(text) // 4
    
    def set_template(self, template: str):
        """Change the active template."""
        self.template = template
    
    def get_available_templates(self) -> Dict[str, str]:
        """Return available prompt templates."""
        return {
            'default': self.DEFAULT_TEMPLATE,
            'academic': self.ACADEMIC_TEMPLATE,
            'concise': self.CONCISE_TEMPLATE
        }


class AdaptiveAugmenter(Augmenter):
    """
    Augmenter that adapts template based on query type.
    """
    
    TEMPLATES = {
        'factual': """Pergunta factual: {query}

Informações relevantes:
{context}

Resposta (fato):""",
        
        'analytical': """Pergunta analítica: {query}

Contexto para análise:
{context}

Análise detalhada:""",
        
        'comparative': """Pergunta comparativa: {query}

Contexto comparativo:
{context}

Comparação:""",
        
        'explanatory': """Explicação requerida: {query}

Contexto explicativo:
{context}

Explicação:"""
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._query_classifier = None
    
    def _classify_query(self, query: str) -> str:
        """Classify query type for template selection."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['o que é', 'quem é', 'quando', 'onde', 'qual']):
            return 'factual'
        elif any(word in query_lower for word in ['por que', 'como', 'explique', 'analise']):
            return 'analytical'
        elif any(word in query_lower for word in ['diferença', 'comparar', 'versus', 'vs']):
            return 'comparative'
        elif any(word in query_lower for word in ['defina', 'significado', 'o que significa']):
            return 'explanatory'
        else:
            return 'factual'
    
    def augment(self, query: str, retrieved_chunks: List[Dict[str, Any]], **kwargs) -> AugmentedPrompt:
        """Augment with query-type-adaptive template."""
        query_type = self._classify_query(query)
        template = self.TEMPLATES.get(query_type, self.DEFAULT_TEMPLATE)
        
        return super().augment(query, retrieved_chunks, template=template, **kwargs)
