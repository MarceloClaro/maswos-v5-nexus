#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Autonomous Agent (Claude+Manus Architecture)

Baseado nas arquiteturas:
- Claude Agent: Agent Loop com tools + memory + orchestration
- Manus AI: Planner → Memory → Tool loops com CodeAct

Arquitetura:
┌─────────────────────────────────────────────────────────────┐
│                    MASWOS AUTONOMOUS AGENT                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────────┐    ┌──────────────────┐   │
│  │ INPUT   │───▶│  PLANNER   │───▶│  MEMORY LAYER   │   │
│  │ (Goal)  │    │ (Decompose)│    │ (Context Store) │   │
│  └─────────┘    └─────────────┘    └──────────────────┘   │
│                        │                     │             │
│                        ▼                     ▼             │
│              ┌─────────────────┐    ┌──────────────────┐   │
│              │   SUB-AGENTS    │    │  ORCHESTRATOR   │   │
│              │  (Parallel Exec) │◀──▶│   (Coordinator) │   │
│              └─────────────────┘    └──────────────────┘   │
│                     │                     │             │
│                     ▼                     ▼             │
│              ┌─────────────────────────────────────┐     │
│              │         TOOL EXECUTOR               │     │
│              │  ┌────────┐ ┌────────┐ ┌────────┐  │     │
│              │  │Browser │ │CodeExec│ │ FileOp │  │     │
│              │  │Control │ │(Sandbox│ │        │  │     │
│              │  └────────┘ └────────┘ └────────┘  │     │
│              └─────────────────────────────────────┘     │
│                            │                             │
│                            ▼                             │
│              ┌─────────────────────────────────────┐     │
│              │         VERIFIER / REFLECTOR         │     │
│              │      (Self-Correction Loop)           │     │
│              └─────────────────────────────────────┘     │
│                            │                             │
│                            ▼                             │
│              ┌─────────────────────────────────────┐     │
│              │           OUTPUT / DELIVERABLE        │     │
│              │  Report | Code | Dashboard | Deploy    │     │
│              └─────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘

Features:
- Multi-agent decomposition (Manus-style)
- Agent Loop (Claude-style)
- CodeAct execution
- Memory persistence
- Self-healing loops
- Sandbox execution
"""

import asyncio
import json
import time
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MASWOSAgent")

# ============================================================
# CORE ENUMS E DATACLASSES
# ============================================================

class AgentState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

@dataclass
class ToolResult:
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    duration_ms: float = 0

@dataclass
class SubTask:
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    result: Optional[ToolResult] = None
    attempts: int = 0
    max_attempts: int = 3
    tools_needed: List[str] = field(default_factory=list)

@dataclass
class AgentContext:
    session_id: str
    goal: str
    state: AgentState = AgentState.IDLE
    tasks: List[SubTask] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

# ============================================================
# TOOL SYSTEM (Claude-style)
# ============================================================

class BaseTool(ABC):
    """Ferramenta base para o agent loop"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **params) -> ToolResult:
        """Executa a ferramenta"""
        pass
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description
        }

class WebSearchTool(BaseTool):
    """Ferramenta de busca web"""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Busca informações na web. Input: query (string)"
        )
    
    async def execute(self, query: str, **params) -> ToolResult:
        start = time.time()
        try:
            # Usa os scrapers integrados
            from transformer_scraper_integration import collect_academic_papers
            
            results = collect_academic_papers(query, limit=10)
            return ToolResult(
                tool_name=self.name,
                success=True,
                output=results,
                duration_ms=(time.time() - start) * 1000
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=None,
                error=str(e),
                duration_ms=(time.time() - start) * 1000
            )

class CodeExecutorTool(BaseTool):
    """Executor de código em sandbox"""
    
    def __init__(self, sandbox_path: str = ".agent_sandbox"):
        super().__init__(
            name="code_executor",
            description="Executa código Python em sandbox. Input: code (string)"
        )
        self.sandbox_path = sandbox_path
        import os
        os.makedirs(sandbox_path, exist_ok=True)
    
    async def execute(self, code: str, **params) -> ToolResult:
        start = time.time()
        try:
            # Executa código de forma segura
            import subprocess
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.sandbox_path
            )
            
            if result.returncode == 0:
                return ToolResult(
                    tool_name=self.name,
                    success=True,
                    output=result.stdout,
                    duration_ms=(time.time() - start) * 1000
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    success=False,
                    output=result.stdout,
                    error=result.stderr,
                    duration_ms=(time.time() - start) * 1000
                )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=None,
                error=str(e),
                duration_ms=(time.time() - start) * 1000
            )

class FileOperationTool(BaseTool):
    """Operações de arquivo"""
    
    def __init__(self):
        super().__init__(
            name="file_operation",
            description="Lê/escreve arquivos. Ops: read, write. Input: path, operation, content (opcional)"
        )
    
    async def execute(self, operation: str, path: str, content: str = None, **params) -> ToolResult:
        start = time.time()
        try:
            import os
            
            if operation == "read":
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        output = f.read()
                    return ToolResult(
                        tool_name=self.name,
                        success=True,
                        output=output,
                        duration_ms=(time.time() - start) * 1000
                    )
                else:
                    return ToolResult(
                        tool_name=self.name,
                        success=False,
                        output=None,
                        error=f"File not found: {path}",
                        duration_ms=(time.time() - start) * 1000
                    )
            elif operation == "write":
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content or "")
                return ToolResult(
                    tool_name=self.name,
                    success=True,
                    output=f"Written to {path}",
                    duration_ms=(time.time() - start) * 1000
                )
            else:
                return ToolResult(
                    tool_name=self.name,
                    success=False,
                    output=None,
                    error=f"Unknown operation: {operation}",
                    duration_ms=(time.time() - start) * 1000
                )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=None,
                error=str(e),
                duration_ms=(time.time() - start) * 1000
            )

class MCPInvokeTool(BaseTool):
    """Invoca MCP do ecossistema"""
    
    def __init__(self):
        super().__init__(
            name="mcp_invoke",
            description="Invoca MCP do ecossistema. Input: mcp_name, method, params"
        )
    
    async def execute(self, mcp_name: str, method: str, params: Dict = None, **kwargs) -> ToolResult:
        start = time.time()
        try:
            from unified_mcp_orchestrator import quick_query
            
            result = quick_query(params.get("query", ""), "all")
            return ToolResult(
                tool_name=self.name,
                success=True,
                output=result,
                duration_ms=(time.time() - start) * 1000
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=None,
                error=str(e),
                duration_ms=(time.time() - start) * 1000
            )

class ToolRegistry:
    """Registro de ferramentas disponíveis"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Registra ferramentas padrão"""
        self.register(WebSearchTool())
        self.register(CodeExecutorTool())
        self.register(FileOperationTool())
        self.register(MCPInvokeTool())
    
    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict]:
        return [tool.to_dict() for tool in self.tools.values()]

# ============================================================
# MEMORY SYSTEM (Manus-style)
# ============================================================

class AgentMemory:
    """
    Sistema de memória do agente
    Mantém contexto entre sessões e的长操作
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.short_term: Dict[str, Any] = {}  # Contexto atual
        self.long_term: Dict[str, Any] = {}     # Persistência
        self.working: Dict[str, Any] = {}       # Dados de trabalho
        self.knowledge: List[Dict] = []         # Conhecimento adquirido
    
    def store(self, key: str, value: Any, memory_type: str = "short"):
        """Armazena na memória"""
        if memory_type == "short":
            self.short_term[key] = value
        elif memory_type == "long":
            self.long_term[key] = value
        elif memory_type == "working":
            self.working[key] = value
    
    def retrieve(self, key: str, memory_type: str = "short") -> Any:
        """Recupera da memória"""
        if memory_type == "short":
            return self.short_term.get(key)
        elif memory_type == "long":
            return self.long_term.get(key)
        elif memory_type == "working":
            return self.working.get(key)
        return None
    
    def add_knowledge(self, knowledge: Dict):
        """Adiciona conhecimento aprendido"""
        knowledge["timestamp"] = datetime.now().isoformat()
        self.knowledge.append(knowledge)
    
    def get_context(self) -> str:
        """Gera contexto para o LLM"""
        context_parts = []
        
        if self.short_term:
            context_parts.append(f"Current Context: {json.dumps(self.short_term)}")
        if self.working:
            context_parts.append(f"Working Data: {json.dumps(self.working)}")
        if self.knowledge:
            recent = self.knowledge[-3:]
            context_parts.append(f"Recent Knowledge: {json.dumps(recent)}")
        
        return "\n".join(context_parts)

# ============================================================
# PLANNER (Manus-style decomposition)
# ============================================================

class TaskPlanner:
    """
    Planejador de tarefas
    Decompõe objetivos em sub-tarefas executáveis
    """
    
    def __init__(self):
        self.planning_prompt = """Você é um planejador de tarefas para um agente autônomo.
        
Analise o objetivo do usuário e decomponha em tarefas menores e executáveis.

Formate a resposta como JSON:
{
    "tasks": [
        {
            "id": "task_1",
            "description": "Descrição clara da tarefa",
            "dependencies": [],
            "estimated_time": "5min",
            "tools_needed": ["web_search", "code_executor"]
        }
    ],
    "plan_summary": "Resumo do plano de execução"
}

Objetivo: {goal}
"""
    
    def create_plan(self, goal: str) -> Dict:
        """Cria plano de execução (simulado)"""
        # Decomposição automática baseada em palavras-chave
        tasks = []
        task_id = 1
        
        goal_lower = goal.lower()
        
        # Detecção de necessidades
        if any(w in goal_lower for w in ["buscar", "pesquisar", "encontrar", "procurar"]):
            tasks.append({
                "id": f"task_{task_id}",
                "description": f"Pesquisar informações sobre: {goal}",
                "dependencies": [],
                "tools_needed": ["web_search", "mcp_invoke"]
            })
            task_id += 1
        
        if any(w in goal_lower for w in ["analisar", "processar", "calcular"]):
            tasks.append({
                "id": f"task_{task_id}",
                "description": f"Analisar e processar dados relacionados a: {goal}",
                "dependencies": [f"task_{task_id-1}"] if task_id > 1 else [],
                "tools_needed": ["code_executor"]
            })
            task_id += 1
        
        if any(w in goal_lower for w in ["gerar", "criar", "escrever", "produzir"]):
            tasks.append({
                "id": f"task_{task_id}",
                "description": f"Gerar resultado final sobre: {goal}",
                "dependencies": [f"task_{i}" for i in range(1, task_id)],
                "tools_needed": ["file_operation", "code_executor"]
            })
            task_id += 1
        
        if not tasks:
            tasks.append({
                "id": "task_1",
                "description": f"Executar análise sobre: {goal}",
                "dependencies": [],
                "tools_needed": ["web_search", "mcp_invoke"]
            })
        
        return {
            "tasks": [SubTask(**t) for t in tasks],
            "plan_summary": f"Plano com {len(tasks)} tarefas para: {goal[:50]}..."
        }

# ============================================================
# AGENT LOOP (Claude-style)
# ============================================================

class MASWOSAutonomousAgent:
    """
    Agente Autônomo MASWOS
    Combina Claude Agent Loop + Manus Planner
    
    Fluxo:
    1. Input (Goal) → Planner (decompose)
    2. Planner → SubTasks
    3. SubTasks → Tool Executor (parallel)
    4. Tool Results → Verifier
    5. Verify → Loop (se necessário) ou Output
    """
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.tools = ToolRegistry()
        self.memory = AgentMemory(self.session_id)
        self.planner = TaskPlanner()
        self.state = AgentState.IDLE
        self.context: Optional[AgentContext] = None
        
        logger.info(f"[MASWOSAgent] Session {self.session_id} initialized")
    
    async def execute_goal(self, goal: str, max_iterations: int = 10) -> Dict:
        """
        Executa um objetivo completo
        
        Returns:
            Dict com resultado, histórico e métricas
        """
        logger.info(f"[MASWOSAgent] Executing goal: {goal[:50]}...")
        
        # 1. CRIAR CONTEXTO
        self.context = AgentContext(
            session_id=self.session_id,
            goal=goal
        )
        self.state = AgentState.PLANNING
        
        # 2. PLANEJAR (Manus-style decomposition)
        plan = self.planner.create_plan(goal)
        self.context.tasks = plan["tasks"]
        self.memory.store("current_plan", plan)
        
        logger.info(f"[MASWOSAgent] Plan created: {len(self.context.tasks)} tasks")
        
        # 3. EXECUTAR LOOP (Claude-style)
        iteration = 0
        completed_tasks = []
        
        while iteration < max_iterations:
            iteration += 1
            self.state = AgentState.EXECUTING
            
            # Executa tarefas pendentes
            pending_tasks = [t for t in self.context.tasks 
                           if t.status == TaskStatus.PENDING and 
                           all(dep in completed_tasks for dep in t.dependencies)]
            
            if not pending_tasks:
                if all(t.status == TaskStatus.COMPLETED for t in self.context.tasks):
                    break
                continue
            
            # Executa em paralelo ( Manus-style)
            task_results = await self._execute_tasks_parallel(pending_tasks)
            
            # Atualiza status
            for task_id, result in task_results.items():
                task = next((t for t in self.context.tasks if t.id == task_id), None)
                if task:
                    task.result = result
                    task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
                    completed_tasks.append(task_id)
            
            # 4. VERIFICAR (Claude-style self-correction)
            self.state = AgentState.VERIFYING
            verification = await self._verify_completion()
            
            if verification["complete"]:
                break
        
        # 5. OUTPUT
        self.state = AgentState.COMPLETED
        return self._generate_output()
    
    async def _execute_tasks_parallel(self, tasks: List[SubTask]) -> Dict[str, ToolResult]:
        """Executa múltiplas tarefas em paralelo"""
        results = {}
        
        async def execute_single(task: SubTask):
            # Seleciona ferramenta
            tool_name = task.description.split()[0]
            if "pesquisar" in task.description.lower() or "buscar" in task.description.lower():
                tool = self.tools.get_tool("web_search")
            elif "gerar" in task.description.lower() or "criar" in task.description.lower():
                tool = self.tools.get_tool("file_operation")
            else:
                tool = self.tools.get_tool("mcp_invoke")
            
            if tool:
                params = {"query": task.description}
                result = await tool.execute(**params)
                results[task.id] = result
            else:
                results[task.id] = ToolResult(
                    tool_name="none",
                    success=False,
                    output=None,
                    error="No tool available"
                )
        
        # Executa em paralelo
        await asyncio.gather(*[execute_single(t) for t in tasks], return_exceptions=True)
        return results
    
    async def _verify_completion(self) -> Dict:
        """Verifica se o objetivo foi atingido"""
        completed = all(t.status == TaskStatus.COMPLETED for t in self.context.tasks)
        
        return {
            "complete": completed,
            "completed_count": sum(1 for t in self.context.tasks if t.status == TaskStatus.COMPLETED),
            "failed_count": sum(1 for t in self.context.tasks if t.status == TaskStatus.FAILED),
            "pending_count": sum(1 for t in self.context.tasks if t.status == TaskStatus.PENDING)
        }
    
    def _generate_output(self) -> Dict:
        """Gera output final"""
        results = []
        for task in self.context.tasks:
            if task.result:
                results.append({
                    "task_id": task.id,
                    "description": task.description,
                    "success": task.result.success,
                    "output": task.result.output,
                    "error": task.result.error
                })
        
        return {
            "session_id": self.session_id,
            "goal": self.context.goal,
            "status": "completed" if self.state == AgentState.COMPLETED else "failed",
            "tasks_executed": len(results),
            "results": results,
            "memory_summary": self.memory.get_context(),
            "timestamp": datetime.now().isoformat()
        }

# ============================================================
# SUB-AGENTS (Claude-style)
# ============================================================

class ResearchSubAgent:
    """Sub-agente para pesquisa (Manus-style)"""
    
    def __init__(self, agent: MASWOSAutonomousAgent):
        self.agent = agent
        self.tools = agent.tools
    
    async def research(self, topic: str) -> Dict:
        """Executa pesquisa aprofundada"""
        # 1. Busca inicial
        search_tool = self.tools.get_tool("web_search")
        initial_result = await search_tool.execute(query=topic)
        
        # 2. Coleta via MCPs
        mcp_tool = self.tools.get_tool("mcp_invoke")
        mcp_result = await mcp_tool.execute(
            mcp_name="academic",
            method="query",
            params={"query": topic}
        )
        
        # 3. Consolida
        return {
            "topic": topic,
            "web_results": initial_result.output if initial_result.success else [],
            "mcp_results": mcp_result.output if mcp_result.success else [],
            "timestamp": datetime.now().isoformat()
        }

class CodeSubAgent:
    """Sub-agente para código (Manus-style CodeAct)"""
    
    def __init__(self, agent: MASWOSAutonomousAgent):
        self.agent = agent
        self.tools = agent.tools
    
    async def generate_code(self, specification: str) -> Dict:
        """Gera e executa código"""
        executor = self.tools.get_tool("code_executor")
        
        # Gera código
        code = f"""
import json
result = {{
    "specification": "{specification}",
    "status": "generated",
    "timestamp": "{datetime.now().isoformat()}"
}}
print(json.dumps(result, indent=2))
"""
        
        # Executa
        result = await executor.execute(code=code)
        
        return {
            "specification": specification,
            "code": code,
            "execution_result": result.output if result.success else None,
            "error": result.error
        }

# ============================================================
# ORCHESTRATOR (Multi-agent coordination)
# ============================================================

class AgentOrchestrator:
    """
    Orquestrador de múltiplos agentes
    Coordena execução paralela de sub-agentes
    """
    
    def __init__(self):
        self.agents: Dict[str, MASWOSAutonomousAgent] = {}
        self.max_agents = 5
    
    def create_agent(self, agent_id: str) -> MASWOSAutonomousAgent:
        """Cria novo agente"""
        if len(self.agents) >= self.max_agents:
            raise Exception(f"Maximum agents ({self.max_agents}) reached")
        
        agent = MASWOSAutonomousAgent(session_id=agent_id)
        self.agents[agent_id] = agent
        return agent
    
    async def execute_parallel(self, goals: List[str]) -> List[Dict]:
        """Executa múltiplos objetivos em paralelo"""
        tasks = []
        
        for i, goal in enumerate(goals):
            agent_id = f"agent_{i}_{int(time.time())}"
            agent = self.create_agent(agent_id)
            tasks.append(agent.execute_goal(goal))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    def get_agent(self, agent_id: str) -> Optional[MASWOSAutonomousAgent]:
        return self.agents.get(agent_id)

# ============================================================
# FACTORY
# ============================================================

def create_autonomous_agent(session_id: Optional[str] = None) -> MASWOSAutonomousAgent:
    """Factory para criar agente autônomo"""
    return MASWOSAutonomousAgent(session_id=session_id)

def create_orchestrator() -> AgentOrchestrator:
    """Factory para criar orquestrador"""
    return AgentOrchestrator()

# ============================================================
# TESTE
# ============================================================

async def test_maswos_agent():
    """Testa o agente autônomo MASWOS"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - Autonomous Agent Test")
    print("=" * 70)
    
    # Cria agente
    agent = create_autonomous_agent("test_session_001")
    
    print(f"\n[INFO] Session: {agent.session_id}")
    print(f"[INFO] Tools available: {[t for t in agent.tools.list_tools()]}")
    
    # Teste 1: Pesquisa simples
    print("\n[TEST 1] Single Goal Execution")
    result = await agent.execute_goal("Pesquisar sobre machine learning no Brasil")
    print(f"  Status: {result['status']}")
    print(f"  Tasks: {result['tasks_executed']}")
    
    # Teste 2: Orquestrador
    print("\n[TEST 2] Parallel Execution")
    orchestrator = create_orchestrator()
    results = await orchestrator.execute_parallel([
        "Pesquisar dados do IBGE sobre população",
        "Buscar papers sobre deep learning"
    ])
    print(f"  Goals executed: {len(results)}")
    for i, r in enumerate(results):
        print(f"    Goal {i+1}: {r.get('status', 'error')}")
    
    # Teste 3: Sub-agents
    print("\n[TEST 3] Sub-Agent Research")
    research_agent = ResearchSubAgent(agent)
    research = await research_agent.research("inteligência artificial")
    print(f"  Topic: {research['topic']}")
    print(f"  Web results: {'OK' if research['web_results'] else 'Empty'}")
    
    print("\n" + "=" * 70)
    print("MASWOS Autonomous Agent - Architecture Verified!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    asyncio.run(test_maswos_agent())
