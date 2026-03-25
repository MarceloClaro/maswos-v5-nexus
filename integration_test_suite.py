"""
Integration Test Suite
======================
Testes de integracao entre os modulos de integração do MASWOS V5 NEXUS.

Autor: MASWOS V5 NEXUS
Versão: 5.1.1
"""

import sys
import asyncio
from datetime import datetime

# Importar modulos
from cross_mcp_protocol import (
    classify_and_route, 
    execute_workflow, 
    get_orchestrator,
    IntentType,
    MCPType
)
from handoff_protocol import (
    create_session, 
    execute_handoff, 
    get_full_context,
    get_handoff_manager
)
from integration_dashboard import (
    get_dashboard,
    IntegrationDashboard
)


def test_cross_mcp_classification():
    """Teste 1: Classificacao de intent"""
    print("\n" + "="*60)
    print("TEST 1: Cross-MCP Intent Classification")
    print("="*60)
    
    test_cases = [
        ("Preciso de uma petição inicial de ação de danos", "juridico"),
        ("Escreva um artigo científico sobre machine learning", "academic"),
        ("Crie uma API REST com autenticação JWT", "development"),
        ("Audite esta aplicação web para vulnerabilidades", "security")
    ]
    
    passed = 0
    for message, expected_intent in test_cases:
        result = classify_and_route(message)
        actual_intent = result["intent"]
        status = "PASS" if actual_intent == expected_intent else "FAIL"
        print(f"  [{status}] '{message[:40]}...'")
        print(f"         Expected: {expected_intent}, Got: {actual_intent}")
        if status == "PASS":
            passed += 1
    
    print(f"\n  Result: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_mcp_routing():
    """Teste 2: Roteamento para MCPs"""
    print("\n" + "="*60)
    print("TEST 2: MCP Routing")
    print("="*60)
    
    test_cases = [
        ("Preciso de uma petição", "maswos-juridico"),
        ("Escreva um artigo", "academic"),
        ("Crie uma API", "opencode")
    ]
    
    passed = 0
    for message, expected_mcp in test_cases:
        result = classify_and_route(message)
        actual_mcp = result["mcp"]
        status = "PASS" if actual_mcp == expected_mcp else "FAIL"
        print(f"  [{status}] {message[:30]}...")
        print(f"         Expected MCP: {expected_mcp}, Got: {actual_mcp}")
        if status == "PASS":
            passed += 1
    
    print(f"\n  Result: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_skill_mapping():
    """Teste 3: Mapeamento de skills"""
    print("\n" + "="*60)
    print("TEST 3: Skill Mapping")
    print("="*60)
    
    test_cases = [
        ("Preciso de uma petição", ["legal-agents", "juridico-workflow"]),
        ("Escreva um artigo", ["criador-de-artigo-v2", "academic-research"]),
        ("Crie uma API", ["api-patterns", "nodejs-best-practices"])
    ]
    
    passed = 0
    for message, expected_skills in test_cases:
        result = classify_and_route(message)
        actual_skills = result["skills"]
        
        # Verificar se pelo menos um skill esperado está presente
        has_match = any(s in actual_skills for s in expected_skills)
        status = "PASS" if has_match else "FAIL"
        print(f"  [{status}] {message[:30]}...")
        print(f"         Expected skills: {expected_skills}")
        print(f"         Got skills: {actual_skills}")
        if status == "PASS":
            passed += 1
    
    print(f"\n  Result: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_handoff_protocol():
    """Teste 4: Protocolo de handoff"""
    print("\n" + "="*60)
    print("TEST 4: Handoff Protocol")
    print("="*60)
    
    # Criar sessão
    session_id = create_session(
        original_request="Crie uma rede social",
        user_decisions=["tech=Vue 3", "design=youthful"],
        entities={"type": "webapp"}
    )
    print(f"  [+] Session created: {session_id[:8]}...")
    
    # Executar handoffs
    handoffs = [
        ("orchestrator", "project-planner", "Create PLAN.md"),
        ("project-planner", "frontend-specialist", "UI implementation"),
        ("project-planner", "backend-specialist", "API implementation")
    ]
    
    passed = len(handoffs)
    for from_a, to_a, action in handoffs:
        result = execute_handoff(
            session_id=session_id,
            from_agent=from_a,
            to_agent=to_a,
            action=action,
            result={"status": "completed"},
            quality_score=0.95
        )
        if result["status"] != "success":
            print(f"  [FAIL] Handoff {from_a} -> {to_a} failed")
            passed -= 1
        else:
            print(f"  [PASS] {from_a} -> {to_a}")
    
    # Verificar contexto final
    context = get_full_context(session_id)
    if context:
        print(f"\n  Context verification:")
        print(f"    - Handoff count: {context['handoff_count']}")
        print(f"    - Quality score: {context['quality_score']}")
        print(f"    - Audit trail: {len(context['audit_trail'])} entries")
    else:
        passed = 0
        print(f"  [FAIL] Context not found")
    
    print(f"\n  Result: {passed}/{len(handoffs)} tests passed")
    return passed == len(handoffs)


def test_dashboard():
    """Teste 5: Dashboard de integracao"""
    print("\n" + "="*60)
    print("TEST 5: Integration Dashboard")
    print("="*60)
    
    dashboard = get_dashboard()
    
    # Testar resumos
    mcp_summary = dashboard.get_mcp_summary()
    agent_summary = dashboard.get_agent_summary()
    skill_summary = dashboard.get_skill_summary()
    
    print(f"  [+] MCP Summary: {mcp_summary['active']} active, {mcp_summary['total']} total")
    print(f"  [+] Agent Summary: {agent_summary['total']} agents, {agent_summary['avg_success_rate']*100:.1f}% success")
    print(f"  [+] Skill Summary: {skill_summary['loaded']} loaded, {skill_summary['total_usages']} usages")
    
    # Testar JSON export
    json_output = dashboard.to_json()
    has_data = "maswos-juridico" in json_output
    print(f"  [+] JSON export: {'PASS' if has_data else 'FAIL'}")
    
    # Testar Markdown export
    md_output = dashboard.to_markdown()
    has_mcp_section = "## MCPs" in md_output
    print(f"  [+] Markdown export: {'PASS' if has_mcp_section else 'FAIL'}")
    
    result = has_data and has_mcp_section
    print(f"\n  Result: {'PASS' if result else 'FAIL'}")
    return result


def test_async_workflow():
    """Teste 6: Workflow assincrono"""
    print("\n" + "="*60)
    print("TEST 6: Async Workflow")
    print("="*60)
    
    async def run_test():
        result = await execute_workflow("Escreva um artigo sobre IA")
        return result["status"] == "completed"
    
    result = asyncio.run(run_test())
    print(f"  [{'PASS' if result else 'FAIL'}] Async workflow execution")
    print(f"\n  Result: {'PASS' if result else 'FAIL'}")
    return result


def test_error_handling():
    """Teste 7: tratamento de erros"""
    print("\n" + "="*60)
    print("TEST 7: Error Handling")
    print("="*60)
    
    # Testar sessão inexistente
    result = execute_handoff(
        session_id="inexistent-session-id",
        from_agent="agent1",
        to_agent="agent2",
        action="test"
    )
    error_handled = result["status"] == "error"
    print(f"  [{'PASS' if error_handled else 'FAIL'}] Handle non-existent session")
    
    # Testar contexto inválido
    invalid_context = get_full_context("inexistent-id")
    null_handled = invalid_context is None
    print(f"  [{'PASS' if null_handled else 'FAIL'}] Handle null context")
    
    result = error_handled and null_handled
    print(f"\n  Result: {'PASS' if result else 'FAIL'}")
    return result


def run_all_tests():
    """Executar todos os testes"""
    print("\n" + "#"*60)
    print("# INTEGRATION TEST SUITE - MASWOS V5 NEXUS")
    print("#"*60)
    print(f"Started at: {datetime.now().isoformat()}")
    
    tests = [
        ("Intent Classification", test_cross_mcp_classification),
        ("MCP Routing", test_mcp_routing),
        ("Skill Mapping", test_skill_mapping),
        ("Handoff Protocol", test_handoff_protocol),
        ("Dashboard", test_dashboard),
        ("Async Workflow", test_async_workflow),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n  [ERROR] {name}: {e}")
            results.append((name, False))
    
    # Resumo final
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")
    
    print(f"\n  Total: {passed_count}/{total_count} tests passed")
    print(f"  Completed at: {datetime.now().isoformat()}")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)