"""
RAG com Memória - Implementação MASWOS Academic
Usa Redis para armazenar histórico de conversas.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import json
import time


class MemoryStore:
    """
    Armazenamento de memória usando Redis ou fallback em memória.
    
    Permite manter contexto entre múltiplas interações.
    """
    
    def __init__(
        self,
        use_redis: bool = True,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        expiration_seconds: int = 86400,  # 24 hours
        max_history_turns: int = 10
    ):
        self.use_redis = use_redis
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.expiration_seconds = expiration_seconds
        self.max_history_turns = max_history_turns
        
        self._client = None
        self._memory = {}  # Fallback in-memory
        
        if use_redis:
            self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis connection."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                decode_responses=True
            )
            self._client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}. Using in-memory fallback.")
            self.use_redis = False
    
    def _get_key(self, session_id: str) -> str:
        """Generate Redis key for session."""
        return f"rag:memory:{session_id}"
    
    def add_turn(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> bool:
        """
        Adiciona um turno à memória da sessão.
        
        Args:
            session_id: Identificador único da sessão
            role: 'user' ou 'assistant'
            content: Conteúdo da mensagem
            
        Returns:
            True se bem-sucedido
        """
        key = self._get_key(session_id)
        
        history = self.get_history(session_id)
        
        history.append({
            'role': role,
            'content': content,
            'timestamp': time.time()
        })
        
        if len(history) > self.max_history_turns:
            history = history[-self.max_history_turns:]
        
        if self.use_redis and self._client:
            try:
                self._client.setex(
                    key,
                    self.expiration_seconds,
                    json.dumps(history)
                )
                return True
            except Exception:
                pass
        
        self._memory[key] = history
        return True
    
    def get_history(
        self,
        session_id: str,
        max_turns: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Recupera histórico da sessão.
        
        Args:
            session_id: Identificador da sessão
            max_turns: Máximo de turnos a retornar
            
        Returns:
            Lista de mensagens no formato [{'role': str, 'content': str}]
        """
        key = self._get_key(session_id)
        max_turns = max_turns or self.max_history_turns
        
        if self.use_redis and self._client:
            try:
                data = self._client.get(key)
                if data:
                    history = json.loads(data)
                    return history[-max_turns:]
            except Exception:
                pass
        
        history = self._memory.get(key, [])
        return history[-max_turns:]
    
    def clear_session(self, session_id: str) -> bool:
        """Limpa histórico de uma sessão."""
        key = self._get_key(session_id)
        
        if self.use_redis and self._client:
            try:
                self._client.delete(key)
                return True
            except Exception:
                pass
        
        if key in self._memory:
            del self._memory[key]
        return True
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Retorna informações sobre a sessão."""
        history = self.get_history(session_id, max_turns=100)
        
        return {
            'session_id': session_id,
            'turns': len(history),
            'oldest_timestamp': history[0].get('timestamp') if history else None,
            'newest_timestamp': history[-1].get('timestamp') if history else None,
            'storage_type': 'redis' if self.use_redis else 'memory'
        }


class MemoryRAG:
    """
    Implementação do RAG com Memória para MASWOS Academic.
    
    Mantém contexto entre interações usando Redis ou armazenamento em memória.
    Útil para sessões de revisão extensas de artigos.
    """
    
    def __init__(
        self,
        vanilla_rag: Any = None,
        memory_store: Optional[MemoryStore] = None,
        include_history_turns: int = 5,
        **kwargs
    ):
        self.vanilla_rag = vanilla_rag
        self.memory_store = memory_store or MemoryStore()
        self.include_history_turns = include_history_turns
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize components if not provided."""
        from .vanilla_rag import VanillaRAG, VanillaRAGConfig
        
        if self.vanilla_rag is None:
            config = VanillaRAGConfig(**kwargs)
            self.vanilla_rag = VanillaRAG(config=config)
    
    def query(
        self,
        query: str,
        session_id: str = "default",
        include_history: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Processa query com memória de sessão.
        
        Args:
            query: Query do usuário
            session_id: Identificador da sessão
            include_history: Se deve incluir histórico no contexto
            
        Returns:
            Resposta com metadados
        """
        if include_history:
            history = self.memory_store.get_history(
                session_id,
                max_turns=self.include_history_turns
            )
            
            history_text = self._format_history(history)
            
            full_query = f"{history_text}\n\nPergunta atual: {query}"
        else:
            full_query = query
        
        result = self.vanilla_rag.query(full_query, **kwargs)
        
        self.memory_store.add_turn(session_id, "user", query)
        self.memory_store.add_turn(session_id, "assistant", result['answer'])
        
        result['session_id'] = session_id
        result['history_included'] = include_history
        
        if include_history:
            result['history_turns'] = len(history)
        
        return result
    
    def _format_history(self, history: List[Dict[str, str]]) -> str:
        """Formata histórico para inclusão no prompt."""
        if not history:
            return ""
        
        formatted = ["Histórico da conversa:"]
        
        for turn in history:
            role = turn.get('role', 'user').upper()
            content = turn.get('content', '')
            formatted.append(f"\n{role}: {content[:200]}...")
        
        return "\n".join(formatted)
    
    def clear_session(self, session_id: str) -> bool:
        """Limpa memória de uma sessão."""
        return self.memory_store.clear_session(session_id)
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Retorna informações da sessão."""
        return self.memory_store.get_session_info(session_id)
    
    def list_active_sessions(self) -> List[str]:
        """Lista sessões ativas (apenas para modo em memória)."""
        if self.memory_store.use_redis:
            try:
                keys = self.memory_store._client.keys("rag:memory:*")
                return [k.replace("rag:memory:", "") for k in keys]
            except Exception:
                return []
        else:
            return list(self.memory_store._memory.keys())


class ConversationManager:
    """
    Gerenciador de múltiplas conversas simultâneas.
    
    Permite criar e gerenciar múltiplas sessões de RAG com memória.
    """
    
    def __init__(self, **kwargs):
        self.sessions: Dict[str, MemoryRAG] = {}
        self.default_kwargs = kwargs
    
    def get_or_create_session(
        self,
        session_id: str,
        **kwargs
    ) -> MemoryRAG:
        """Obtém ou cria uma sessão."""
        if session_id not in self.sessions:
            session_kwargs = {**self.default_kwargs, **kwargs}
            self.sessions[session_id] = MemoryRAG(**session_kwargs)
        
        return self.sessions[session_id]
    
    def query(
        self,
        query: str,
        session_id: str = "default",
        **kwargs
    ) -> Dict[str, Any]:
        """Query em sessão específica."""
        session = self.get_or_create_session(session_id)
        return session.query(query, session_id=session_id, **kwargs)
    
    def close_session(self, session_id: str) -> bool:
        """Fecha e remove uma sessão."""
        if session_id in self.sessions:
            self.sessions[session_id].clear_session(session_id)
            del self.sessions[session_id]
            return True
        return False
    
    def list_sessions(self) -> List[str]:
        """Lista todas as sessões ativas."""
        return list(self.sessions.keys())
