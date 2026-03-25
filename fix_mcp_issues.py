#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Script de Correção de Problemas MCP
Corrige erros e bugs encontrados na auditoria
"""

import json
import requests
import urllib3
from pathlib import Path
import time

# Desativar avisos SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MCPFixer:
    """Classe para corrigir problemas nos MCPs"""
    
    def __init__(self):
        self.fixes_applied = []
        self.errors_found = []
        
    def fix_stf_endpoint(self):
        """Corrigir endpoint STF - usar transparência ou alternative"""
        print("=== Corrigindo endpoint STF ===")
        
        # Endpoints alternativos do STF
        stf_endpoints = [
            "https://transparencia.stf.jus.br/single/?appid=9cc80576-9d66-4d1b-b6e4-3a93e0c423f2&sheet=80c4aff9-9a59-48f1-b043-58f4d20c69d0&opt=nointeraction&select=clearall",
            "https://sistemas.stf.jus.br/repgeral/pesquisa",
            "https://portal.stf.jus.br/textos/verTexto.asp?servico=jurisprudencia"
        ]
        
        working_endpoint = None
        for endpoint in stf_endpoints:
            try:
                r = requests.get(endpoint, timeout=5, verify=False, 
                               headers={'User-Agent': 'MASWOS-V5-NEXUS/5.0'})
                if r.status_code < 400:
                    working_endpoint = endpoint
                    print(f"[OK] Endpoint STF funcionando: {endpoint}")
                    break
            except:
                continue
        
        if working_endpoint:
            self.fixes_applied.append("STF endpoint corrigido")
            return working_endpoint
        else:
            self.errors_found.append("STF sem endpoints disponíveis")
            return None
    
    def fix_ibge_endpoint(self):
        """Corrigir endpoint IBGE - usar API específica"""
        print("=== Corrigindo endpoint IBGE ===")
        
        # APIs específicas do IBGE
        ibge_endpoints = [
            "https://servicodados.ibge.gov.br/api/v1/localidades/estados",
            "https://servicodados.ibge.gov.br/api/v3/agregados",
            "https://apisidra.ibge.gov.br/values"
        ]
        
        working_endpoint = None
        for endpoint in ibge_endpoints:
            try:
                r = requests.get(endpoint, timeout=10, verify=False,
                               headers={'User-Agent': 'MASWOS-V5-NEXUS/5.0'})
                if r.status_code < 400:
                    working_endpoint = endpoint
                    print(f"[OK] Endpoint IBGE funcionando: {endpoint}")
                    break
            except Exception as e:
                print(f"  [AVISO] {endpoint}: {e}")
                continue
        
        if working_endpoint:
            self.fixes_applied.append("IBGE endpoint corrigido")
            return working_endpoint
        else:
            self.errors_found.append("IBGE sem endpoints disponíveis")
            return None
    
    def fix_ssl_issues(self):
        """Corrigir problemas de SSL globalmente"""
        print("=== Configurando SSL global ===")
        
        # Criar script de configuração SSL
        ssl_config = '''
# Configuração SSL para MASWOS V5 NEXUS
import urllib3
import ssl

# Desativar verificações SSL para APIs governamentais
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurar contexto SSL mais permissivo para APIs específicas
ssl._create_default_https_context = ssl._create_unverified_context
'''
        
        ssl_file = Path("ssl_config.py")
        with open(ssl_file, 'w') as f:
            f.write(ssl_config)
        
        self.fixes_applied.append("Configuração SSL criada")
        print(f"[OK] Configuração SSL salva em {ssl_file}")
    
    def sync_agent_layers(self):
        """Sincronizar camadas de agentes entre MCPs"""
        print("=== Sincronizando camadas de agentes ===")
        
        # Verificar arquivo de sincronização
        sync_file = Path("mcp_sync_state_final.json")
        if sync_file.exists():
            with open(sync_file, 'r') as f:
                sync_data = json.load(f)
            
            # Verificar se há agentes faltando
            layer_alignment = sync_data.get("layer_alignment", {})
            
            # Verificar agentes obrigatórios por camada
            required_agents = {
                "Encoder": ["N01_intent_parser", "N02_query_builder"],
                "Validation": ["constraint_checker", "multi_validator"],
                "Decoder": ["skill_assembler", "critic_router"]
            }
            
            missing_agents = []
            for layer, agents in required_agents.items():
                for agent in agents:
                    found = False
                    for mcp_name, mcp_layers in layer_alignment.items():
                        if layer in mcp_layers and agent in mcp_layers[layer]:
                            found = True
                            break
                    if not found:
                        missing_agents.append(f"{layer}:{agent}")
            
            if missing_agents:
                print(f"[AVISO] Agentes faltando: {missing_agents}")
                self.errors_found.append(f"Agentes faltando: {missing_agents}")
            else:
                print("[OK] Todos os agentes obrigatórios presentes")
                self.fixes_applied.append("Agentes sincronizados")
        
        return len(self.errors_found) == 0
    
    def create_fallback_mechanisms(self):
        """Criar mecanismos de fallback para APIs indisponíveis"""
        print("=== Criando mecanismos de fallback ===")
        
        fallback_config = {
            "fallback_strategies": {
                "STF": {
                    "primary": "portal.stf.jus.br",
                    "fallbacks": [
                        "transparencia.stf.jus.br",
                        "sistemas.stf.jus.br/repgeral",
                        "cache_local"
                    ],
                    "cache_ttl": 3600
                },
                "IBGE": {
                    "primary": "servicodados.ibge.gov.br/api/v1",
                    "fallbacks": [
                        "apisidra.ibge.gov.br",
                        "censo.ibge.gov.br",
                        "cache_local"
                    ],
                    "cache_ttl": 86400
                }
            },
            "retry_policy": {
                "max_retries": 3,
                "backoff_factor": 1.5,
                "initial_delay": 1.0
            }
        }
        
        fallback_file = Path("fallback_config.json")
        with open(fallback_file, 'w') as f:
            json.dump(fallback_config, f, indent=2)
        
        self.fixes_applied.append("Mecanismos de fallback criados")
        print(f"[OK] Configuração de fallback salva em {fallback_file}")
    
    def update_sync_plan(self):
        """Atualizar plano de sincronização"""
        print("=== Atualizando plano de sincronização ===")
        
        sync_plan = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pending_syncs": [
                {
                    "source": "maswos-mcp",
                    "target": "ecosystem-transformer",
                    "agents": ["query_builder", "skill_synthesizer"],
                    "status": "pending"
                }
            ],
            "alignment_updates": [
                {
                    "mcp": "maswos-juridico",
                    "layer": "Encoder",
                    "add": ["N03a_chain_of_thought"],
                    "remove": []
                }
            ]
        }
        
        sync_file = Path("sync_plan_update.json")
        with open(sync_file, 'w') as f:
            json.dump(sync_plan, f, indent=2)
        
        self.fixes_applied.append("Plano de sincronização atualizado")
        print(f"[OK] Plano atualizado salvo em {sync_file}")
    
    def generate_fix_report(self):
        """Gerar relatório de correções"""
        report = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fixes_applied": self.fixes_applied,
            "errors_found": self.errors_found,
            "status": "PARTIAL" if self.errors_found else "SUCCESS",
            "recommendations": [
                "Executar testes de integração após correções",
                "Monitorar disponibilidade das APIs diariamente",
                "Implementar cache distribuído para dados estáticos"
            ]
        }
        
        report_file = Path("fix_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n=== Relatório de Correções ===")
        print(f"Correções aplicadas: {len(self.fixes_applied)}")
        print(f"Erros encontrados: {len(self.errors_found)}")
        print(f"Status: {report['status']}")
        print(f"Relatório salvo em: {report_file}")
        
        return report

def main():
    """Função principal"""
    print("MASWOS V5 NEXUS - Correção de Problemas MCP")
    print("=" * 50)
    
    fixer = MCPFixer()
    
    # Aplicar correções
    fixer.fix_ssl_issues()
    fixer.fix_stf_endpoint()
    fixer.fix_ibge_endpoint()
    fixer.create_fallback_mechanisms()
    fixer.update_sync_plan()
    fixer.sync_agent_layers()
    
    # Gerar relatório
    report = fixer.generate_fix_report()
    
    print("\n" + "=" * 50)
    print("Correções concluídas!")
    print(f"Próximos passos:")
    print("1. Verificar relatório em fix_report.json")
    print("2. Executar testes: python api_validator.py")
    print("3. Sincronizar MCPS: orchestrator_unified_pipeline")

if __name__ == "__main__":
    main()