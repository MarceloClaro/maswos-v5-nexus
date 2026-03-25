"""
Generator - LLM generation for RAG
Handles response generation with various LLM providers.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json
import time


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"
    MOCK = "mock"


@dataclass
class GenerationResult:
    """Container for generation results."""
    text: str
    provider: LLMProvider
    model: str
    token_count: int
    latency_ms: float
    metadata: Optional[Dict[str, Any]] = None
    citations: Optional[List[Dict[str, Any]]] = None


@dataclass  
class GenerationConfig:
    """Configuration for text generation."""
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: Optional[List[str]] = None
    system_prompt: Optional[str] = None


class Generator:
    """
    Handles text generation using various LLM providers.
    
    Supports multiple providers with unified interface.
    """
    
    DEFAULT_CONFIG = GenerationConfig()
    
    def __init__(
        self,
        provider: LLMProvider = LLMProvider.OPENAI,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        config: Optional[GenerationConfig] = None,
        **kwargs
    ):
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.config = config or self.DEFAULT_CONFIG
        
        self._client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize the LLM client based on provider."""
        if self.provider == LLMProvider.OPENAI:
            self._init_openai()
        elif self.provider == LLMProvider.ANTHROPIC:
            self._init_anthropic()
        elif self.provider == LLMProvider.GOOGLE:
            self._init_google()
        elif self.provider == LLMProvider.LOCAL:
            self._init_local()
        elif self.provider == LLMProvider.MOCK:
            pass  # No client needed
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            api_key = self.api_key or self._get_env_var('OPENAI_API_KEY')
            self._client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")
    
    def _init_anthropic(self):
        """Initialize Anthropic client."""
        try:
            import anthropic
            api_key = self.api_key or self._get_env_var('ANTHROPIC_API_KEY')
            self._client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("anthropic package required. Install with: pip install anthropic")
    
    def _init_google(self):
        """Initialize Google GenAI client."""
        try:
            from google import genai
            api_key = self.api_key or self._get_env_var('GOOGLE_API_KEY')
            self._client = genai.Client(api_key=api_key)
        except ImportError:
            raise ImportError("google-genai package required. Install with: pip install google-genai")
    
    def _init_local(self):
        """Initialize local LLM client (e.g., Ollama)."""
        self._local_endpoint = self._get_env_var('LOCAL_LLM_ENDPOINT', 'http://localhost:11434')
    
    def _get_env_var(self, name: str, default: Optional[str] = None) -> str:
        """Get environment variable."""
        import os
        return os.environ.get(name, default)
    
    def generate(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate text from prompt.
        
        Args:
            prompt: Input prompt
            config: Optional generation config override
            **kwargs: Additional provider-specific parameters
            
        Returns:
            GenerationResult with generated text and metadata
        """
        config = config or self.config
        start_time = time.time()
        
        if self.provider == LLMProvider.OPENAI:
            return self._generate_openai(prompt, config, start_time)
        elif self.provider == LLMProvider.ANTHROPIC:
            return self._generate_anthropic(prompt, config, start_time)
        elif self.provider == LLMProvider.GOOGLE:
            return self._generate_google(prompt, config, start_time)
        elif self.provider == LLMProvider.LOCAL:
            return self._generate_local(prompt, config, start_time)
        elif self.provider == LLMProvider.MOCK:
            return self._generate_mock(prompt, config, start_time)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _generate_openai(
        self,
        prompt: str,
        config: GenerationConfig,
        start_time: float
    ) -> GenerationResult:
        """Generate using OpenAI API."""
        messages = []
        
        if config.system_prompt:
            messages.append({"role": "system", "content": config.system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p,
            frequency_penalty=config.frequency_penalty,
            presence_penalty=config.presence_penalty,
            stop=config.stop_sequences
        )
        
        latency = (time.time() - start_time) * 1000
        
        return GenerationResult(
            text=response.choices[0].message.content,
            provider=self.provider,
            model=self.model,
            token_count=response.usage.total_tokens,
            latency_ms=latency,
            metadata={
                'finish_reason': response.choices[0].finish_reason
            }
        )
    
    def _generate_anthropic(
        self,
        prompt: str,
        config: GenerationConfig,
        start_time: float
    ) -> GenerationResult:
        """Generate using Anthropic API."""
        system = config.system_prompt if config.system_prompt else ""
        
        response = self._client.messages.create(
            model=self.model,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p
        )
        
        latency = (time.time() - start_time) * 1000
        
        return GenerationResult(
            text=response.content[0].text,
            provider=self.provider,
            model=self.model,
            token_count=response.usage.input_tokens + response.usage.output_tokens,
            latency_ms=latency
        )
    
    def _generate_google(
        self,
        prompt: str,
        config: GenerationConfig,
        start_time: float
    ) -> GenerationResult:
        """Generate using Google GenAI API."""
        response = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                'temperature': config.temperature,
                'max_output_tokens': config.max_tokens,
                'top_p': config.top_p
            }
        )
        
        latency = (time.time() - start_time) * 1000
        
        return GenerationResult(
            text=response.text,
            provider=self.provider,
            model=self.model,
            token_count=0,  # Google doesn't always return this
            latency_ms=latency
        )
    
    def _generate_local(
        self,
        prompt: str,
        config: GenerationConfig,
        start_time: float
    ) -> GenerationResult:
        """Generate using local LLM (Ollama)."""
        import requests
        
        response = requests.post(
            f"{self._local_endpoint}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens
            }
        )
        
        result = response.json()
        
        latency = (time.time() - start_time) * 1000
        
        return GenerationResult(
            text=result.get('response', ''),
            provider=self.provider,
            model=self.model,
            token_count=len(result.get('response', '')) // 4,
            latency_ms=latency
        )
    
    def _generate_mock(
        self,
        prompt: str,
        config: GenerationConfig,
        start_time: float
    ) -> GenerationResult:
        """Mock generation for testing."""
        time.sleep(0.1)  # Simulate latency
        
        return GenerationResult(
            text="Esta é uma resposta mock para testes. O contexto fornecido foi processado corretamente.",
            provider=self.provider,
            model=self.model,
            token_count=20,
            latency_ms=100,
            metadata={'mock': True}
        )
    
    def generate_with_citations(
        self,
        prompt: str,
        context_chunks: List[Dict[str, Any]]
    ) -> GenerationResult:
        """
        Generate with automatic citation extraction.
        
        Attempts to identify citations in generated text.
        """
        result = self.generate(prompt)
        
        citations = self._extract_citations(result.text, context_chunks)
        result.citations = citations
        
        return result
    
    def _extract_citations(
        self,
        text: str,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract citations from generated text."""
        import re
        
        citation_pattern = r'\[(?:Fonte|source):\s*([^\]]+)\]'
        matches = re.findall(citation_pattern, text)
        
        citations = []
        for source_name in matches:
            for chunk in chunks:
                if chunk.get('source') == source_name:
                    citations.append({
                        'source': source_name,
                        'text': chunk.get('text', '')[:200]
                    })
                    break
        
        return citations


class AcademicGenerator(Generator):
    """
    Specialized generator for academic content.
    Configured for scholarly writing and citations.
    """
    
    ACADEMIC_SYSTEM_PROMPT = """Você é um assistente acadêmico especializado em pesquisa científica.
- Escreva de forma formal e objetiva
- Use referências bibliográficas no formato (Autor, Ano)
- Mantenha rigor científico
- Evite linguagem coloquial
- Apresente evidências e fundamentação"""

    def __init__(
        self,
        provider: LLMProvider = LLMProvider.OPENAI,
        model: str = "gpt-4",
        **kwargs
    ):
        config = GenerationConfig(
            temperature=0.3,  # Lower for factual accuracy
            max_tokens=4000,
            system_prompt=self.ACADEMIC_SYSTEM_PROMPT
        )
        
        super().__init__(provider, model, config=config, **kwargs)
    
    def generate_academic(
        self,
        prompt: str,
        context_chunks: List[Dict[str, Any]],
        citation_style: str = "abnt"
    ) -> GenerationResult:
        """Generate academic content with proper citations."""
        result = self.generate_with_citations(prompt, context_chunks)
        
        result.metadata = result.metadata or {}
        result.metadata['citation_style'] = citation_style
        result.metadata['academic_mode'] = True
        
        return result
