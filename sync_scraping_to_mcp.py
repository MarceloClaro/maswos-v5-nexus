#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Sync Scraping Agent to MCP
Sincronizar agente de scraping com MCP Jurídico

Arquitetura: Transformer-Agentes
"""

import json
from pathlib import Path
from datetime import datetime

def sync_scraping_to_mcp():
    """Sincronizar agente de scraping ao MCP Jurídico"""
    
    print("=" * 70)
    print("MASWOS V5 NEXUS - Sync Scraping Agent to MCP Jurídico")
    print("=" * 70)
    
    # 1. Atualizar configuração do MCP Jurídico
    config_file = Path("maswos-juridico-config.json")
    
    if not config_file.exists():
        print("[ERRO] Arquivo de configuração do MCP Jurídico não encontrado")
        return False
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 2. Adicionar agente de scraping integrado à camada Collection
    new_scraper_agent = {
        "id": "N12_integrated_scraper",
        "name": "Integrated Scraping Agent",
        "layer": "Collection",
        "description": "Agente de scraping granular e cirúrigico com fallback automático",
        "capabilities": [
            "advanced_scraping",
            "cache_management",
            "retry_with_backoff",
            "browser_headers_rotation",
            "ssl_bypass",
            "multi_source_fallback"
        ],
        "supported_sources": ["STF", "IBGE", "PUBMED", "Europe_PMC"],
        "transformer_mapping": "Multi-Head Attention",
        "fallback_enabled": True,
        "cache_ttl_hours": 24
    }
    
    # Verificar se já existe
    collection_agents = config.get("agents", {}).get("collection", [])
    existing_ids = [a.get("id") for a in collection_agents]
    
    if "N12_integrated_scraper" not in existing_ids:
        collection_agents.append(new_scraper_agent)
        config["agents"]["collection"] = collection_agents
        print("[OK] Agente de scraping integrado adicionado ao MCP Jurídico")
    else:
        print("[INFO] Agente de scraping já existe no MCP Jurídico")
    
    # 3. Atualizar scrapers existentes com fallback
    scraper_updates = {
        "N06": {
            "fallback_enabled": True,
            "fallback_agent": "N12_integrated_scraper",
            "techniques": ["api_alternative", "portal_search", "transparencia_search"]
        },
        "N09": {
            "fallback_enabled": True,
            "fallback_agent": "N12_integrated_scraper",
            "techniques": ["api_sidra", "api_localidades", "scraping_web"]
        }
    }
    
    for agent in collection_agents:
        agent_id = agent.get("id")
        if agent_id in scraper_updates:
            agent.update(scraper_updates[agent_id])
    
    # 4. AdicionarQuality Gate para scraping
    quality_gates = config.get("quality_gates", {})
    if "G1_scraping" not in quality_gates:
        quality_gates["G1_scraping"] = {
            "threshold": 0.70,
            "agents": ["N04-N12", "N12_integrated_scraper"],
            "description": "Quality gate para scraping e coleta de dados"
        }
        config["quality_gates"] = quality_gates
    
    # 5. Salvar configuração atualizada
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("[OK] Configuração do MCP Jurídico atualizada")
    
    # 6. Atualizar arquivo de sincronização
    sync_file = Path("mcp_sync_state_final.json")
    
    if sync_file.exists():
        with open(sync_file, 'r', encoding='utf-8') as f:
            sync_data = json.load(f)
        
        # Adicionar agente ao layer alignment
        layer_alignment = sync_data.get("layer_alignment", {})
        
        if "maswos_juridico" in layer_alignment:
            collection_layer = layer_alignment["maswos_juridico"].get("Collection", [])
            
            if "N12_integrated_scraper" not in collection_layer:
                collection_layer.append("N12_integrated_scraper")
                layer_alignment["maswos_juridico"]["Collection"] = collection_layer
                
                sync_data["layer_alignment"] = layer_alignment
                
                # Atualizar métricas
                sync_data["mcp_status"]["maswos-juridico"]["agents"] = 38  # +1
                
                with open(sync_file, 'w', encoding='utf-8') as f:
                    json.dump(sync_data, f, indent=2, ensure_ascii=False)
                
                print("[OK] Arquivo de sincronização atualizado")
    
    # 7. Criar relatório de sincronização
    report = {
        "timestamp": datetime.now().isoformat(),
        "action": "sync_scraping_to_mcp",
        "changes": [
            "Integrated Scraping Agent (N12_integrated_scraper) adicionado à camada Collection",
            "Fallback habilitado para scrapers N06 (STF) e N09 (IBGE)",
            "Quality Gate G1_scraping adicionado",
            "Layer alignment atualizado"
        ],
        "new_capabilities": [
            "advanced_scraping",
            "cache_management",
            "retry_with_backoff",
            "browser_headers_rotation",
            "ssl_bypass"
        ],
        "status": "SUCCESS"
    }
    
    report_file = Path("sync_scraping_report.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Relatório de sincronização salvo em: {report_file}")
    
    print("\n" + "=" * 70)
    print("SINCRONIZAÇÃO CONCLUÍDA")
    print("=" * 70)
    print("\nResumo:")
    print("  - Agente N12_integrated_scraper adicionado")
    print("  - Scrapers N06 e N09 atualizados com fallback")
    print("  - Quality Gate G1_scraping adicionado")
    print("  - Layer alignment atualizado")
    
    return True

if __name__ == "__main__":
    success = sync_scraping_to_mcp()
    exit(0 if success else 1)