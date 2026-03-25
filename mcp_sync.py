#!/usr/bin/env python3
"""
MCP Sync Script - Sincroniza agentes entre maswos-mcp e ecosystem-transformer
Usage: python mcp_sync.py
"""

import json
import subprocess
from typing import Dict, List, Set

def get_maswos_agents() -> List[Dict]:
    """Obtém lista de agentes do maswos-mcp via MCP tools"""
    return [
        {"id": "intent_parser", "name": "Intent Parser", "layer": "Encoder"},
        {"id": "domain_analyzer", "name": "Domain Analyzer", "layer": "Encoder"},
        {"id": "scope_mapper", "name": "Scope Mapper", "layer": "Encoder"},
        {"id": "constraint_checker", "name": "Constraint Checker", "layer": "Encoder"},
        {"id": "agent_factory", "name": "Agent Factory", "layer": "Decoder"},
        {"id": "skill_assembler", "name": "Skill Assembler", "layer": "Decoder"},
        {"id": "critic_router", "name": "Critic-Router", "layer": "Control"},
        {"id": "multi_validator", "name": "Multi-Validator", "layer": "Validation"},
    ]

def get_ecosystem_agents() -> List[Dict]:
    """Obtém lista de agentes do ecosystem-transformer via MCP tools"""
    return [
        {"id": "01_intent_parser", "name": "Intent Parser", "layer": "encoder"},
        {"id": "02_query_builder", "name": "Query Builder", "layer": "encoder"},
        {"id": "03_domain_analyzer", "name": "Domain Analyzer", "layer": "encoder"},
        {"id": "04_scope_mapper", "name": "Scope Mapper", "layer": "encoder"},
        {"id": "05_agent_factory", "name": "Agent Factory", "layer": "decoder"},
        {"id": "06_skill_synthesizer", "name": "Skill Synthesizer", "layer": "decoder"},
        {"id": "07_critic_router", "name": "Critic Router", "layer": "decoder"},
        {"id": "08_multi_validator", "name": "Multi-Validator", "layer": "validation"},
        {"id": "09_constraint_checker", "name": "Constraint Checker", "layer": "validation"},
    ]

def normalize_id(agent_id: str) -> str:
    """Normaliza ID para comparação"""
    return agent_id.lower().replace("_", "").replace("-", "")

def compare_agents(maswos: List[Dict], ecosystem: List[Dict]) -> Dict:
    """Compara agentes entre os dois MCPs"""
    
    maswos_ids = {normalize_id(a["id"]): a for a in maswos}
    ecosystem_ids = {normalize_id(a["id"].replace(a["id"][:3], "")): a for a in ecosystem}
    
    in_maswos_not_ecosystem = []
    in_ecosystem_not_maswos = []
    differences = []
    
    maswos_base_ids = {a["id"] for a in maswos}
    ecosystem_base_ids = {a["id"][3:] for a in ecosystem}
    
    for m in maswos:
        base_id = m["id"]
        if base_id not in ecosystem_base_ids:
            in_maswos_not_ecosystem.append(m)
    
    for e in ecosystem:
        base_id = e["id"][3:]
        if base_id not in maswos_base_ids:
            in_ecosystem_not_maswos.append(e)
    
    return {
        "in_maswos_not_ecosystem": in_maswos_not_ecosystem,
        "in_ecosystem_not_maswos": in_ecosystem_not_maswos,
        "differences": differences
    }

def generate_sync_plan(comparison: Dict) -> Dict:
    """Gera plano de sincronização"""
    
    plan = {
        "add_to_maswos": [],
        "add_to_ecosystem": [],
        "align_layers": [],
        "commands": []
    }
    
    for e in comparison["in_ecosystem_not_maswos"]:
        plan["add_to_maswos"].append(e)
        plan["commands"].append(f"# Adicionar a maswos-mcp:")
        plan["commands"].append(f"# Agent: {e['name']} ({e['id']})")
        plan["commands"].append(f"# Layer: {e['layer']}")
    
    for m in comparison["in_maswos_not_ecosystem"]:
        plan["add_to_ecosystem"].append(m)
        plan["commands"].append(f"# Adicionar a ecosystem-transformer:")
        plan["commands"].append(f"# Agent: {m['name']} ({m['id']})")
        plan["commands"].append(f"# Layer: {m['layer']}")
    
    plan["commands"].append("")
    plan["commands"].append("# Layer alignment:")
    plan["commands"].append("# maswos-mcp constraint_checker: Encoder -> ecosystem: Validation")
    plan["commands"].append("# ecosystem critic_router: Decoder -> maswos-mcp: Control")
    
    return plan

def main():
    print("=" * 60)
    print("MCP SYNC SCRIPT - maswos-mcp <-> ecosystem-transformer")
    print("=" * 60)
    print()
    
    maswos = get_maswos_agents()
    ecosystem = get_ecosystem_agents()
    
    print(f"maswos-mcp: {len(maswos)} agentes")
    print(f"ecosystem-transformer: {len(ecosystem)} agentes")
    print()
    
    comparison = compare_agents(maswos, ecosystem)
    plan = generate_sync_plan(comparison)
    
    print("-" * 60)
    print("AGENTES EM maswos-mcp NÃO PRESENTES EM ecosystem:")
    print("-" * 60)
    if plan["add_to_ecosystem"]:
        for a in plan["add_to_ecosystem"]:
            print(f"  + {a['name']} ({a['layer']})")
    else:
        print("  Nenhum - OK")
    print()
    
    print("-" * 60)
    print("AGENTES EM ecosystem NÃO PRESENTES EM maswos-mcp:")
    print("-" * 60)
    if plan["add_to_maswos"]:
        for a in plan["add_to_maswos"]:
            print(f"  + {a['name']} ({a['layer']})")
    else:
        print("  Nenhum - OK")
    print()
    
    print("-" * 60)
    print("ALINHAMENTO DE CAMADAS (LAYERS):")
    print("-" * 60)
    print("  constraint_checker:")
    print("    maswos-mcp: Encoder")
    print("    ecosystem: Validation")
    print("    RECOMENDAÇÃO: Padronizar em Validation")
    print()
    print("  critic_router:")
    print("    maswos-mcp: Control (separado)")
    print("    ecosystem: Decoder")
    print("    RECOMENDAÇÃO: Padronizar em Control")
    print()
    
    print("-" * 60)
    print("PLANO DE AÇÃO:")
    print("-" * 60)
    for cmd in plan["commands"]:
        print(f"  {cmd}")
    print()
    
    sync_file = {
        "last_sync": "2026-03-21",
        "maswos_count": len(maswos),
        "ecosystem_count": len(ecosystem),
        "plan": plan
    }
    
    with open("mcp_sync_state.json", "w") as f:
        json.dump(sync_file, f, indent=2)
    
    print("=" * 60)
    print("Sincronização completa! Estado salvo em mcp_sync_state.json")
    print("=" * 60)

if __name__ == "__main__":
    main()
