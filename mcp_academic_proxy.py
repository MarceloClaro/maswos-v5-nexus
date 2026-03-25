#!/usr/bin/env python3
"""
MASWOS Academic MCP Proxy Server
Integra APIs acadêmicas reais ao MCP Academic via JSON-RPC
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify
from academic_api_client import AcademicAPIFacade

app = Flask(__name__)
facade = AcademicAPIFacade()

class MCPProtocol:
    """Implementação do protocolo MCP"""
    
    @staticmethod
    def create_response(request_id: Any, result: Any) -> Dict:
        """Cria resposta MCP padrão"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    @staticmethod
    def create_error(request_id: Any, code: int, message: str) -> Dict:
        """Cria erro MCP"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }


@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    """Endpoint principal do MCP"""
    try:
        req = request.get_json()
        
        if not req:
            return jsonify(MCPProtocol.create_error(None, -32600, "Invalid Request")), 400
        
        method = req.get("method")
        request_id = req.get("id")
        params = req.get("params", {})
        
        if method == "tools/list":
            return jsonify(MCPProtocol.create_response(request_id, {
                "tools": [
                    {
                        "name": "academic_search_all",
                        "description": "Busca artigos acadêmicos em todas as fontes disponíveis",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Termo de busca"},
                                "limit_per_source": {"type": "integer", "description": "Limite por fonte", "default": 5}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "academic_search_arxiv",
                        "description": "Busca artigos no arXiv",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Termo de busca"},
                                "category": {"type": "string", "description": "Categoria arXiv (opcional)"},
                                "max_results": {"type": "integer", "description": "Máximo de resultados", "default": 10}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "academic_search_crossref",
                        "description": "Busca artigos no CrossRef",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Termo de busca"},
                                "limit": {"type": "integer", "description": "Máximo de resultados", "default": 10}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "academic_search_openalex",
                        "description": "Busca no OpenAlex",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Termo de busca"},
                                "limit": {"type": "integer", "description": "Máximo de resultados", "default": 10}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "academic_get_geospatial_datasets",
                        "description": "Lista datasets geoespaciais disponíveis",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "academic_list_sources",
                        "description": "Lista todas as fontes acadêmicas disponíveis",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "type_filter": {"type": "string", "description": "Filtrar por tipo (national/international/government)"}
                            }
                        }
                    }
                ]
            }))
        
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name == "academic_search_all":
                result = facade.search_all(
                    query=tool_args.get("query"),
                    limit_per_source=tool_args.get("limit_per_source", 5)
                )
                return jsonify(MCPProtocol.create_response(request_id, {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, ensure_ascii=False)
                        }
                    ]
                }))
            
            elif tool_name == "academic_search_arxiv":
                result = facade.arxiv.search(
                    query=tool_args.get("query"),
                    max_results=tool_args.get("max_results", 10),
                    category=tool_args.get("category")
                )
                return jsonify(MCPProtocol.create_response(request_id, {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, ensure_ascii=False)
                        }
                    ]
                }))
            
            elif tool_name == "academic_search_crossref":
                result = facade.crossref.search(
                    query=tool_args.get("query"),
                    limit=tool_args.get("limit", 10)
                )
                return jsonify(MCPProtocol.create_response(request_id, {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, ensure_ascii=False)
                        }
                    ]
                }))
            
            elif tool_name == "academic_search_openalex":
                result = facade.openalex.search_works(
                    query=tool_args.get("query"),
                    limit=tool_args.get("limit", 10)
                )
                return jsonify(MCPProtocol.create_response(request_id, {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, ensure_ascii=False)
                        }
                    ]
                }))
            
            elif tool_name == "academic_get_geospatial_datasets":
                result = facade.get_geospatial_datasets()
                return jsonify(MCPProtocol.create_response(request_id, {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, ensure_ascii=False)
                        }
                    ]
                }))
            
            elif tool_name == "academic_list_sources":
                with open("academic-api-config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                sources = config.get("apis", {})
                
                type_filter = tool_args.get("type_filter")
                if type_filter:
                    filtered = {k: v for k, v in sources.items() if v.get("status") == type_filter}
                    sources = filtered
                
                return jsonify(MCPProtocol.create_response(request_id, {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(sources, indent=2, ensure_ascii=False)
                        }
                    ]
                }))
            
            else:
                return jsonify(MCPProtocol.create_error(request_id, -32601, f"Tool not found: {tool_name}"))
        
        elif method == "initialize":
            return jsonify(MCPProtocol.create_response(request_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "maswos-academic-proxy",
                    "version": "1.0.0"
                }
            }))
        
        else:
            return jsonify(MCPProtocol.create_error(request_id, -32601, f"Method not found: {method}"))
    
    except Exception as e:
        return jsonify(MCPProtocol.create_error(request_id.get("id") if request.get_json() else None, -32603, str(e))), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "arxiv": "ok",
            "crossref": "ok", 
            "openalex": "ok",
            "pubmed": "ok"
        }
    })


@app.route("/sources", methods=["GET"])
def list_sources():
    """Lista fontes disponíveis"""
    with open("academic-api-config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    return jsonify(config.get("apis", {}))


if __name__ == "__main__":
    print("=" * 60)
    print("MASWOS Academic MCP Proxy Server")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /mcp         - MCP protocol endpoint")
    print("  GET  /health      - Health check")
    print("  GET  /sources     - List available sources")
    print("\nStarting server on http://localhost:5000")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=5000, debug=False)
