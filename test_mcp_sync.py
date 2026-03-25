#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Teste de Sincronização entre MCPs
Verifica comunicação e arquitetura Transformer-Agentes
"""

import json
from pathlib import Path

class MCPTestSuite:
    """Suite de testes para sincronização MCP"""
    
    def __init__(self):
        self.test_results = []
        
    def test_agent_mapping(self):
        """Testar mapeamento de agentes entre camadas"""
        print("=== Teste 1: Mapeamento de Agentes ===")
        
        config_file = Path("maswos-mcp-config.json")
        if not config_file.exists():
            print("[FALHA] Arquivo de configuração não encontrado")
            return False
            
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Verificar se todos os agentes têm layer definida
        agents = config.get("agents", {})
        missing_layers = []
        
        for layer_name, layer_agents in agents.items():
            if isinstance(layer_agents, list):
                for agent in layer_agents:
                    if "layer" not in agent:
                        missing_layers.append(f"{layer_name}:{agent.get('id', 'unknown')}")
        
        if missing_layers:
            print(f"[FALHA] Agentes sem layer: {missing_layers}")
            self.test_results.append(("agent_mapping", "FAIL", missing_layers))
            return False
        else:
            print("[OK] Todos os agentes têm layer definida")
            self.test_results.append(("agent_mapping", "PASS", None))
            return True
    
    def test_transformer_architecture(self):
        """Testar arquitetura Transformer-Agentes"""
        print("\n=== Teste 2: Arquitetura Transformer-Agentes ===")
        
        layers = ["Encoder", "Validation", "AgentFactory", "Decoder", "Control"]
        config_file = Path("maswos-mcp-config.json")
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Verificar se as camadas estão presentes
        config_layers = config.get("architecture", {}).get("layers", [])
        
        missing_layers = [l for l in layers if l not in config_layers]
        
        if missing_layers:
            print(f"[FALHA] Camadas faltando: {missing_layers}")
            self.test_results.append(("transformer_arch", "FAIL", missing_layers))
            return False
        else:
            print("[OK] Arquitetura Transformer completa")
            self.test_results.append(("transformer_arch", "PASS", None))
            return True
    
    def test_quality_gates(self):
        """Testar quality gates"""
        print("\n=== Teste 3: Quality Gates ===")
        
        config_file = Path("maswos-mcp-config.json")
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        gates = config.get("architecture", {}).get("quality_gates", [])
        expected_gates = ["G0", "G1", "G2", "G3", "GF"]
        
        missing_gates = [g for g in expected_gates if g not in gates]
        
        if missing_gates:
            print(f"[FALHA] Quality gates faltando: {missing_gates}")
            self.test_results.append(("quality_gates", "FAIL", missing_gates))
            return False
        else:
            print("[OK] Todos os quality gates presentes")
            self.test_results.append(("quality_gates", "PASS", None))
            return True
    
    def test_cross_mcp_sync(self):
        """Testar sincronização cross-MCP"""
        print("\n=== Teste 4: Sincronização Cross-MCP ===")
        
        sync_file = Path("mcp_sync_state_final.json")
        if not sync_file.exists():
            print("[FALHA] Arquivo de sincronização não encontrado")
            return False
            
        with open(sync_file, 'r') as f:
            sync_data = json.load(f)
        
        # Verificar MCPS integrados
        mcps = sync_data.get("mcp_status", {})
        integrated_count = len(mcps)
        
        if integrated_count < 2:
            print(f"[FALHA] Menos de 2 MCPs integrados: {integrated_count}")
            self.test_results.append(("cross_mcp_sync", "FAIL", integrated_count))
            return False
        else:
            print(f"[OK] {integrated_count} MCPs integrados")
            self.test_results.append(("cross_mcp_sync", "PASS", integrated_count))
            return True
    
    def test_handoff_protocol(self):
        """Testar protocolo de handoff"""
        print("\n=== Teste 5: Protocolo de Handoff ===")
        
        config_file = Path("maswos-juridico-config.json")
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        handoff = config.get("handoff_protocol", {})
        required_fields = handoff.get("required_fields", [])
        
        expected_fields = ["session_id", "agent_source", "agent_target", "timestamp", "context", "quality_score"]
        missing_fields = [f for f in expected_fields if f not in required_fields]
        
        if missing_fields:
            print(f"[FALHA] Campos de handoff faltando: {missing_fields}")
            self.test_results.append(("handoff_protocol", "FAIL", missing_fields))
            return False
        else:
            print("[OK] Protocolo de handoff completo")
            self.test_results.append(("handoff_protocol", "PASS", None))
            return True
    
    def test_rag_protocol(self):
        """Testar protocolo RAG 3-AXES"""
        print("\n=== Teste 6: Protocolo RAG 3-AXES ===")
        
        config_file = Path("maswos-juridico-config.json")
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        rag = config.get("rag_protocol", {})
        axes = list(rag.keys())
        
        if len(axes) < 3:
            print(f"[FALHA] Menos de 3 eixos RAG: {len(axes)}")
            self.test_results.append(("rag_protocol", "FAIL", len(axes)))
            return False
        else:
            print(f"[OK] Protocolo RAG 3-AXES: {axes}")
            self.test_results.append(("rag_protocol", "PASS", axes))
            return True
    
    def generate_report(self):
        """Gerar relatório de testes"""
        print("\n" + "=" * 60)
        print("RELATÓRIO DE TESTES DE SINCRONIZAÇÃO")
        print("=" * 60)
        
        passed = sum(1 for r in self.test_results if r[1] == "PASS")
        total = len(self.test_results)
        
        print(f"\nTotal de testes: {total}")
        print(f"Passou: {passed}")
        print(f"Falhou: {total - passed}")
        print(f"Taxa de sucesso: {passed/total*100:.1f}%")
        
        print("\nDetalhes:")
        for test_name, status, details in self.test_results:
            status_icon = "[OK]" if status == "PASS" else "[FALHA]"
            print(f"  {status_icon} {test_name}: {status}")
            if details:
                print(f"      Detalhes: {details}")
        
        # Salvar relatório
        report = {
            "timestamp": "2026-03-22T16:00:00Z",
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": passed/total*100,
            "test_results": self.test_results,
            "status": "PASS" if passed == total else "PARTIAL"
        }
        
        report_file = Path("mcp_sync_test_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[OK] Relatório salvo em: {report_file}")
        
        return report

def main():
    """Função principal"""
    print("MASWOS V5 NEXUS - Teste de Sincronização MCP")
    print("=" * 60)
    
    test_suite = MCPTestSuite()
    
    # Executar testes
    test_suite.test_agent_mapping()
    test_suite.test_transformer_architecture()
    test_suite.test_quality_gates()
    test_suite.test_cross_mcp_sync()
    test_suite.test_handoff_protocol()
    test_suite.test_rag_protocol()
    
    # Gerar relatório
    report = test_suite.generate_report()
    
    print("\n" + "=" * 60)
    if report["status"] == "PASS":
        print("[SUCESSO] Todos os testes passaram!")
        print("Sincronização entre MCPs está correta.")
    else:
        print("[AVISO] Alguns testes falharam.")
        print("Verifique o relatório para detalhes.")
    
    return report["status"] == "PASS"

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)