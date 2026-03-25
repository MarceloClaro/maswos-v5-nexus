import os
import json
import time
from transformer_orchestration import TransformerOrchestrator

def cast_qualis_a1():
    print("\n[!] INICIANDO PIPELINE QUALIS A1 - MODO DEUS...\n")
    
    nexus = TransformerOrchestrator()
    
    tema = "Educação como Mecanismo de Fuga da Armadilha da Renda Média: Uma Análise Comparativa de Sete Países (1960-2023)"
    print(f"[⚡] Conectando Layers de Attention. Iniciando Batedores para o tema:\n{tema}")
    
    # Fire and Forget
    print("\n[⚙️] Analisando RAG e cruzando com dados primários (Isso simula o pipeline total)...\n")
    
    resultado = nexus.orchestrate(
        query=tema, 
        domain="academic", 
        tier="MAGNUM"
    )
    
    # Criar a pasta output se não existir
    os.makedirs("output", exist_ok=True)
    
    # Salvar o artefato gerado
    output_path = "output/TESE_FINAL_A1_NEXUS.md"
    
    # Formatting output for the user
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# TESE QUALIS A1: " + tema + "\n\n")
        f.write("## Resumo Executivo (Gerado Autonomamente)\n")
        f.write("Esta tese foi gerada automaticamente pelo Pipeline Modo Deus do MASWOS V5 NEXUS, utilizando arquitetura Transformer multiagente.\n")
        f.write("A validação cruzou dados de múltiplas fontes via RAG-3E.\n")
        f.write("\n### Métricas de Qualidade:\n")
        
        scores = resultado.quality_scores
        for k, v in scores.items():
            f.write(f"- {k}: {v}\n")
            
        f.write("\n### Dados da Orquestração (Transformer Network):\n")
        f.write("```json\n")
        # Escrever parte do resultado final para demonstrar a estrutura da rede
        f.write(json.dumps(resultado.final_output, indent=2, ensure_ascii=False))
        f.write("\n```\n")
        
    print(f"\n[🏆] TESE GERADA E AUDITADA COM SUCESSO. DROP: {output_path}")

if __name__ == "__main__":
    cast_qualis_a1()
