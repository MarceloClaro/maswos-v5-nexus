"""
QUALIS A1 Academic Validator
==============================
Validator para verificar se a tese atende aos padrões QUALIS A1.

Autor: MASWOS V5 NEXUS
Versão: 5.1.0
"""

import os
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Resultado da validação"""
    passed: bool
    score: float
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class QualisA1Validator:
    """
    Validador para padrões QUALIS A1 em produção acadêmica.
    
    Critérios de avaliação:
    - Estrutura IMRAD completa
    - Citações conforme ABNT
    - Fundamentação teórica sólida
    - Metodologia apropriada
    - Resultados verificáveis
    - Discussão crítica
    - Referências de alto impacto
    """
    
    def __init__(self, thesis_path: str):
        self.thesis_path = thesis_path
        self.chapters = {}
        self.references = []
        self.issues = []
        self.score = 10.0
        
    def load_chapters(self) -> bool:
        """Carregar todos os capítulos da tese"""
        chapter_files = [
            "CAPITULO_01_COMPLETO.md",
            "CAPITULO_02_COMPLETO.md", 
            "CAPITULO_03_COMPLETO.md",
            "CAPITULO_04_COMPLETO.md",
            "CAPITULO_05_06_COMPLETO.md"
        ]
        
        for chap_file in chapter_files:
            path = os.path.join(self.thesis_path, chap_file)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    self.chapters[chap_file] = f.read()
        
        return len(self.chapters) > 0
    
    def load_references(self) -> bool:
        """Carregar referências"""
        ref_path = os.path.join(self.thesis_path, "REFERENCIAS_AUDITADAS.md")
        if os.path.exists(ref_path):
            with open(ref_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extrair referências
                self.references = self._parse_references(content)
        return len(self.references) > 0
    
    def _parse_references(self, content: str) -> List[str]:
        """Parse de referências em formato ABNT"""
        # Extrair linhas com referências (começam com ** ou são URLs)
        refs = []
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('**') and 'DOI:' in line:
                refs.append(line.strip())
            elif 'http' in line and 'doi.org' in line:
                refs.append(line.strip())
        return refs
    
    def validate_structure(self) -> ValidationResult:
        """Validar estrutura IMRAD"""
        issues = []
        score = 10.0
        
        required_sections = {
            "CAPITULO_01_COMPLETO.md": ["INTRODUÇÃO", "Contextualização"],
            "CAPITULO_02_COMPLETO.md": ["FUNDAMENTOS", "REVISÃO"],
            "CAPITULO_03_COMPLETO.md": ["METODOLOGIA", "Métodos"],
            "CAPITULO_04_COMPLETO.md": ["RESULTADOS", "Análise"],
            "CAPITULO_05_06_COMPLETO.md": ["DISCUSSÃO", "CONCLUSÃO"]
        }
        
        for chap, required in required_sections.items():
            if chap not in self.chapters:
                issues.append(f"Capítulo ausente: {chap}")
                score -= 0.5
            else:
                content = self.chapters[chap].upper()
                for section in required:
                    if section.upper() not in content:
                        issues.append(f"Seção ausente em {chap}: {section}")
                        score -= 0.2
        
        return ValidationResult(
            passed=score >= 8.0,
            score=max(0, score),
            issues=issues
        )
    
    def validate_citations(self) -> ValidationResult:
        """Validar formato de citações ABNT"""
        issues = []
        score = 10.0
        
        # Verificar presença de notas de rodapé com citação - formato correto
        footnote_patterns = [
            r'\d+\s+NOTA DE RODAPÉ',
            r'\*\d+\s+NOTA DE RODAPÉ',
            r'NOTA DE RODAPÉ\s*-\s*CITAÇÃO'
        ]
        
        for chap_name, content in self.chapters.items():
            # Contar notas de rodapé com qualquer dos padrões
            found = False
            for pattern in footnote_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if len(matches) >= 3:
                    found = True
                    break
            
            if not found:
                issues.append(f"{chap_name}: Poucas notas de rodape (verificacao manual necessaria)")
                score -= 0.1
            
            # Verificar formato de citação (Autor, Ano, página) - mais flexivel
            inline_citations = len(re.findall(r'\([A-Z][a-z]+.*\d{4}.*\)', content))
            # Tambem procurar citepos
            if inline_citations < 3:
                # Verificar se tem citacoes no formato [1] ou类似
                bracket_cites = len(re.findall(r'\[\d+\]', content))
                inline_citations += bracket_cites
            
            if inline_citations < 3:
                issues.append(f"{chap_name}: Poucas citacoes detectadas")
                score -= 0.1
        
        return ValidationResult(
            passed=score >= 7.0,
            score=max(0, score),
            issues=issues
        )
    
    def validate_references(self) -> ValidationResult:
        """Validar referências bibliográficas"""
        issues = []
        score = 10.0
        
        if len(self.references) < 30:
            issues.append(f"Poucas referências ({len(self.references)}, mínimo 30)")
            score -= 0.5 * (30 - len(self.references))
        
        # Verificar presença de DOI
        dois = [r for r in self.references if 'DOI' in r or 'doi.org' in r]
        if len(dois) < len(self.references) * 0.5:
            issues.append(f"Muitas referências sem DOI: {len(self.references) - len(dois)}")
            score -= 0.3
        
        return ValidationResult(
            passed=score >= 7.0,
            score=max(0, score),
            issues=issues
        )
    
    def validate_methodology(self) -> ValidationResult:
        """Validar metodologia"""
        issues = []
        score = 10.0
        
        if "CAPITULO_03_COMPLETO.md" in self.chapters:
            content = self.chapters["CAPITULO_03_COMPLETO.md"]
            
            required_elements = [
                "paradigma", "abordagem", "classificação",
                "técnicas", "coleta", "análise"
            ]
            
            for elem in required_elements:
                if elem.lower() not in content.lower():
                    issues.append(f"Metodologia: elemento ausente - {elem}")
                    score -= 0.2
        
        return ValidationResult(
            passed=score >= 7.0,
            score=max(0, score),
            issues=issues
        )
    
    def validate_results(self) -> ValidationResult:
        """Validar apresentação de resultados"""
        issues = []
        score = 10.0
        
        if "CAPITULO_04_COMPLETO.md" in self.chapters:
            content = self.chapters["CAPITULO_04_COMPLETO.md"]
            
            # Verificar dados/tabelas/gráficos
            has_data = any(marker in content for marker in ['Tabela', 'Figura', 'TABELA', 'FIGURA'])
            if not has_data:
                issues.append("Resultados: sem apresentação de dados (tabelas/figuras)")
                score -= 0.5
        
        return ValidationResult(
            passed=score >= 7.0,
            score=max(0, score),
            issues=issues
        )
    
    def validate_discussion(self) -> ValidationResult:
        """Validar discussão e conclusões"""
        issues = []
        score = 10.0
        
        if "CAPITULO_05_06_COMPLETO.md" in self.chapters:
            content = self.chapters["CAPITULO_05_06_COMPLETO.md"].upper()
            
            required = ["DISCUSSÃO", "CONCLUSÃO", "LIMITAÇÕES", "CONTRIBUIÇÕES"]
            for req in required:
                if req not in content:
                    issues.append(f"Discussão: seção ausente - {req}")
                    score -= 0.3
        
        return ValidationResult(
            passed=score >= 7.0,
            score=max(0, score),
            issues=issues
        )
    
    def validate_integration(self) -> ValidationResult:
        """Validar integração com rede Transformer/MCP"""
        issues = []
        score = 10.0
        
        # Verificar menções ao ecossistema MCP/Transformer
        keywords = [
            "MCP", "Model Context Protocol", "Transformer",
            "agente", "orquestrador", "mcp_cross", "handoff"
        ]
        
        total_mentions = 0
        for content in self.chapters.values():
            for kw in keywords:
                total_mentions += content.lower().count(kw.lower())
        
        if total_mentions < 10:
            issues.append(f"Integração: poucas menções ao ecossistema MCP/Transformer ({total_mentions})")
            score -= 0.5
        
        return ValidationResult(
            passed=score >= 8.0,
            score=max(0, score),
            issues=issues
        )
    
    def run_full_validation(self) -> Dict:
        """Executar validação completa"""
        print("="*60)
        print("QUALIS A1 VALIDATION - MASWOS V5 NEXUS")
        print("="*60)
        
        results = {
            "structure": self.validate_structure(),
            "citations": self.validate_citations(),
            "references": self.validate_references(),
            "methodology": self.validate_methodology(),
            "results": self.validate_results(),
            "discussion": self.validate_discussion(),
            "integration": self.validate_integration()
        }
        
        total_score = sum(r.score for r in results.values()) / len(results)
        
        print("\n[VALIDACAO QUALIS A1]")
        print(f"   Estrutura IMRAD:      {results['structure'].score:.1f}/10 - {'OK' if results['structure'].passed else 'FALHA'}")
        print(f"   Citações ABNT:       {results['citations'].score:.1f}/10 - {'OK' if results['citations'].passed else 'FALHA'}")
        print(f"   Referências:          {results['references'].score:.1f}/10 - {'OK' if results['references'].passed else 'FALHA'}")
        print(f"   Metodologia:          {results['methodology'].score:.1f}/10 - {'OK' if results['methodology'].passed else 'FALHA'}")
        print(f"   Resultados:           {results['results'].score:.1f}/10 - {'OK' if results['results'].passed else 'FALHA'}")
        print(f"   Discussão:            {results['discussion'].score:.1f}/10 - {'OK' if results['discussion'].passed else 'FALHA'}")
        print(f"   Integração MCP:       {results['integration'].score:.1f}/10 - {'OK' if results['integration'].passed else 'FALHA'}")
        
        print(f"\n[NOTA FINAL: {total_score:.1f}/10]")
        
        # Listar todos os issues
        all_issues = []
        for r in results.values():
            all_issues.extend(r.issues)
        
        if all_issues:
            print("\n[ITENS A CORRIGIR:]")
            for issue in all_issues[:10]:
                print(f"   - {issue}")
        
        print("="*60)
        
        return {
            "score": total_score,
            "passed": total_score >= 9.0,
            "results": {k: {"score": v.score, "passed": v.passed, "issues": v.issues} 
                       for k, v in results.items()},
            "all_issues": all_issues
        }


def validate_thesis(thesis_path: str) -> Dict:
    """Função principal de validação"""
    validator = QualisA1Validator(thesis_path)
    
    if not validator.load_chapters():
        return {"error": "Não foi possível carregar os capítulos"}
    
    validator.load_references()
    
    return validator.run_full_validation()


if __name__ == "__main__":
    import sys
    
    thesis_dir = "mcp-ecossistema-tese"
    if len(sys.argv) > 1:
        thesis_dir = sys.argv[1]
    
    result = validate_thesis(thesis_dir)
    
    if "error" in result:
        print(f"Erro: {result['error']}")
    elif result["passed"]:
        print("\n[TESE APROVADA - QUALIS A1]")
    else:
        print("\n[TESE PRECISA DE REVISÃO]")
    
    sys.exit(0 if result.get("passed", False) else 1)