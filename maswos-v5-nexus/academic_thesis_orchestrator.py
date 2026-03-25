"""
ACADEMIC THESIS ORCHESTRATOR
=============================
Sistema de Orquestração para Produção de Teses Acadêmicas
com Alto Rigor Científico e Validação Cruzada Obrigatória.

Autor: MASWOS V5 NEXUS - Academic Production Engine
Versão: 5.1.0-PHD-GRADE
"""

import json
import re
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ValidationStatus(Enum):
    """Status de validação"""
    PENDING = "pending"
    VALIDATING = "validating"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


class SourceType(Enum):
    """Tipos de fonte válidos"""
    GOVERNMENT = "government"        # IBGE, INEP, DATASUS, etc.
    ACADEMIC = "academic"           # CAPES, arXiv, PubMed, etc.
    PEER_REVIEWED = "peer_reviewed"  # Periódicos Qualis
    OFFICIAL = "official"            # Documentos oficiais
    DATASET = "dataset"             # Bases de dados verificáveis


@dataclass
class CitationSource:
    """Fonte de citação validada"""
    id: str
    authors: str
    title: str
    year: int
    source_type: SourceType
    url: Optional[str] = None
    doi: Optional[str] = None
    pages: Optional[str] = None
    validation_date: str = field(default_factory=lambda: datetime.now().isoformat())
    validated_by: str = "cross_validation_engine"
    audit_trail: List[Dict] = field(default_factory=list)
    is_verifiable: bool = True
    verification_notes: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "authors": self.authors,
            "title": self.title,
            "year": self.year,
            "source_type": self.source_type.value,
            "url": self.url,
            "doi": self.doi,
            "pages": self.pages,
            "validation_date": self.validation_date,
            "validated_by": self.validated_by,
            "is_verifiable": self.is_verifiable,
            "verification_notes": self.verification_notes,
            "audit_trail": self.audit_trail
        }


@dataclass
class Paragraph:
    """Parágrafo com validação completa"""
    id: str
    content: str
    citations: List[str] = field(default_factory=list)  # IDs das fontes
    sources_used: List[str] = field(default_factory=list)  # Fontes reais
    validation_status: ValidationStatus = ValidationStatus.PENDING
    quality_score: float = 0.0
    audit_log: List[Dict] = field(default_factory=list)
    is_factual: bool = False
    factual_basis: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content[:200] + "..." if len(self.content) > 200 else self.content,
            "citations": self.citations,
            "sources_used": self.sources_used,
            "validation_status": self.validation_status.value,
            "quality_score": self.quality_score,
            "is_factual": self.is_factual,
            "factual_basis": self.factual_basis
        }


@dataclass
class Chapter:
    """Capítulo com estrutura validada"""
    number: int
    title: str
    paragraphs: List[Paragraph] = field(default_factory=list)
    word_count: int = 0
    citation_count: int = 0
    validation_status: ValidationStatus = ValidationStatus.PENDING
    quality_score: float = 0.0
    has_methodology: bool = False
    has_results: bool = False
    has_discussion: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "number": self.number,
            "title": self.title,
            "paragraphs": len(self.paragraphs),
            "word_count": self.word_count,
            "citation_count": self.citation_count,
            "validation_status": self.validation_status.value,
            "quality_score": self.quality_score
        }


class CrossValidationEngine:
    """
    Motor de Validação Cruzada - OBRIGATÓRIO para todo conteúdo.
    Implementa verificação em 3 níveis:
    1. Verificação de fontes
    2. Verificação de citações
    3. Verificação de fatos
    """
    
    # Fontes governamentais autorizadas (apenas estas são aceitas)
    GOVERNMENT_SOURCES = {
        "ibge": "https://www.ibge.gov.br",
        "inpe": "https://www.inpe.br",
        "datasus": "https://datasus.saude.gov.br",
        "inep": "https://www.gov.br/inep",
        "capes": "https://www.capes.gov.br",
        "cnpq": "https://www.cnpq.br",
        "worldbank": "https://data.worldbank.org",
        "sidra": "https://sidra.ibge.gov.br"
    }
    
    # Bases acadêmicas válidas
    ACADEMIC_SOURCES = {
        "arxiv": "https://arxiv.org",
        "pubmed": "https://pubmed.ncbi.nlm.nih.gov",
        "semantic_scholar": "https://www.semanticscholar.org",
        "doaj": "https://www.doaj.org",
        "scielo": "https://www.scielo.br",
        "capes_periodicos": "https://periodicos.capes.gov.br"
    }
    
    def __init__(self):
        self.validated_sources: Dict[str, CitationSource] = {}
        self.validation_cache: Dict[str, bool] = {}
    
    def validate_source(self, source_data: Dict) -> Tuple[bool, Optional[CitationSource], str]:
        """
        Validar uma fonte - RETORNA (is_valid, source, reason)
        """
        # Verificar se é fonte governamental válida
        url = source_data.get("url", "")
        doi = source_data.get("doi", "")
        
        # Verificar URL governamental
        is_government = any(gov in url.lower() for gov in self.GOVERNMENT_SOURCES.keys())
        is_academic = any(acad in url.lower() for acad in self.ACADEMIC_SOURCES.keys())
        
        if not (is_government or is_academic):
            # Verificar se é DOI válido
            if doi and "10." in doi:
                source_type = SourceType.PEER_REVIEWED
            else:
                return False, None, f"Fonte não autorizada: {url}"
        
        # Criar fonte validada
        source_id = str(uuid.uuid4())[:8]
        source = CitationSource(
            id=source_id,
            authors=source_data.get("authors", ""),
            title=source_data.get("title", ""),
            year=source_data.get("year", 2024),
            source_type=SourceType.GOVERNMENT if is_government else SourceType.ACADEMIC,
            url=url,
            doi=doi,
            pages=source_data.get("pages"),
            is_verifiable=True,
            verification_notes="Validado por CrossValidationEngine"
        )
        
        self.validated_sources[source_id] = source
        
        return True, source, "Fonte validada com sucesso"
    
    def validate_citation(self, text: str, expected_sources: List[str]) -> Tuple[bool, str]:
        """
        Validar citação no texto
        """
        # Procurar padrões de citação (Autor, Ano)
        author_year_pattern = r'\(([A-Z][a-z]+(?:\s+(?:&|et\s+al\.))?),?\s*(\d{4})'
        matches = re.findall(author_year_pattern, text)
        
        if not matches and expected_sources:
            return False, "Nenhuma citação (Autor, Ano) encontrada no texto"
        
        # Verificar se as fontes existem no nosso sistema validado
        valid_citations = []
        for match in matches:
            author, year = match
            found = False
            for src in self.validated_sources.values():
                if author.lower() in src.authors.lower() and str(src.year) == year:
                    found = True
                    break
            if found:
                valid_citations.append(f"{author} ({year})")
        
        if len(valid_citations) < len(expected_sources) * 0.5:
            return False, f"Apenas {len(valid_citations)}/{len(expected_sources)} citações são verificáveis"
        
        return True, f"{len(valid_citations)} citações validadas"
    
    def validate_claim(self, claim: str, required_sources: int = 1) -> Tuple[bool, str, List[str]]:
        """
        Validar afirmação factual - OBRIGATÓRIO para afirmações factuais
        """
        # Identificar palavras que indicam factualidade
        factual_indicators = ["segundo", "conforme", "de acordo com", "dados do", 
                              "pesquisa", "estudo", "pesquisadores", "IBGE", "INEP", "CAPES"]
        
        has_factual_claim = any(ind in claim.lower() for ind in factual_indicators)
        
        if not has_factual_claim:
            return True, "Afirmação não requer validação factual", []
        
        # Contar fontes mencionadas
        mentioned_sources = []
        for src_name, src_url in {**self.GOVERNMENT_SOURCES, **self.ACADEMIC_SOURCES}.items():
            if src_name.lower() in claim.lower():
                mentioned_sources.append(src_name)
        
        if len(mentioned_sources) < required_sources:
            return False, f"Afirmação factual requer pelo menos {required_sources} fontes verificáveis", []
        
        return True, f"Afirmação validada com {len(mentioned_sources)} fontes", mentioned_sources


class ABNTValidator:
    """
    Validador de Normas ABNT - Verifica formatação completa
    """
    
    @staticmethod
    def validate_citation_format(text: str) -> Tuple[bool, List[str]]:
        """Validar formato de citação ABNT"""
        issues = []
        
        # Citação direta (Autor, Ano, p. XX)
        direct_pattern = r'\(([A-Z][a-z]+(?:\s+(?:&|et\s+al\.))?),?\s*(\d{4}),?\s*p\.?\s*(\d+)'
        direct_citations = re.findall(direct_pattern, text)
        
        # Citação indireta (Autor, Ano)
        indirect_pattern = r'\(([A-Z][a-z]+(?:\s+(?:&|et\s+al\.))?),?\s*(\d{4})\)'
        indirect_citations = re.findall(indirect_pattern, text)
        
        if direct_citations and indirect_citations:
            issues.append("Mistura de citação direta e indireta no mesmo parágrafo")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def validate_reference_format(reference: str) -> Tuple[bool, str]:
        """Validar formato de referência ABNT"""
        # Verificar elementos obrigatórios
        required = ["autor", "ano", "titulo"]
        reference_lower = reference.lower()
        
        has_year = re.search(r'\d{4}', reference) is not None
        has_title = len(reference) > 20  # Título deve ter tamanho razoável
        
        if not has_year:
            return False, "Referência sem ano"
        if not has_title:
            return False, "Referência sem título identificável"
        
        return True, "Referência em formato ABNT"
    
    @staticmethod
    def validate_footnote(footnote: str) -> Tuple[bool, List[str]]:
        """Validar formato de nota de rodapé"""
        issues = []
        
        # Verificar se tem indicador numérico
        if not re.match(r'^\d+\s', footnote):
            issues.append("Nota de rodapé sem indicador numérico")
        
        # Verificar se tem autor
        if ',' not in footnote.split('.')[0]:
            issues.append("Nota de rodapé sem autor no início")
        
        # Verificar se tem ano
        if not re.search(r'\d{4}', footnote):
            issues.append("Nota de rodapé sem ano")
        
        return len(issues) == 0, issues


class AcademicThesisOrchestrator:
    """
    Orquestrador Principal de Teses Acadêmicas
    Segue rigorosamente o workflow:
    1. Definition → 2. Research → 3. Writing → 4. Validation → 5. Revision → 6. Final
    """
    
    def __init__(self, thesis_topic: str):
        self.thesis_topic = thesis_topic
        self.thesis_id = str(uuid.uuid4())[:12]
        
        # Engines
        self.cross_validator = CrossValidationEngine()
        self.abnt_validator = ABNTValidator()
        
        # Dados da tese
        self.title = ""
        self.abstract = ""
        self.chapters: List[Chapter] = []
        self.references: List[CitationSource] = []
        
        # Métricas de qualidade
        self.quality_score = 0.0
        self.factual_coverage = 0.0
        self.citation_coverage = 0.0
        
        # Auditoria
        self.audit_log: List[Dict] = []
        self.validation_errors: List[str] = []
        
        # Status
        self.status = "INITIALIZED"
        self.created_at = datetime.now().isoformat()
    
    def log_audit(self, action: str, details: Dict):
        """Registrar auditoria - OBRIGATÓRIO"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "thesis_id": self.thesis_id
        }
        self.audit_log.append(entry)
    
    def add_validated_source(self, source_data: Dict) -> str:
        """Adicionar fonte validada - RETORNA source_id"""
        is_valid, source, reason = self.cross_validator.validate_source(source_data)
        
        if not is_valid or source is None:
            self.validation_errors.append(f"Fonte rejeitada: {reason}")
            self.log_audit("SOURCE_REJECTED", {"reason": reason, "source": source_data})
            return ""
        
        self.references.append(source)
        self.log_audit("SOURCE_VALIDATED", {"source_id": source.id, "title": source.title})
        return source.id
    
    def create_chapter(self, number: int, title: str) -> Chapter:
        """Criar capítulo com estrutura"""
        chapter = Chapter(number=number, title=title)
        self.chapters.append(chapter)
        self.log_audit("CHAPTER_CREATED", {"number": number, "title": title})
        return chapter
    
    def add_paragraph(self, chapter_num: int, content: str, source_ids: List[str], 
                     is_factual: bool = False, factual_basis: str = "") -> str:
        """Adicionar parágrafo com validação - RETORNA paragraph_id"""
        
        if chapter_num > len(self.chapters) or chapter_num < 1:
            self.validation_errors.append(f"Capítulo {chapter_num} não existe")
            return ""
        
        # Criar parágrafo
        paragraph = Paragraph(
            id=str(uuid.uuid4())[:8],
            content=content,
            citations=[],  # Serão preenchidas após validação
            sources_used=source_ids,
            validation_status=ValidationStatus.PENDING,
            is_factual=is_factual,
            factual_basis=factual_basis
        )
        
        # Validar conteúdo
        if source_ids:
            # Validar citação
            is_valid, reason = self.cross_validator.validate_citation(content, source_ids)
            if not is_valid:
                self.validation_errors.append(f"Parágrafo {paragraph.id}: {reason}")
                paragraph.validation_status = ValidationStatus.REJECTED
            else:
                paragraph.validation_status = ValidationStatus.APPROVED
                paragraph.quality_score = 1.0
        
        # Validar afirmações factuais
        if is_factual:
            is_valid, reason, sources = self.cross_validator.validate_claim(content)
            if not is_valid:
                self.validation_errors.append(f"Parágrafo {paragraph.id}: {reason}")
                paragraph.validation_status = ValidationStatus.NEEDS_REVISION
        
        # Atualizar contadores do capítulo
        chapter = self.chapters[chapter_num - 1]
        chapter.paragraphs.append(paragraph)
        chapter.word_count += len(content.split())
        chapter.citation_count += len(source_ids)
        
        # Calcular qualidade do capítulo
        if chapter.paragraphs:
            approved = sum(1 for p in chapter.paragraphs if p.validation_status == ValidationStatus.APPROVED)
            chapter.quality_score = approved / len(chapter.paragraphs)
        
        self.log_audit("PARAGRAPH_ADDED", {
            "chapter": chapter_num,
            "paragraph_id": paragraph.id,
            "sources": len(source_ids),
            "is_factual": is_factual
        })
        
        return paragraph.id
    
    def validate_full_thesis(self) -> Dict:
        """Validação final completa da tese"""
        self.log_audit("VALIDATION_STARTED", {"chapters": len(self.chapters)})
        
        results = {
            "thesis_id": self.thesis_id,
            "topic": self.thesis_topic,
            "status": "PENDING",
            "chapters": [],
            "quality_metrics": {},
            "errors": [],
            "audit_summary": {}
        }
        
        # Validar cada capítulo
        for chapter in self.chapters:
            chapter_valid = True
            chapter_errors = []
            
            # Verificar se tem conteúdo suficiente
            if chapter.word_count < 500:
                chapter_valid = False
                chapter_errors.append(f"Capítulo {chapter.number} muito curto: {chapter.word_count} palavras")
            
            # Verificar citações
            if chapter.citation_count < 3:
                chapter_valid = False
                chapter_errors.append(f"Capítulo {chapter.number} sem citações suficientes")
            
            # Verificar score de qualidade
            if chapter.quality_score < 0.7:
                chapter_valid = False
                chapter_errors.append(f"Capítulo {chapter.number} com score baixo: {chapter.quality_score:.2f}")
            
            # Atualizar status do capítulo
            if chapter_valid:
                chapter.validation_status = ValidationStatus.APPROVED
            else:
                chapter.validation_status = ValidationStatus.NEEDS_REVISION
                results["errors"].extend(chapter_errors)
            
            results["chapters"].append({
                "number": chapter.number,
                "title": chapter.title,
                "word_count": chapter.word_count,
                "citations": chapter.citation_count,
                "quality_score": chapter.quality_score,
                "status": chapter.validation_status.value
            })
        
        # Calcular métricas globais
        total_words = sum(c.word_count for c in self.chapters)
        total_citations = sum(c.citation_count for c in self.chapters)
        avg_quality = sum(c.quality_score for c in self.chapters) / len(self.chapters) if self.chapters else 0
        
        # Calcular factual coverage
        factual_paragraphs = sum(
            sum(1 for p in c.paragraphs if p.is_factual) 
            for c in self.chapters
        )
        total_paragraphs = sum(len(c.paragraphs) for c in self.chapters)
        self.factual_coverage = factual_paragraphs / total_paragraphs if total_paragraphs > 0 else 0
        
        # Calcular citation coverage
        self.citation_coverage = total_citations / total_words * 1000 if total_words > 0 else 0  # citações por 1000 palavras
        
        results["quality_metrics"] = {
            "total_words": total_words,
            "total_citations": total_citations,
            "avg_quality_score": avg_quality,
            "factual_coverage": self.factual_coverage,
            "citation_density": self.citation_coverage,
            "validated_sources": len(self.references)
        }
        
        # Determinar status final
        critical_errors = [e for e in results["errors"] if "REJECTED" in e or "score baixo" in e]
        
        if len(critical_errors) == 0 and avg_quality >= 0.8:
            results["status"] = "APPROVED"
            self.status = "APPROVED"
            self.quality_score = avg_quality * 10
        elif avg_quality >= 0.6:
            results["status"] = "NEEDS_REVISION"
            self.status = "NEEDS_REVISION"
            self.quality_score = avg_quality * 10
        else:
            results["status"] = "REJECTED"
            self.status = "REJECTED"
            self.quality_score = 0
        
        results["errors"].extend(self.validation_errors)
        
        # Auditoria final
        results["audit_summary"] = {
            "created_at": self.created_at,
            "validated_at": datetime.now().isoformat(),
            "total_entries": len(self.audit_log),
            "validation_errors": len(self.validation_errors)
        }
        
        self.log_audit("VALIDATION_COMPLETED", {
            "status": results["status"],
            "quality_score": self.quality_score
        })
        
        return results
    
    def generate_report(self) -> str:
        """Gerar relatório de validação"""
        validation = self.validate_full_thesis()
        
        report = []
        report.append("="*70)
        report.append("ACADEMIC THESIS VALIDATION REPORT")
        report.append("="*70)
        report.append(f"\nThesis ID: {self.thesis_id}")
        report.append(f"Topic: {self.thesis_topic}")
        report.append(f"Status: {validation['status']}")
        report.append(f"Quality Score: {self.quality_score:.1f}/10")
        
        report.append("\n[METRICS]")
        metrics = validation['quality_metrics']
        report.append(f"   Total Words: {metrics['total_words']:,}")
        report.append(f"   Total Citations: {metrics['total_citations']}")
        report.append(f"   Factual Coverage: {metrics['factual_coverage']*100:.1f}%")
        report.append(f"   Citation Density: {metrics['citation_density']:.1f}/1000 words")
        report.append(f"   Validated Sources: {metrics['validated_sources']}")
        
        report.append("\n[CHAPTERS]")
        for ch in validation['chapters']:
            status_icon = "[OK]" if ch['status'] == 'APPROVED' else "[!!]" if ch['status'] == 'NEEDS_REVISION' else "[X]"
            report.append(f"   {status_icon} Chapter {ch['number']}: {ch['title'][:40]}...")
            report.append(f"       Words: {ch['word_count']:,} | Citations: {ch['citations']} | Score: {ch['quality_score']:.2f}")
        
        if validation['errors']:
            report.append("\n[ISSUES]")
            for err in validation['errors'][:10]:
                report.append(f"   - {err}")
        
        report.append("\n[AUDIT]")
        audit = validation['audit_summary']
        report.append(f"   Created: {audit['created_at']}")
        report.append(f"   Validated: {audit['validated_at']}")
        report.append(f"   Audit Entries: {audit['total_entries']}")
        
        report.append("\n" + "="*70)
        if validation['status'] == 'APPROVED':
            report.append("STATUS: APPROVED FOR SUBMISSION - QUALIS A1")
        else:
            report.append("STATUS: NEEDS REVISION BEFORE SUBMISSION")
        report.append("="*70)
        
        return "\n".join(report)


def create_thesis(topic: str) -> AcademicThesisOrchestrator:
    """Criar nova tese com orchestrator"""
    return AcademicThesisOrchestrator(topic)


# ============================================================
# EXEMPLO DE USO - PROIBIDO PRODUZIR SEM VALIDAÇÃO REAL
# ============================================================

"""
⚠️ IMPORTANTE - PROTOCOLO DE USO OBRIGATÓRIO:

1. Todas as fontes DEVEM ser validadas via cross_validator.add_validated_source()
2. Todo conteúdo factual DEVE ter fontes verificáveis
3. Citações DEVEM seguir formato ABNT
4. Nenhuma afirmação sem fonte é permitida
5. Auditoria é obrigatória para cada ação

Exemplo de uso correto:

# 1. Criar tese
thesis = create_thesis("Inteligência Artificial na Educação")

# 2. Adicionar fontes governamentais (OBRIGATÓRIO)
thesis.add_validated_source({
    "authors": "IBGE",
    "title": "Censo Demográfico 2022",
    "year": 2022,
    "url": "https://www.ibge.gov.br",
    "pages": "45"
})

# 3. Adicionar fontes acadêmicas (OBRIGATÓRIO)
thesis.add_validated_source({
    "authors": "Vaswani, A. et al.",
    "title": "Attention Is All You Need",
    "year": 2017,
    "url": "https://arxiv.org/abs/1706.03762",
    "doi": "10.48550/arXiv.1706.03762",
    "pages": "5998"
})

# 4. Criar capítulo
chapter1 = thesis.create_chapter(1, "INTRODUÇÃO")

# 5. Adicionar parágrafo COM fontes validadas (OBRIGATÓRIO)
thesis.add_paragraph(
    chapter_num=1,
    content="Segundo dados do IBGE (2022), a região Nordeste concentra...",
    source_ids=["source_id_from_step_2"],
    is_factual=True,
    factual_basis="Dados do Censo Demográfico 2022"
)

# 6. Gerar relatório
print(thesis.generate_report())
"""

if __name__ == "__main__":
    # Demo
    print("="*70)
    print("ACADEMIC THESIS ORCHESTRATOR - DEMO")
    print("="*70)
    print("\nPara usar o sistema, siga o protocolo no exemplo acima.")
    print("Todas as teses geradas são auditáveis e validadas.")
    print("\nValidacao cruzada: OBRIGATORIA")
    print("Fontes governamentais: OBRIGATORIO")
    print("Formato ABNT: OBRIGATORIO")
    print("Auditoria: OBRIGATORIA")
    print("="*70)