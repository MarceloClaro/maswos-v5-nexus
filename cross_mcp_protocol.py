"""
Cross-MCP Communication Protocol
=================================
Sistema de comunicação entre múltiplos MCPs na rede Transformer do OpenCode.

Autor: MASWOS V5 NEXUS
Versão: 5.1.0
"""

import json
import asyncio
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class MCPType(Enum):
    """Tipos de MCP disponíveis"""
    JURIDICO = "maswos-juridico"
    SKILL_GENERATION = "maswos-mcp"
    ACADEMIC = "academic"
    PAGEINDEX = "pageindex"
    OPENCODE = "opencode"
    FILESYSTEM = "filesystem"
    GITHUB = "github"


class IntentType(Enum):
    """Tipos de intent detectados"""
    JURIDICO = "juridico"
    ACADEMIC = "academic"
    SKILL_GENERATION = "skill_generation"
    DEVELOPMENT = "development"
    SECURITY = "security"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DATABASE = "database"
    PERFORMANCE = "performance"
    SEO = "seo"


@dataclass
class MCPContext:
    """Contexto compartilhado entre MCPs"""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    original_request: str = ""
    entities: Dict[str, Any] = field(default_factory=dict)
    intent_type: Optional[IntentType] = None
    quality_score: float = 1.0
    audit_trail: List[Dict] = field(default_factory=list)
    intermediate_results: Dict[str, Any] = field(default_factory=dict)
    
    def add_audit(self, agent: str, action: str, result: Any):
        """Adicionar entrada ao audit trail"""
        self.audit_trail.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "result": str(result)[:500]  # Truncate para evitar logs muito grandes
        })
    
    def to_dict(self) -> Dict:
        """Serializar para dict"""
        return {
            "session_id": self.session_id,
            "original_request": self.original_request,
            "entities": self.entities,
            "intent_type": self.intent_type.value if self.intent_type else None,
            "quality_score": self.quality_score,
            "audit_trail": self.audit_trail,
            "intermediate_results": self.intermediate_results
        }


@dataclass
class MCPCall:
    """Representa uma chamada a um MCP"""
    mcp_type: MCPType
    function: str
    params: Dict[str, Any]
    context: MCPContext
    priority: int = 1
    timeout_ms: int = 30000
    
    def to_dict(self) -> Dict:
        return {
            "mcp": self.mcp_type.value,
            "function": self.function,
            "params": self.params,
            "priority": self.priority
        }


class MCPRegistry:
    """Registro de MCPs disponíveis"""
    
    def __init__(self):
        self.mcps: Dict[MCPType, Dict[str, Any]] = {
            MCPType.JURIDICO: {
                "endpoint": "http://localhost:3001/mcp",
                "type": "legal",
                "agents": 60,
                "capabilities": ["peticao", "jurisprudencia", "legislacao", "parecer", "contrato"],
                "status": "configured",
                "skills": ["legal-agents", "juridico-workflow"]
            },
            MCPType.SKILL_GENERATION: {
                "endpoint": "http://localhost:3002/mcp",
                "type": "skill-generation",
                "agents": 15,
                "capabilities": ["create_skill", "generate_agents", "validate_skill"],
                "status": "configured",
                "skills": ["mcp-builder", "ecosystem-create-skill"]
            },
            MCPType.ACADEMIC: {
                "endpoint": "http://localhost:3003/mcp",
                "type": "academic-research",
                "agents": 55,
                "capabilities": ["research_paper", "collect_data", "validate_methodology"],
                "status": "configured",
                "scrapers": ["arxiv", "pubmed", "semantic_scholar", "doaj", "capes", "ibge"],
                "skills": ["criador-de-artigo-v2", "academic-research"]
            },
            MCPType.PAGEINDEX: {
                "endpoint": "https://api.pageindex.ai/mcp",
                "type": "vectorless-rag",
                "agents": 10,
                "capabilities": ["index_documents", "query_documents", "tree_reasoning"],
                "features": {"vectorless_rag": True, "tree_indexing": True},
                "status": "active"
            },
            MCPType.OPENCODE: {
                "endpoint": "stdio",
                "type": "ai-coding-agent",
                "agents": 17,
                "capabilities": ["build", "edit", "ask", "plan", "orchestrate"],
                "status": "active"
            }
        }
    
    def get_mcp(self, mcp_type: MCPType) -> Optional[Dict]:
        """Obter configuração de um MCP"""
        return self.mcps.get(mcp_type)
    
    def get_capabilities(self, mcp_type: MCPType) -> List[str]:
        """Obter capabilities de um MCP"""
        mcp = self.mcps.get(mcp_type)
        return mcp.get("capabilities", []) if mcp else []
    
    def get_skills(self, mcp_type: MCPType) -> List[str]:
        """Obter skills associados a um MCP"""
        mcp = self.mcps.get(mcp_type)
        return mcp.get("skills", []) if mcp else []
    
    def list_available(self) -> List[str]:
        """Listar MCPs disponíveis"""
        return [mcp.value for mcp, config in self.mcps.items() if config.get("status") == "active"]


class IntentClassifier:
    """Classificador de intent do usuário"""
    
    def __init__(self):
        self.patterns: Dict[IntentType, List[str]] = {
            IntentType.JURIDICO: [
                "petição", "jurisprudência", "advogado", "tribunal", "processo", 
                "sentença", "recurso", "direito", "civil", "penal", "trabalhista",
                "tributário", "consumidor", "constitucional"
            ],
            IntentType.ACADEMIC: [
                "artigo", "pesquisa", "dissertação", "tese", "paper", 
                "qualis", "acadêmico", "publicação", "scientific"
            ],
            IntentType.SKILL_GENERATION: [
                "criar skill", "gerar skill", "desenvolver skill", "skill novo"
            ],
            IntentType.DEVELOPMENT: [
                "criar", "desenvolver", "implementar", "api", "web", "app",
                "frontend", "backend", "server", "aplicação"
            ],
            IntentType.SECURITY: [
                "segurança", "vulnerabilidade", "auditoria", "pentest", "scan",
                "seguro", "proteger", "vulnerabilidades", "invasão", "ataque",
                "audite", "segurança", "penetração", "malware", "hack"
            ],
            IntentType.TESTING: [
                "teste", "testar", "coverage", "e2e", "unit", "integration"
            ],
            IntentType.DATABASE: [
                "banco", "schema", "sql", "migration", "query", "dados"
            ],
            IntentType.PERFORMANCE: [
                "otimizar", "performance", "profiling", "lento", "velocidade"
            ],
            IntentType.SEO: [
                "seo", "google", "busca", "ranking", "visibilidade"
            ]
        }
        
        self.mcp_mapping: Dict[IntentType, MCPType] = {
            IntentType.JURIDICO: MCPType.JURIDICO,
            IntentType.ACADEMIC: MCPType.ACADEMIC,
            IntentType.SKILL_GENERATION: MCPType.SKILL_GENERATION,
            IntentType.DEVELOPMENT: MCPType.OPENCODE,
            IntentType.SECURITY: MCPType.OPENCODE,
            IntentType.TESTING: MCPType.OPENCODE,
            IntentType.DATABASE: MCPType.OPENCODE,
            IntentType.PERFORMANCE: MCPType.OPENCODE,
            IntentType.SEO: MCPType.OPENCODE
        }
    
    def classify(self, message: str) -> IntentType:
        """Classificar intent da mensagem"""
        message_lower = message.lower()
        
        scores: Dict[IntentType, int] = {}
        for intent, patterns in self.patterns.items():
            score = sum(1 for p in patterns if p in message_lower)
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return IntentType.DEVELOPMENT  # Default
        
        # Corrigido: usar max com key lambda explícita
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def get_mcp_for_intent(self, intent: Optional[IntentType]) -> MCPType:
        """Obter MCP correto para o intent"""
        if intent is None:
            return MCPType.OPENCODE
        return self.mcp_mapping.get(intent, MCPType.OPENCODE)
    
    def get_agents_for_intent(self, intent: Optional[IntentType]) -> List[str]:
        """Obter agentes recomendados para o intent"""
        agent_mapping: Dict[IntentType, List[str]] = {
            IntentType.JURIDICO: ["jurista-supremo", "especialista-civil", "especialista-penal"],
            IntentType.ACADEMIC: ["research-planner", "paper-collector", "methodology-generator"],
            IntentType.SKILL_GENERATION: ["domain-analyzer", "scope-mapper", "agent-factory"],
            IntentType.DEVELOPMENT: ["frontend-specialist", "backend-specialist", "database-architect"],
            IntentType.SECURITY: ["security-auditor", "penetration-tester"],
            IntentType.TESTING: ["test-engineer", "qa-automation-engineer"],
            IntentType.DATABASE: ["database-architect"],
            IntentType.PERFORMANCE: ["performance-optimizer"],
            IntentType.SEO: ["seo-specialist"]
        }
        if intent is None:
            return ["general"]
        return agent_mapping.get(intent, ["general"])
    
    def get_skills_for_intent(self, intent: Optional[IntentType]) -> List[str]:
        """Obter skills recomendados para o intent"""
        skill_mapping: Dict[IntentType, List[str]] = {
            IntentType.JURIDICO: ["legal-agents", "juridico-workflow"],
            IntentType.ACADEMIC: ["criador-de-artigo-v2", "academic-research"],
            IntentType.SKILL_GENERATION: ["mcp-builder", "ecosystem-create-skill"],
            IntentType.DEVELOPMENT: ["api-patterns", "nodejs-best-practices", "react-best-practices"],
            IntentType.SECURITY: ["vulnerability-scanner", "red-team-tactics"],
            IntentType.TESTING: ["testing-patterns", "tdd-workflow", "webapp-testing"],
            IntentType.DATABASE: ["database-design"],
            IntentType.PERFORMANCE: ["performance-profiling"],
            IntentType.SEO: ["seo-fundamentals"]
        }
        if intent is None:
            return []
        return skill_mapping.get(intent, [])


class ResultMerger:
    """Mesclador de resultados de múltiplos MCPs"""
    
    @staticmethod
    def weighted_merge(results: List[Dict], weights: Dict[str, float]) -> Dict:
        """Mesclagem ponderada por relevância"""
        if not results:
            return {}
        
        merged: Dict[str, float] = {}
        total_weight = sum(weights.values())
        
        for result in results:
            for key, value in result.items():
                if isinstance(value, (int, float)):
                    weight = weights.get(key, 1.0)
                    if key not in merged:
                        merged[key] = 0.0
                    merged[key] += float(value) * weight / total_weight
        
        return merged
    
    @staticmethod
    def priority_order_merge(results: List[Dict], priority: List[str]) -> Dict:
        """Mesclagem por ordem de prioridade"""
        if not results:
            return {}
        
        # Criar dicionário de resultados por MCP
        results_by_mcp: Dict[str, Dict] = {}
        for result in results:
            mcp = result.get("_mcp", "unknown")
            results_by_mcp[mcp] = result
        
        # Aplicar prioridade
        merged: Dict[str, Any] = {}
        for mcp_name in priority:
            if mcp_name in results_by_mcp:
                merged.update(results_by_mcp[mcp_name])
        
        return merged
    
    @staticmethod
    def consensus_merge(results: List[Dict], threshold: float = 0.5) -> Dict:
        """Mesclagem por consenso (majority agreement)"""
        if not results:
            return {}
        
        # Contar ocorrências de cada valor
        value_counts: Dict[str, Dict[str, int]] = {}
        for result in results:
            for key, value in result.items():
                if key not in value_counts:
                    value_counts[key] = {}
                value_str = str(value)
                value_counts[key][value_str] = value_counts[key].get(value_str, 0) + 1
        
        # Selecionar valores com maioria
        merged: Dict[str, Any] = {}
        for key, counts in value_counts.items():
            total = sum(counts.values())
            for value_str, count in counts.items():
                if count / total >= threshold:
                    # Parsear de volta para tipo original
                    try:
                        merged[key] = json.loads(value_str)
                    except (json.JSONDecodeError, TypeError):
                        merged[key] = value_str
                    break
        
        return merged


class CrossMCPOrchestrator:
    """Orquestrador de chamadas cross-MCP"""
    
    def __init__(self):
        self.registry = MCPRegistry()
        self.classifier = IntentClassifier()
        self.merger = ResultMerger()
        self.active_contexts: Dict[str, MCPContext] = {}
    
    def create_context(self, message: str) -> MCPContext:
        """Criar novo contexto para uma requisição"""
        intent = self.classifier.classify(message)
        context = MCPContext(
            original_request=message,
            intent_type=intent
        )
        self.active_contexts[context.session_id] = context
        return context
    
    def plan_execution(self, context: MCPContext) -> List[MCPCall]:
        """Planejar sequência de execução de MCPs"""
        calls = []
        intent = context.intent_type
        
        if intent is None:
            intent = IntentType.DEVELOPMENT
        
        # MCP primário
        primary_mcp = self.classifier.get_mcp_for_intent(intent)
        calls.append(MCPCall(
            mcp_type=primary_mcp,
            function=self._get_primary_function(intent),
            params={"request": context.original_request},
            context=context,
            priority=1
        ))
        
        # MCPs secundários baseados em dependências
        if intent == IntentType.ACADEMIC:
            # Academic pode usar PageIndex para RAG
            calls.append(MCPCall(
                mcp_type=MCPType.PAGEINDEX,
                function="rag_query",
                params={"query": context.original_request},
                context=context,
                priority=2
            ))
        
        return sorted(calls, key=lambda x: x.priority)
    
    def _get_primary_function(self, intent: IntentType) -> str:
        """Mapear intent para função do MCP"""
        function_map: Dict[IntentType, str] = {
            IntentType.JURIDICO: "juridico_workflow",
            IntentType.ACADEMIC: "academic_research",
            IntentType.SKILL_GENERATION: "create_skill",
            IntentType.DEVELOPMENT: "build_project",
            IntentType.SECURITY: "security_audit",
            IntentType.TESTING: "run_tests",
            IntentType.DATABASE: "design_database",
            IntentType.PERFORMANCE: "optimize_performance",
            IntentType.SEO: "seo_analysis"
        }
        return function_map.get(intent, "general_task")
    
    async def execute_parallel(self, calls: List[MCPCall]) -> List[Dict]:
        """Executar múltiplas chamadas em paralelo"""
        
        async def call_mcp(call: MCPCall) -> Dict:
            # Simular chamada MCP (substituir por implementação real)
            return {
                "_mcp": call.mcp_type.value,
                "function": call.function,
                "result": f"Result from {call.mcp_type.value}",
                "status": "success"
            }
        
        # Executar em paralelo
        tasks = [call_mcp(call) for call in calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar exceptions
        return [r for r in results if isinstance(r, dict)]
    
    def merge_results(self, results: List[Dict], strategy: str = "priority") -> Dict:
        """Mesclar resultados de múltiplos MCPs"""
        if strategy == "weighted":
            weights = {r.get("_mcp", "unknown"): 1.0 for r in results}
            return self.merger.weighted_merge(results, weights)
        elif strategy == "priority":
            return self.merger.priority_order_merge(
                results, 
                ["maswos-juridico", "academic", "maswos-mcp", "opencode"]
            )
        elif strategy == "consensus":
            return self.merger.consensus_merge(results)
        else:
            # Last resort - just merge all
            merged: Dict[str, Any] = {}
            for r in results:
                merged.update(r)
            return merged
    
    def get_status_report(self) -> Dict:
        """Gerar relatório de status dos MCPs"""
        return {
            "registry": {
                mcp.value: config.get("status", "unknown")
                for mcp, config in self.registry.mcps.items()
            },
            "active_contexts": len(self.active_contexts),
            "available_mcps": self.registry.list_available()
        }


# Instância global do orquestrador
_orchestrator: Optional[CrossMCPOrchestrator] = None

def get_orchestrator() -> CrossMCPOrchestrator:
    """Obter instância global do orquestrador"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = CrossMCPOrchestrator()
    return _orchestrator


def classify_and_route(message: str) -> Dict:
    """
    Função principal: classificar intent e planejar rota
    
    Usage:
        >>> result = classify_and_route("Preciso de uma petição de danos materiais")
        >>> print(result)
        {
            "intent": "juridico",
            "mcp": "maswos-juridico",
            "agents": ["jurista-supremo", "especialista-civil"],
            "skills": ["legal-agents", "juridico-workflow"],
            "execution_plan": [...]
        }
    """
    orchestrator = get_orchestrator()
    context = orchestrator.create_context(message)
    calls = orchestrator.plan_execution(context)
    
    intent = context.intent_type
    classifier = orchestrator.classifier
    
    return {
        "intent": intent.value if intent else "unknown",
        "mcp": classifier.get_mcp_for_intent(intent).value if intent else "opencode",
        "agents": classifier.get_agents_for_intent(intent),
        "skills": classifier.get_skills_for_intent(intent),
        "session_id": context.session_id,
        "execution_plan": [call.to_dict() for call in calls]
    }


async def execute_workflow(message: str) -> Dict:
    """
    Executar workflow completo com múltiplos MCPs
    
    Usage:
        >>> result = await execute_workflow("Escreva um artigo sobre IA na educação")
        >>> print(result)
    """
    orchestrator = get_orchestrator()
    context = orchestrator.create_context(message)
    calls = orchestrator.plan_execution(context)
    
    # Executar em paralelo
    results = await orchestrator.execute_parallel(calls)
    
    # Mesclar resultados
    merged = orchestrator.merge_results(results)
    
    context.add_audit("cross_mcp_orchestrator", "workflow_execution", merged)
    
    return {
        "context": context.to_dict(),
        "results": results,
        "merged_result": merged,
        "status": "completed"
    }


# Teste rápido
if __name__ == "__main__":
    # Teste de classificação
    test_messages = [
        "Preciso de uma petição inicial de ação de danos",
        "Escreva um artigo científico sobre machine learning",
        "Crie uma API REST com autenticação JWT",
        "Audite esta aplicação web para vulnerabilidades"
    ]
    
    print("=" * 60)
    print("CROSS-MCP COMMUNICATION PROTOCOL - TEST")
    print("=" * 60)
    
    for msg in test_messages:
        result = classify_and_route(msg)
        print(f"\n📝 Input: {msg}")
        print(f"   🎯 Intent: {result['intent']}")
        print(f"   🔗 MCP: {result['mcp']}")
        print(f"   👥 Agents: {', '.join(result['agents'])}")
        print(f"   🛠️ Skills: {', '.join(result['skills'])}")
    
    print("\n" + "=" * 60)
    print("MCP Status Report:")
    print(get_orchestrator().get_status_report())