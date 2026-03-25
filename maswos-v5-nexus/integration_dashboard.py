"""
Integration Dashboard
=====================
Dashboard de monitoramento para a rede Transformer do OpenCode.

Autor: MASWOS V5 NEXUS
Versão: 5.1.0
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class MCPStatus:
    """Status de um MCP"""
    name: str
    endpoint: str
    status: str  # active, inactive, error
    latency_ms: float = 0.0
    error_rate: float = 0.0
    last_check: str = ""
    agents_count: int = 0
    capabilities: List[str] = field(default_factory=list)


@dataclass
class AgentStatus:
    """Status de um agente"""
    name: str
    domain: str
    status: str  # idle, busy, error
    tasks_completed: int = 0
    success_rate: float = 1.0
    avg_latency_ms: float = 0.0
    skills_injected: List[str] = field(default_factory=list)


@dataclass
class SkillStatus:
    """Status de um skill"""
    name: str
    domain: str
    loaded: bool = False
    last_used: str = ""
    usage_count: int = 0


class IntegrationDashboard:
    """Dashboard de integração para monitoramento"""
    
    def __init__(self):
        self.mcps: Dict[str, MCPStatus] = {}
        self.agents: Dict[str, AgentStatus] = {}
        self.skills: Dict[str, SkillStatus] = {}
        self.session_history: List[Dict] = []
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_latency_ms": 0.0,
            "routing_accuracy": 0.95
        }
        
        # Inicializar dados mock
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Inicializar dados de exemplo"""
        # MCPs
        self.mcps = {
            "maswos-juridico": MCPStatus(
                name="maswos-juridico",
                endpoint="http://localhost:3001/mcp",
                status="active",
                latency_ms=125.5,
                error_rate=0.02,
                last_check=datetime.now().isoformat(),
                agents_count=60,
                capabilities=["peticao", "jurisprudencia", "legislacao"]
            ),
            "maswos-mcp": MCPStatus(
                name="maswos-mcp",
                endpoint="http://localhost:3002/mcp",
                status="active",
                latency_ms=89.2,
                error_rate=0.01,
                last_check=datetime.now().isoformat(),
                agents_count=15,
                capabilities=["create_skill", "generate_agents"]
            ),
            "academic": MCPStatus(
                name="academic",
                endpoint="http://localhost:3003/mcp",
                status="active",
                latency_ms=210.8,
                error_rate=0.05,
                last_check=datetime.now().isoformat(),
                agents_count=55,
                capabilities=["research_paper", "collect_data", "scrape_government"]
            ),
            "pageindex": MCPStatus(
                name="pageindex",
                endpoint="https://api.pageindex.ai/mcp",
                status="active",
                latency_ms=180.3,
                error_rate=0.03,
                last_check=datetime.now().isoformat(),
                agents_count=10,
                capabilities=["index_documents", "query_documents"]
            ),
            "opencode": MCPStatus(
                name="opencode",
                endpoint="stdio",
                status="active",
                latency_ms=50.0,
                error_rate=0.0,
                last_check=datetime.now().isoformat(),
                agents_count=17,
                capabilities=["build", "edit", "ask", "plan", "orchestrate"]
            )
        }
        
        # Agents (exemplos)
        self.agents = {
            "project-planner": AgentStatus(
                name="project-planner",
                domain="planning",
                status="idle",
                tasks_completed=45,
                success_rate=0.98,
                avg_latency_ms=3200,
                skills_injected=["plan-writing", "brainstorming"]
            ),
            "frontend-specialist": AgentStatus(
                name="frontend-specialist",
                domain="frontend",
                status="busy",
                tasks_completed=78,
                success_rate=0.96,
                avg_latency_ms=4500,
                skills_injected=["react-best-practices", "tailwind-patterns", "frontend-design"]
            ),
            "backend-specialist": AgentStatus(
                name="backend-specialist",
                domain="backend",
                status="idle",
                tasks_completed=92,
                success_rate=0.97,
                avg_latency_ms=3800,
                skills_injected=["nodejs-best-practices", "api-patterns", "database-design"]
            ),
            "security-auditor": AgentStatus(
                name="security-auditor",
                domain="security",
                status="idle",
                tasks_completed=23,
                success_rate=1.0,
                avg_latency_ms=5200,
                skills_injected=["vulnerability-scanner", "red-team-tactics"]
            ),
            "test-engineer": AgentStatus(
                name="test-engineer",
                domain="testing",
                status="idle",
                tasks_completed=56,
                success_rate=0.94,
                avg_latency_ms=2900,
                skills_injected=["testing-patterns", "tdd-workflow", "webapp-testing"]
            ),
            "jurista-supremo": AgentStatus(
                name="jurista-supremo",
                domain="juridico",
                status="idle",
                tasks_completed=34,
                success_rate=0.99,
                avg_latency_ms=8000,
                skills_injected=["legal-agents", "juridico-workflow"]
            )
        }
        
        # Skills (exemplos)
        self.skills = {
            "criador-de-artigo-v2": SkillStatus(
                name="criador-de-artigo-v2",
                domain="academic",
                loaded=True,
                last_used=datetime.now().isoformat(),
                usage_count=15
            ),
            "vulnerability-scanner": SkillStatus(
                name="vulnerability-scanner",
                domain="security",
                loaded=True,
                last_used=datetime.now().isoformat(),
                usage_count=8
            ),
            "react-best-practices": SkillStatus(
                name="react-best-practices",
                domain="frontend",
                loaded=True,
                last_used=datetime.now().isoformat(),
                usage_count=22
            ),
            "api-patterns": SkillStatus(
                name="api-patterns",
                domain="backend",
                loaded=True,
                last_used=datetime.now().isoformat(),
                usage_count=18
            ),
            "database-design": SkillStatus(
                name="database-design",
                domain="database",
                loaded=True,
                last_used=datetime.now().isoformat(),
                usage_count=12
            )
        }
    
    def get_mcp_summary(self) -> Dict:
        """Obter resumo dos MCPs"""
        total = len(self.mcps)
        active = sum(1 for m in self.mcps.values() if m.status == "active")
        error = sum(1 for m in self.mcps.values() if m.status == "error")
        
        return {
            "total": total,
            "active": active,
            "inactive": total - active - error,
            "error": error,
            "avg_latency_ms": sum(m.latency_ms for m in self.mcps.values()) / total if total else 0,
            "total_agents": sum(m.agents_count for m in self.mcps.values())
        }
    
    def get_agent_summary(self) -> Dict:
        """Obter resumo dos agentes"""
        total = len(self.agents)
        busy = sum(1 for a in self.agents.values() if a.status == "busy")
        idle = total - busy
        
        return {
            "total": total,
            "busy": busy,
            "idle": idle,
            "total_tasks": sum(a.tasks_completed for a in self.agents.values()),
            "avg_success_rate": sum(a.success_rate for a in self.agents.values()) / total if total else 0
        }
    
    def get_skill_summary(self) -> Dict:
        """Obter resumo dos skills"""
        total = len(self.skills)
        loaded = sum(1 for s in self.skills.values() if s.loaded)
        
        return {
            "total": total,
            "loaded": loaded,
            "total_usages": sum(s.usage_count for s in self.skills.values())
        }
    
    def get_full_report(self) -> Dict:
        """Obter relatório completo"""
        return {
            "timestamp": datetime.now().isoformat(),
            "mcp_summary": self.get_mcp_summary(),
            "agent_summary": self.get_agent_summary(),
            "skill_summary": self.get_skill_summary(),
            "metrics": self.metrics,
            "mcp_details": {
                name: {
                    "status": mcp.status,
                    "latency_ms": mcp.latency_ms,
                    "error_rate": mcp.error_rate,
                    "agents_count": mcp.agents_count,
                    "capabilities": mcp.capabilities
                }
                for name, mcp in self.mcps.items()
            },
            "agent_details": {
                name: {
                    "domain": agent.domain,
                    "status": agent.status,
                    "tasks_completed": agent.tasks_completed,
                    "success_rate": agent.success_rate,
                    "skills_injected": agent.skills_injected
                }
                for name, agent in self.agents.items()
            }
        }
    
    def print_dashboard(self):
        """Imprimir dashboard formatado"""
        print("=" * 70)
        print("TRANSFORMER NETWORK INTEGRATION DASHBOARD")
        print("=" * 70)
        
        # MCP Summary
        mcp_s = self.get_mcp_summary()
        print(f"\nMCPs: {mcp_s['active']}/{mcp_s['total']} ativos | {mcp_s['total_agents']} agentes | {mcp_s['avg_latency_ms']:.1f}ms avg")
        
        for name, mcp in self.mcps.items():
            status_icon = "[+]" if mcp.status == "active" else "[!]" if mcp.status == "error" else "[-]"
            print(f"   {status_icon} {name}: {mcp.latency_ms:.1f}ms | {mcp.error_rate*100:.1f}% errors | {mcp.agents_count} agents")
        
        # Agent Summary
        agent_s = self.get_agent_summary()
        print(f"\nAgentes: {agent_s['busy']}/{agent_s['total']} ocupados | {agent_s['total_tasks']} tasks | {agent_s['avg_success_rate']*100:.1f}% success")
        
        for name, agent in self.agents.items():
            status_icon = "[*]" if agent.status == "busy" else "[ ]" if agent.status == "idle" else "[!]"
            skills = ", ".join(agent.skills_injected[:2]) + ("..." if len(agent.skills_injected) > 2 else "")
            print(f"   {status_icon} {name}: {agent.tasks_completed} tasks | {agent.success_rate*100:.0f}% | [{skills}]")
        
        # Skill Summary
        skill_s = self.get_skill_summary()
        print(f"\nSkills: {skill_s['loaded']}/{skill_s['total']} carregados | {skill_s['total_usages']} usos")
        
        for name, skill in self.skills.items():
            print(f"   * {name}: {skill.usage_count} usos")
        
        print("\n" + "=" * 70)
    
    def to_json(self) -> str:
        """Exportar para JSON"""
        return json.dumps(self.get_full_report(), indent=2)
    
    def to_markdown(self) -> str:
        """Exportar para Markdown"""
        report = self.get_full_report()
        
        md = [
            "# Transformer Network - Integration Dashboard",
            "",
            f"**Atualizado:** {report['timestamp']}",
            "",
            "## Resumo",
            "",
            f"- **MCPs:** {report['mcp_summary']['active']}/{report['mcp_summary']['total']} ativos",
            f"- **Agentes:** {report['agent_summary']['busy']}/{report['agent_summary']['total']} ocupados",
            f"- **Skills:** {report['skill_summary']['loaded']}/{report['skill_summary']['total']} carregados",
            "",
            "## MCPs",
            "",
            "| MCP | Status | Latência | Erros | Agentes |",
            "|-----|--------|----------|-------|---------|"
        ]
        
        for name, mcp in report['mcp_details'].items():
            md.append(f"| {name} | {mcp['status']} | {mcp['latency_ms']:.1f}ms | {mcp['error_rate']*100:.1f}% | {mcp['agents_count']} |")
        
        md.extend([
            "",
            "## Agentes",
            "",
            "| Agente | Domínio | Status | Tasks | Success Rate |",
            "|--------|----------|--------|-------|--------------|"
        ])
        
        for name, agent in report['agent_details'].items():
            md.append(f"| {name} | {agent['domain']} | {agent['status']} | {agent['tasks_completed']} | {agent['success_rate']*100:.0f}% |")
        
        return "\n".join(md)


# Instância global
_dashboard = None

def get_dashboard() -> IntegrationDashboard:
    """Obter instância global do dashboard"""
    global _dashboard
    if _dashboard is None:
        _dashboard = IntegrationDashboard()
    return _dashboard


def show_dashboard():
    """Mostrar dashboard no console"""
    dashboard = get_dashboard()
    dashboard.print_dashboard()


def get_report() -> Dict:
    """Obter relatório completo"""
    dashboard = get_dashboard()
    return dashboard.get_full_report()


# Teste
if __name__ == "__main__":
    show_dashboard()
    print("\n📄 Markdown Output:")
    print(get_dashboard().to_markdown())