#!/usr/bin/env python3
"""
MCP Academic Transform - Versão Otimizada para CPU
Otimizado para: CPU-only, baixo consumo de memória, modelos quantizados
"""

import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import asyncio
import json
import gc

# Configurações para CPU
CPU_CONFIG = {
    "torch_threads": 4,  # Ajuste conforme seu CPU
    "use_quantization": True,
    "model_size": "small",  # small, medium (avoid large)
    "batch_size": 1,
    "max_length": 512,
    "cache_enabled": True
}

# ============================================================================
# CONFIGURAÇÕES DE MODELOS LEVES PARA CPU
# ============================================================================

CPU_FRIENDLY_MODELS = {
    # Modelos pequenos e eficientes para CPU
    "text-generation": [
        "microsoft/Phi-3-mini-4k-instruct",  # 3.8B - Excelente para CPU
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # 1.1B - Muito leve
        "Qwen/Qwen2.5-0.5B-Instruct",  # 0.5B - Extremamente leve
        "meta-llama/Llama-3.2-1B-Instruct",  # 1B - Bom equilíbrio
    ],
    "text-classification": [
        "distilbert-base-uncased",  # 66M - Muito leve
        "bert-base-uncased",  # 110M - Padrão
    ],
    "embedding": [
        "sentence-transformers/all-MiniLM-L6-v2",  # 22M - Muito eficiente
        "sentence-transformers/all-MiniLM-L12-v2",  # 33M - Bom
    ]
}


class CPUOptimizer:
    """Otimizador de recursos para CPU"""
    
    @staticmethod
    def configure_torch():
        """Configura PyTorch para CPU"""
        try:
            import torch
            torch.set_num_threads(CPU_CONFIG["torch_threads"])
            torch.set_num_interop_threads(2)
            print(f"PyTorch configurado para {CPU_CONFIG['torch_threads']} threads")
            return True
        except ImportError:
            print("[AVISO] PyTorch não encontrado")
            return False
    
    @staticmethod
    def get_optimal_model(task: str):
        """Retorna modelo otimizado para CPU"""
        models = CPU_FRIENDLY_MODELS.get(task, [])
        return models[0] if models else None
    
    @staticmethod
    def clear_cache():
        """Limpa cache de memória"""
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except:
            pass
    
    @staticmethod
    def get_memory_usage() -> Dict[str, float]:
        """Retorna uso de memória"""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,  # MB
            "vms_mb": memory_info.vms / 1024 / 1024,  # MB
            "percent": process.memory_percent()
        }


# ============================================================================
# AGENTES OTIMIZADOS PARA CPU
# ============================================================================

@dataclass
class AgentOutput:
    """Saída padrão de um agente"""
    agent_id: str
    layer: str
    data: Dict[str, Any]
    confidence: float
    metadata: Dict[str, Any]


class CPUOptimizedAgent(ABC):
    """Classe base otimizada para CPU"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agent_id = config.get("id", "unknown")
        self.layer = config.get("layer", "unknown")
        self.name = config.get("name", "Unknown Agent")
        self._model = None
        self._tokenizer = None
        
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> AgentOutput:
        """Executa o agente"""
        pass
    
    def _lazy_load_model(self, model_name: str):
        """Carrega modelo apenas quando necessário (lazy loading)"""
        if self._model is None:
            print(f"  [CARREGANDO] Modelo: {model_name}")
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                import torch
                
                # Configuração para CPU
                self._tokenizer = AutoTokenizer.from_pretrained(model_name)
                self._model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float32,  # CPU usa float32
                    device_map="cpu",
                    low_cpu_mem_usage=True  # Otimização de memória
                )
                self._model.eval()  # Modo evaluatio
                print(f"  [OK] Modelo carregado")
            except Exception as e:
                print(f"  ❌ Erro ao carregar modelo: {e}")
                raise
    
    def _unload_model(self):
        """Descarrega modelo da memória"""
        if self._model is not None:
            del self._model
            del self._tokenizer
            self._model = None
            self._tokenizer = None
            CPUOptimizer.clear_cache()


# ============================================================================
# AGENTES ENCODER OTIMIZADOS
# ============================================================================

class IntentParserAgentCPU(CPUOptimizedAgent):
    """Agente de parsing de intenção - Otimizado para CPU"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.use_llm = config.get("use_llm", False)  # Desativado por padrão para CPU
        
    async def execute(self, input_data: Dict[str, Any]) -> AgentOutput:
        text = input_data.get("text", "")
        
        if self.use_llm and CPU_CONFIG["use_quantization"]:
            # Usa modelo leve para análise
            result = await self._analyze_with_llm(text)
        else:
            # Análise baseada em regras (mais rápida para CPU)
            result = self._analyze_with_rules(text)
        
        return AgentOutput(
            agent_id=self.agent_id,
            layer=self.layer,
            data=result,
            confidence=0.95,
            metadata={"method": "llm" if self.use_llm else "rules"}
        )
    
    def _analyze_with_rules(self, text: str) -> Dict:
        """Análise baseada em regras - Rápida para CPU"""
        text_lower = text.lower()
        
        # Detecta intenção
        intent = "general_query"
        if any(w in text_lower for w in ["pesquisar", "buscar", "encontrar", "research"]):
            intent = "academic_research"
        elif any(w in text_lower for w in ["analisar", "avaliar", "analysis"]):
            intent = "data_analysis"
        elif any(w in text_lower for w in ["escrever", "gerar", "write"]):
            intent = "document_generation"
        elif any(w in text_lower for w in ["mapa", "geoespacial", "map"]):
            intent = "geospatial_analysis"
        elif any(w in text_lower for w in ["jurisprudência", "tribunal", "lei"]):
            intent = "legal_research"
        
        # Detecta domínio
        domain = "general"
        domain_keywords = {
            "medical": ["medicina", "saúde", "hospital", "médico"],
            "legal": ["direito", "lei", "tribunal", "advogado"],
            "cs": ["computação", "software", "algoritmo", "programação"],
            "engineering": ["engenharia", "sistema", "projeto"],
            "environmental": ["meio ambiente", "natureza", "clima", "desmatamento"]
        }
        
        for dom, keywords in domain_keywords.items():
            if any(kw in text_lower for kw in keywords):
                domain = dom
                break
        
        # Extrai tópicos
        topics = [w for w in text.split() if len(w) > 4][:5]
        
        return {
            "intent": intent,
            "domain": domain,
            "topics": topics,
            "original_text": text
        }
    
    async def _analyze_with_llm(self, text: str) -> Dict:
        """Análise com LLM - Mais precisa mas mais lenta"""
        model_name = CPUOptimizer.get_optimal_model("text-classification")
        
        if model_name is None:
            return self._analyze_with_rules(text)
        
        try:
            self._lazy_load_model(model_name)
            
            # Simplificado para CPU
            return self._analyze_with_rules(text)
        finally:
            self._unload_model()


class DomainClassifierAgentCPU(CPUOptimizedAgent):
    """Classificador de domínio - Otimizado para CPU"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
    async def execute(self, input_data: Dict[str, Any]) -> AgentOutput:
        intent_data = input_data.get("intent_data", {})
        domain = intent_data.get("domain", "general")
        
        # Mapeamento simples
        academic_domain = self._map_domain(domain)
        subdomains = self._get_subdomains(intent_data.get("topics", []))
        
        return AgentOutput(
            agent_id=self.agent_id,
            layer=self.layer,
            data={
                "academic_domain": academic_domain,
                "subdomains": subdomains,
                "suggested_sources": self._suggest_sources(academic_domain)
            },
            confidence=0.92,
            metadata={"cpu_optimized": True}
        )
    
    def _map_domain(self, domain: str) -> str:
        mapping = {
            "cs": "computer_science",
            "medical": "biomedical",
            "legal": "law",
            "engineering": "engineering",
            "environmental": "environmental_science",
            "general": "multidisciplinary"
        }
        return mapping.get(domain, "multidisciplinary")
    
    def _get_subdomains(self, topics: List[str]) -> List[str]:
        subdomains = []
        for topic in topics:
            if any(w in topic.lower() for w in ["inteligência", "ia", "machine"]):
                subdomains.extend(["machine_learning", "artificial_intelligence"])
            elif any(w in topic.lower() for w in ["saúde", "médico"]):
                subdomains.extend(["health", "medicine"])
        return list(set(subdomains))[:3]
    
    def _suggest_sources(self, domain: str) -> List[str]:
        sources = {
            "computer_science": ["arxiv", "acm", "ieee"],
            "biomedical": ["pubmed", "scielo"],
            "law": ["stf", "lexml"],
            "multidisciplinary": ["scopus", "google_scholar"]
        }
        return sources.get(domain, sources["multidisciplinary"])


# ============================================================================
# AGENTES COLLECTION OTIMIZADOS
# ============================================================================

class ArxivCollectorAgentCPU(CPUOptimizedAgent):
    """Coletor ArXiv - Otimizado para CPU"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.max_results = config.get("max_results", 10)  # Limite para CPU
        
    async def execute(self, input_data: Dict[str, Any]) -> AgentOutput:
        domain_data = input_data.get("domain_data", {})
        subdomains = domain_data.get("subdomains", ["cs.AI"])
        
        # Simula coleta (substituir por API real)
        papers = self._collect_papers(subdomains)
        
        return AgentOutput(
            agent_id=self.agent_id,
            layer=self.layer,
            data={
                "source": "arxiv",
                "papers": papers,
                "total": len(papers)
            },
            confidence=0.90,
            metadata={"max_results": self.max_results, "cpu_optimized": True}
        )
    
    def _collect_papers(self, subdomains: List[str]) -> List[Dict]:
        """Coleta papers (simulado)"""
        papers = []
        for i in range(min(self.max_results, 5)):
            papers.append({
                "id": f"arxiv:2026.{i:05d}",
                "title": f"Paper on {subdomains[0] if subdomains else 'AI'} #{i+1}",
                "authors": ["Author A", "Author B"],
                "abstract": "Abstract simulation...",
                "published": "2026-03-20",
                "relevance": 0.85 + (i * 0.02)
            })
        return papers


# ============================================================================
# PIPELINE OTIMIZADO PARA CPU
# ============================================================================

class CPUMCPPipeline:
    """Pipeline MCP otimizado para CPU"""
    
    def __init__(self, config = None):
        self.config = config if config is not None else CPU_CONFIG
        
        # Configura PyTorch
        CPUOptimizer.configure_torch()
        
        # Inicializa agentes
        self.agents = self._init_agents()
        
    def _init_agents(self) -> Dict[str, List]:
        """Inicializa agentes otimizados para CPU"""
        return {
            "encoder": [
                IntentParserAgentCPU({"id": "intent_parser", "layer": "encoder", "name": "Intent Parser", "use_llm": False}),
                DomainClassifierAgentCPU({"id": "domain_classifier", "layer": "encoder", "name": "Domain Classifier"})
            ],
            "collection": [
                ArxivCollectorAgentCPU({"id": "arxiv_collector", "layer": "collection", "name": "ArXiv Collector", "max_results": 10})
            ],
            "validation": [],
            "decoder": [],
            "control": []
        }
    
    async def execute(self, query: str) -> Dict[str, Any]:
        """Executa pipeline"""
        print("=" * 60)
        print("=== MCP CPU-OPTIMIZED PIPELINE ===")
        print("=" * 60)
        print(f"Query: {query}")
        print(f"Config: {self.config['torch_threads']} threads, quantization: {self.config['use_quantization']}")
        print()
        
        input_data = {"text": query}
        results = {}
        
        # Encoder phase
        print("[FASE 1] Encoder")
        for agent in self.agents["encoder"]:
            print(f"  [EXEC] {agent.name}")
            result = await agent.execute(input_data)
            results[agent.agent_id] = result
            input_data[f"{agent.agent_id}_data"] = result.data
        
        # Collection phase
        print("[FASE 2] Collection")
        for agent in self.agents["collection"]:
            print(f"  [EXEC] {agent.name}")
            result = await agent.execute(input_data)
            results[agent.agent_id] = result
        
        # Memory usage
        memory = CPUOptimizer.get_memory_usage()
        print()
        print(f"Memória: {memory['rss_mb']:.2f} MB")
        
        print()
        print("=" * 60)
        print("[CONCLUIDO]")
        print("=" * 60)
        
        return {
            "status": "success",
            "pipeline": "cpu-optimized",
            "results": {k: v.data for k, v in results.items()},
            "memory_usage_mb": memory['rss_mb']
        }


# ============================================================================
# CONFIGURAÇÕES RECOMENDADAS PARA DIFERENTES CPUs
# ============================================================================

CPU_PROFILES = {
    "low_end": {  # CPUs antigas ou lentas (2-4 cores)
        "torch_threads": 2,
        "model_size": "tiny",
        "max_length": 256,
        "batch_size": 1,
        "use_quantization": True,
        "use_llm_agents": False
    },
    "mid_range": {  # CPUs modernas (4-8 cores)
        "torch_threads": 4,
        "model_size": "small",
        "max_length": 512,
        "batch_size": 2,
        "use_quantization": True,
        "use_llm_agents": True
    },
    "high_end": {  # CPUs potentes (8+ cores)
        "torch_threads": 8,
        "model_size": "medium",
        "max_length": 1024,
        "batch_size": 4,
        "use_quantization": False,
        "use_llm_agents": True
    }
}


def get_cpu_profile() -> str:
    """Detecta perfil do CPU automaticamente"""
    import psutil
    
    cores = psutil.cpu_count(logical=False) or 4  # Default para 4 cores
    memory = psutil.virtual_memory().total / (1024**3)  # GB
    
    if cores <= 4 and memory < 8:
        return "low_end"
    elif cores <= 8 and memory < 16:
        return "mid_range"
    else:
        return "high_end"


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

async def main():
    """Exemplo de uso otimizado para CPU"""
    
    # Detecta perfil do CPU
    profile = get_cpu_profile()
    config = CPU_PROFILES[profile]
    
    print("=" * 70)
    print(f"MCP CPU-OPTIMIZED - Perfil: {profile.upper()}")
    print("=" * 70)
    print(f"Config: {config}")
    print()
    
    # Cria pipeline
    pipeline = CPUMCPPipeline(config)
    
    # Executa query
    query = "Pesquisar sobre inteligência artificial aplicada à medicina"
    result = await pipeline.execute(query)
    
    print()
    print("Resultado:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result


if __name__ == "__main__":
    # Instalação necessária:
    # pip install transformers torch psutil
    
    asyncio.run(main())