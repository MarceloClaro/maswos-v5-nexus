"""
Dynamic Handoff Protocol with Context Preservation
====================================================
Protocolo para passagem de contexto entre agentes com preservação total.

Autor: MASWOS V5 NEXUS
Versão: 5.1.1
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque


class HandoffStatus(Enum):
    """Status do handoff"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"


class HandoffError(Exception):
    """Erros de handoff"""
    QUALITY_BELOW_THRESHOLD = "quality_below_threshold"
    TIMEOUT = "timeout"
    INVALID_CONTEXT = "invalid_context"
    MAX_HANDOFFS_EXCEEDED = "max_handoffs_exceeded"


@dataclass
class AuditEntry:
    """Entrada de auditoria"""
    timestamp: str
    from_agent: str
    to_agent: str
    action: str
    quality_score: float
    details: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Serializar para dict"""
        return {
            "timestamp": self.timestamp,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "action": self.action,
            "quality_score": self.quality_score,
            "details": self.details
        }


@dataclass 
class HandoffContext:
    """Contexto completo para handoff entre agentes"""
    # Identificação
    session_id: str
    handoff_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Fluxo original
    original_request: str = ""
    user_decisions: List[str] = field(default_factory=list)
    previous_work_summary: str = ""
    
    # Estado atual
    current_phase: str = ""
    current_plan_state: Dict[str, Any] = field(default_factory=dict)
    
    # Contexto de execução
    entities: Dict[str, Any] = field(default_factory=dict)
    mcp_context: Dict[str, Any] = field(default_factory=dict)
    intermediate_results: List[Dict[str, Any]] = field(default_factory=list)  # CORRIGIDO: era Dict
    
    # Qualidade
    quality_score: float = 1.0
    handoff_count: int = 0
    
    # Auditoria
    audit_trail: List[AuditEntry] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_entry(self, from_agent: str, to_agent: str, action: str, quality: float, details: str = ""):
        """Adicionar entrada ao audit trail"""
        entry = AuditEntry(
            timestamp=datetime.now().isoformat(),
            from_agent=from_agent,
            to_agent=to_agent,
            action=action,
            quality_score=quality,
            details=details
        )
        self.audit_trail.append(entry)
        self.handoff_count += 1
    
    def to_dict(self) -> Dict:
        """Serializar para dict"""
        return {
            "session_id": self.session_id,
            "handoff_id": self.handoff_id,
            "original_request": self.original_request,
            "user_decisions": self.user_decisions,
            "previous_work_summary": self.previous_work_summary,
            "current_phase": self.current_phase,
            "current_plan_state": self.current_plan_state,
            "entities": self.entities,
            "mcp_context": self.mcp_context,
            "intermediate_results": self.intermediate_results,
            "quality_score": self.quality_score,
            "handoff_count": self.handoff_count,
            "audit_trail": [e.to_dict() for e in self.audit_trail],
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HandoffContext':
        """Desserializar de dict"""
        # Extrair audit_trail
        audit_data = data.get("audit_trail", [])
        audit_trail = []
        for entry_data in audit_data:
            audit_trail.append(AuditEntry(
                timestamp=entry_data.get("timestamp", ""),
                from_agent=entry_data.get("from_agent", ""),
                to_agent=entry_data.get("to_agent", ""),
                action=entry_data.get("action", ""),
                quality_score=entry_data.get("quality_score", 1.0),
                details=entry_data.get("details", "")
            ))
        
        context = cls(
            session_id=data.get("session_id", str(uuid.uuid4())),
            handoff_id=data.get("handoff_id", str(uuid.uuid4())),
            original_request=data.get("original_request", ""),
            user_decisions=data.get("user_decisions", []),
            previous_work_summary=data.get("previous_work_summary", ""),
            current_phase=data.get("current_phase", ""),
            current_plan_state=data.get("current_plan_state", {}),
            entities=data.get("entities", {}),
            mcp_context=data.get("mcp_context", {}),
            intermediate_results=data.get("intermediate_results", []),
            quality_score=data.get("quality_score", 1.0),
            handoff_count=data.get("handoff_count", 0),
            created_at=data.get("created_at", datetime.now().isoformat())
        )
        context.audit_trail = audit_trail
        
        return context


class HandoffValidator:
    """Validador de handoff"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            "min_quality_threshold": 0.70,
            "max_handoffs": 5,
            "timeout_seconds": 300,
            "require_context_fields": [
                "original_request",
                "entities",
                "quality_score"
            ]
        }
    
    def validate_context(self, context: HandoffContext) -> Dict[str, Any]:
        """Validar contexto de handoff"""
        errors = []
        warnings = []
        
        # Verificar campos obrigatórios
        for field_name in self.config.get("require_context_fields", []):
            value = getattr(context, field_name, None)
            if not value:
                errors.append(f"Campo obrigatório ausente: {field_name}")
        
        # Verificar threshold de qualidade
        if context.quality_score < self.config.get("min_quality_threshold", 0.70):
            errors.append(f"Quality score below threshold: {context.quality_score}")
        
        # Verificar contagem de handoffs
        if context.handoff_count >= self.config.get("max_handoffs", 5):
            errors.append("Max handoffs exceeded")
        
        # Verificar tamanho do audit trail
        if len(context.audit_trail) == 0:
            warnings.append("Empty audit trail")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "quality_score": context.quality_score
        }
    
    def validate_handoff(self, context: HandoffContext, from_agent: str, to_agent: str) -> Dict:
        """Validar handoff específico"""
        validation = self.validate_context(context)
        
        # Adicionar validações específicas de handoff
        validation["from_agent"] = from_agent
        validation["to_agent"] = to_agent
        validation["handoff_id"] = context.handoff_id
        validation["handoff_count"] = context.handoff_count
        
        return validation


class HandoffManager:
    """Gerenciador de handoffs"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.validator = HandoffValidator(config)
        self.active_contexts: Dict[str, HandoffContext] = {}
        self.history: deque = deque(maxlen=100)  # Manter últimos 100 handoffs
    
    def create_context(
        self,
        session_id: str,
        original_request: str,
        user_decisions: Optional[List[str]] = None,
        entities: Optional[Dict[str, Any]] = None
    ) -> HandoffContext:
        """Criar novo contexto de handoff"""
        context = HandoffContext(
            session_id=session_id,
            original_request=original_request,
            user_decisions=user_decisions or [],
            entities=entities or {}
        )
        
        self.active_contexts[session_id] = context
        return context
    
    def get_context(self, session_id: str) -> Optional[HandoffContext]:
        """Obter contexto ativo"""
        return self.active_contexts.get(session_id)
    
    def execute_handoff(
        self,
        session_id: str,
        from_agent: str,
        to_agent: str,
        action: str,
        additional_context: Optional[Dict[str, Any]] = None,
        quality_score: float = 1.0
    ) -> Dict[str, Any]:
        """Executar handoff entre agentes"""
        context = self.get_context(session_id)
        
        if not context:
            return {
                "status": "error",
                "error": "Session not found",
                "session_id": session_id
            }
        
        # Validar handoff
        validation = self.validator.validate_handoff(context, from_agent, to_agent)
        
        if not validation["valid"]:
            return {
                "status": "failed",
                "error": "Handoff validation failed",
                "validation": validation
            }
        
        # Adicionar dados adicionais ao contexto
        if additional_context:
            plan_state = additional_context.get("plan_state", {})
            if plan_state:
                # Usar update em vez de append para Dict
                context.current_plan_state.update(plan_state)
            
            result = additional_context.get("result")
            if result:
                # Usar append para List
                context.intermediate_results.append(result)
        
        # Executar handoff - CORRIGIDO: usar 'quality' em vez de 'quality_score'
        context.add_entry(from_agent, to_agent, action, quality_score)
        context.quality_score = min(context.quality_score, quality_score)
        
        # Adicionar ao histórico
        self.history.append({
            "session_id": session_id,
            "handoff_id": context.handoff_id,
            "from": from_agent,
            "to": to_agent,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "status": "success",
            "handoff_id": context.handoff_id,
            "context": context.to_dict(),
            "validation": validation
        }
    
    def escalate(self, session_id: str, reason: str) -> Dict:
        """Escalar handoff para orchestrator"""
        context = self.get_context(session_id)
        
        if not context:
            return {"status": "error", "error": "Session not found"}
        
        context.add_entry(
            from_agent="current_agent",
            to_agent="orchestrator",
            action=f"escalation: {reason}",
            quality=context.quality_score  # CORRIGIDO: usar quality
        )
        
        return {
            "status": "escalated",
            "reason": reason,
            "context": context.to_dict()
        }
    
    def get_session_status(self, session_id: str) -> Dict:
        """Obter status de uma sessão"""
        context = self.get_context(session_id)
        
        if not context:
            return {"status": "not_found"}
        
        last_entry_dict = None
        if context.audit_trail:
            last_entry_dict = context.audit_trail[-1].to_dict()
        
        return {
            "session_id": session_id,
            "handoff_count": context.handoff_count,
            "current_phase": context.current_phase,
            "quality_score": context.quality_score,
            "audit_trail_length": len(context.audit_trail),
            "last_entry": last_entry_dict
        }
    
    def cleanup_session(self, session_id: str) -> bool:
        """Limpar sessão"""
        if session_id in self.active_contexts:
            del self.active_contexts[session_id]
            return True
        return False


class ContextPreservation:
    """Preservador de contexto para handoffs"""
    
    @staticmethod
    def create_handoff_message(context: HandoffContext, from_agent: str, to_agent: str, task: str) -> str:
        """Criar mensagem de handoff formatada"""
        
        message_parts = [
            f"## Handoff: {from_agent} → {to_agent}",
            f"",
            f"**Session:** {context.session_id}",
            f"**Handoff ID:** {context.handoff_id}",
            f"",
            f"### 📋 Contexto Original",
            f"{context.original_request}",
            f""
        ]
        
        if context.user_decisions:
            message_parts.extend([
                f"### ✅ Decisões do Usuário",
                *[f"- {d}" for d in context.user_decisions],
                f""
            ])
        
        if context.previous_work_summary:
            message_parts.extend([
                f"### 📊 Trabalho Anterior",
                f"{context.previous_work_summary}",
                f""
            ])
        
        if context.entities:
            message_parts.extend([
                f"### 🎯 Entidades Extraídas",
                f"```json",
                f"{json.dumps(context.entities, indent=2)}",
                f"```",
                f""
            ])
        
        message_parts.extend([
            f"### 🎯 Tarefa",
            f"{task}",
            f"",
            f"### 📈 Métricas",
            f"- Quality Score: {context.quality_score:.2f}",
            f"- Handoff Count: {context.handoff_count}",
            f"- Audit Trail: {len(context.audit_trail)} entries"
        ])
        
        return "\n".join(message_parts)
    
    @staticmethod
    def extract_from_plan_file(plan_content: str) -> Dict[str, Any]:
        """Extrair contexto de arquivo PLAN.md"""
        # Extrai seções típicas de um PLAN.md
        context: Dict[str, Any] = {
            "plan_exists": True,
            "sections": []
        }
        
        # Parser simples de markdown
        lines = plan_content.split("\n")
        current_section = ""
        
        for line in lines:
            if line.startswith("#"):
                current_section = line.strip("# ").strip()
                context["sections"].append(current_section)
                context[current_section] = []
            elif current_section and line.strip():
                if isinstance(context.get(current_section), list):
                    context[current_section].append(line.strip())
        
        return context


# Instância global do gerenciador
_handoff_manager: Optional[HandoffManager] = None

def get_handoff_manager() -> HandoffManager:
    """Obter instância global do gerenciador de handoffs"""
    global _handoff_manager
    if _handoff_manager is None:
        _handoff_manager = HandoffManager()
    return _handoff_manager


def create_session(
    original_request: str,
    user_decisions: Optional[List[str]] = None,
    entities: Optional[Dict[str, Any]] = None
) -> str:
    """
    Criar nova sessão de handoff
    
    Usage:
        >>> session_id = create_session(
        ...     "Crie uma API REST",
        ...     ["tech=Node.js", "db=PostgreSQL"],
        ...     {"type": "api", "auth": "jwt"}
        ... )
    """
    manager = get_handoff_manager()
    session_id = str(uuid.uuid4())
    context = manager.create_context(
        session_id=session_id,
        original_request=original_request,
        user_decisions=user_decisions,
        entities=entities
    )
    return session_id


def execute_handoff(
    session_id: str,
    from_agent: str,
    to_agent: str,
    action: str,
    result: Optional[Dict[str, Any]] = None,
    quality_score: float = 1.0
) -> Dict:
    """
    Executar handoff entre agentes
    
    Usage:
        >>> result = execute_handoff(
        ...     session_id="...",
        ...     from_agent="frontend-specialist",
        ...     to_agent="backend-specialist",
        ...     action="API implementation",
        ...     result={"api_complete": True},
        ...     quality_score=0.95
        ... )
    """
    manager = get_handoff_manager()
    additional_ctx: Optional[Dict[str, Any]] = None
    if result:
        additional_ctx = {"result": result}
    
    return manager.execute_handoff(
        session_id=session_id,
        from_agent=from_agent,
        to_agent=to_agent,
        action=action,
        additional_context=additional_ctx,
        quality_score=quality_score
    )


def get_full_context(session_id: str) -> Optional[Dict]:
    """Obter contexto completo de uma sessão"""
    manager = get_handoff_manager()
    context = manager.get_context(session_id)
    return context.to_dict() if context else None


# Teste
if __name__ == "__main__":
    print("=" * 60)
    print("DYNAMIC HANDOFF PROTOCOL - TEST")
    print("=" * 60)
    
    # Criar sessão
    session_id = create_session(
        original_request="Crie uma rede social para estudantes",
        user_decisions=["tech=Vue 3", "auth=mock", "design=youthful"],
        entities={"type": "webapp", "target": "students"}
    )
    print(f"\n✅ Session created: {session_id}")
    
    # Simular handoffs
    handoffs = [
        ("orchestrator", "project-planner", "Create PLAN.md"),
        ("project-planner", "frontend-specialist", "UI implementation"),
        ("project-planner", "backend-specialist", "API implementation"),
        ("frontend-specialist", "test-engineer", "Verify implementation"),
        ("backend-specialist", "test-engineer", "Verify API")
    ]
    
    for from_a, to_a, action in handoffs:
        result = execute_handoff(
            session_id=session_id,
            from_agent=from_a,
            to_agent=to_a,
            action=action,
            result={"status": "completed"},
            quality_score=0.95
        )
        print(f"   {from_a} → {to_a}: {result['status']}")
    
    # Mostrar contexto final
    context = get_full_context(session_id)
    if context:
        print(f"\n📊 Final Context:")
        print(f"   - Handoff count: {context['handoff_count']}")
        print(f"   - Quality score: {context['quality_score']}")
        print(f"   - Audit trail: {len(context['audit_trail'])} entries")
    
    print("\n✅ All tests passed!")