#!/usr/bin/env python3
"""
MASWOS Academic Forensic Validator
Validador forense de integridade para artigos acadêmicos
"""

import hashlib
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from collections import Counter


class ForensicValidator:
    """Validador forense de artigos acadêmicos"""
    
    def __init__(self):
        self.validation_history = []
    
    def validate_article(self, article: Dict) -> Dict:
        """
        Validação completa de um artigo
        Returns: dict com scores de validação
        """
        results = {
            "article_id": article.get("id") or article.get("doi", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "validations": {},
            "overall_score": 0.0,
            "warnings": [],
            "passed": False
        }
        
        metadata_score = self._validate_metadata(article)
        results["validations"]["metadata"] = metadata_score
        
        citation_score = self._validate_citations(article)
        results["validations"]["citations"] = citation_score
        
        integrity_score = self._validate_integrity(article)
        results["validations"]["integrity"] = integrity_score
        
        plagiarism_score = self._check_plagiarism_risk(article)
        results["validations"]["plagiarism_risk"] = plagiarism_score
        
        quality_score = self._calculate_quality(article)
        results["validations"]["quality"] = quality_score
        
        all_scores = [metadata_score, citation_score, integrity_score, 
                      plagiarism_score, quality_score]
        results["overall_score"] = sum(all_scores) / len(all_scores)
        results["passed"] = results["overall_score"] >= 0.70
        
        self.validation_history.append(results)
        return results
    
    def _validate_metadata(self, article: Dict) -> float:
        """Valida completude dos metadados"""
        score = 0.0
        total = 0
        
        required_fields = ["title", "authors", "doi"]
        optional_fields = ["abstract", "published", "journal", "categories"]
        
        for field in required_fields:
            total += 1
            if article.get(field):
                score += 1.0
            else:
                if field == "doi":
                    if article.get("url") or article.get("id"):
                        score += 0.5
                else:
                    pass
        
        for field in optional_fields:
            total += 0.5
            if article.get(field):
                score += 0.5
        
        return score / total if total > 0 else 0.0
    
    def _validate_citations(self, article: Dict) -> float:
        """Valida formato de citações"""
        score = 0.5
        
        doi = article.get("doi", "")
        if doi:
            doi_pattern = r"^10\.\d{4,}/[^\s]+$"
            if re.match(doi_pattern, doi):
                score += 0.25
        
        if article.get("url"):
            if doi or article.get("pdf_url"):
                score += 0.25
        
        return min(score, 1.0)
    
    def _validate_integrity(self, article: Dict) -> float:
        """Valida integridade do artigo"""
        score = 0.5
        
        title = article.get("title", "")
        if title and len(title) > 10:
            score += 0.25
        
        abstract = article.get("abstract") or article.get("summary", "")
        if abstract and len(abstract) > 50:
            score += 0.25
        
        return min(score, 1.0)
    
    def _check_plagiarism_risk(self, article: Dict) -> float:
        """Calcula risco de plágio"""
        score = 1.0
        
        title = article.get("title", "")
        if not title:
            return 0.0
        
        if len(title) < 10:
            score -= 0.3
        
        authors = article.get("authors", [])
        if not authors or len(authors) == 0:
            score -= 0.2
        
        source = article.get("source", "")
        if source in ["semantic_scholar_fallback", "unknown"]:
            score -= 0.1
        
        return max(score, 0.0)
    
    def _calculate_quality(self, article: Dict) -> float:
        """Calcula score de qualidade"""
        score = 0.3
        
        citations = article.get("cited_by_count", 0)
        if citations:
            if citations > 100:
                score += 0.4
            elif citations > 10:
                score += 0.2
            else:
                score += 0.1
        
        is_oa = article.get("open_access", article.get("is_oa", False))
        if is_oa:
            score += 0.2
        
        pdf_url = article.get("pdf_url")
        if pdf_url and ("arxiv" in str(pdf_url) or "pdf" in str(pdf_url)):
            score += 0.1
        
        return min(score, 1.0)
    
    def cross_validate(self, articles: List[Dict], sources: List[str]) -> Dict:
        """
        Validação cruzada de artigos contra múltiplas fontes
        """
        results = {
            "total_articles": len(articles),
            "sources_checked": sources,
            "convergence": {},
            "divergences": [],
            "overall_convergence": 0.0
        }
        
        doi_groups = {}
        for article in articles:
            doi = article.get("doi")
            if doi:
                if doi not in doi_groups:
                    doi_groups[doi] = []
                doi_groups[doi].append(article.get("source", "unknown"))
        
        matches = 0
        total = 0
        for doi, source_list in doi_groups.items():
            total += 1
            unique_sources = set(source_list)
            if len(unique_sources) > 1:
                matches += 1
                results["convergence"][doi] = {
                    "sources": list(unique_sources),
                    "count": len(unique_sources)
                }
            else:
                results["divergences"].append(doi)
        
        results["overall_convergence"] = matches / total if total > 0 else 0.0
        return results
    
    def detect_duplicates(self, articles: List[Dict]) -> Dict:
        """
        Detecta artigos duplicados
        """
        seen = {}
        duplicates = []
        
        for article in articles:
            key = self._generate_article_key(article)
            if key in seen:
                duplicates.append({
                    "original": seen[key],
                    "duplicate": article.get("id") or article.get("doi", "unknown"),
                    "title": article.get("title", "")
                })
            else:
                seen[key] = article.get("id") or article.get("doi", "unknown")
        
        return {
            "total_articles": len(articles),
            "unique_articles": len(seen),
            "duplicates_found": len(duplicates),
            "duplicate_rate": len(duplicates) / len(articles) if articles else 0,
            "duplicates": duplicates
        }
    
    def _generate_article_key(self, article: Dict) -> str:
        """Gera chave única para artigo"""
        title = article.get("title", "").lower().strip()
        title = re.sub(r'[^\w]', '', title)
        
        authors_len = len(article.get("authors", []))
        
        return f"{title[:50]}_{authors_len}"
    
    def generate_audit_report(self, articles: List[Dict]) -> Dict:
        """
        Gera relatório de auditoria completo
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_articles": len(articles),
            "sources": {},
            "validation_summary": {},
            "quality_distribution": {
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "recommendations": []
        }
        
        for article in articles:
            source = article.get("source", "unknown")
            if source not in report["sources"]:
                report["sources"][source] = 0
            report["sources"][source] += 1
        
        validation_results = [self.validate_article(a) for a in articles]
        
        for vr in validation_results:
            score = vr["overall_score"]
            if score >= 0.8:
                report["quality_distribution"]["high"] += 1
            elif score >= 0.6:
                report["quality_distribution"]["medium"] += 1
            else:
                report["quality_distribution"]["low"] += 1
        
        total = len(validation_results)
        if total > 0:
            avg_score = sum(v["overall_score"] for v in validation_results) / total
            report["validation_summary"]["average_score"] = avg_score
            report["validation_summary"]["pass_rate"] = sum(1 for v in validation_results if v["passed"]) / total
        
        if report["quality_distribution"]["low"] > total * 0.3:
            report["recommendations"].append("Alta taxa de artigos com baixa qualidade. Considere filtrar por fonte.")
        
        dup_result = self.detect_duplicates(articles)
        if dup_result["duplicate_rate"] > 0.05:
            report["recommendations"].append(f"Taxa de duplicatas: {dup_result['duplicate_rate']:.1%}. Considere deduplicar.")
        
        return report


class CitationValidator:
    """Validador de citações"""
    
    @staticmethod
    def parse_citation(citation: str) -> Dict:
        """Parseia string de citação"""
        result = {
            "original": citation,
            "type": "unknown",
            "authors": [],
            "year": None,
            "title": "",
            "doi": None,
            "is_valid": False
        }
        
        doi_match = re.search(r"10\.\d{4,}/[^\s]+", citation)
        if doi_match:
            result["doi"] = doi_match.group()
            result["type"] = "doi"
            result["is_valid"] = True
        
        year_match = re.search(r"\b(19|20)\d{2}\b", citation)
        if year_match:
            result["year"] = int(year_match.group())
        
        return result
    
    @staticmethod
    def validate_reference_list(references: List[str]) -> Dict:
        """Valida lista de referências"""
        parsed = [CitationValidator.parse_citation(ref) for ref in references]
        
        valid = sum(1 for p in parsed if p["is_valid"])
        with_doi = sum(1 for p in parsed if p["doi"])
        
        return {
            "total": len(references),
            "valid": valid,
            "with_doi": with_doi,
            "validity_rate": valid / len(references) if references else 0,
            "doi_rate": with_doi / len(references) if references else 0,
            "parsed": parsed
        }


def main():
    """Teste do validador forense"""
    validator = ForensicValidator()
    
    test_articles = [
        {
            "id": "1",
            "title": "Deep Learning for Natural Language Processing",
            "abstract": "This paper presents a novel approach...",
            "authors": ["John Smith", "Jane Doe"],
            "doi": "10.1234/test.2024.001",
            "cited_by_count": 150,
            "open_access": True,
            "pdf_url": "https://arxiv.org/pdf/2401.00001",
            "source": "arxiv"
        },
        {
            "id": "2",
            "title": "Machine Learning in Healthcare",
            "authors": ["Alice Johnson"],
            "doi": "10.1234/test.2024.002",
            "source": "pubmed"
        }
    ]
    
    print("=" * 60)
    print("MASWOS Forensic Validator - Teste")
    print("=" * 60)
    
    for article in test_articles:
        result = validator.validate_article(article)
        print(f"\nArtigo: {article['title'][:40]}...")
        print(f"  Score: {result['overall_score']:.2f}")
        print(f"  Passed: {result['passed']}")
    
    dup_result = validator.detect_duplicates(test_articles)
    print(f"\nDuplicates: {dup_result['duplicates_found']}")
    
    report = validator.generate_audit_report(test_articles)
    print(f"\nAverage Score: {report['validation_summary'].get('average_score', 0):.2f}")
    print(f"Pass Rate: {report['validation_summary'].get('pass_rate', 0):.1%}")


if __name__ == "__main__":
    main()


class AdvancedForensicValidator:
    """Validador forense avançado com análise de duplicatas e plágio"""
    
    def __init__(self):
        self.article_cache = {}
        self.fingerprint_cache = {}
    
    def compute_article_fingerprint(self, article: Dict) -> str:
        """Gera fingerprint único para artigo baseado em título"""
        import hashlib
        title = article.get("title", "").lower().strip()
        title = re.sub(r'[^\w\s]', '', title)
        title = ' '.join(title.split())
        
        doi = article.get("doi", "").lower().strip()
        
        combined = f"{title}|{doi}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def detect_similarity(self, article1: Dict, article2: Dict) -> float:
        """Detecta similaridade entre dois artigos"""
        title1 = article1.get("title", "").lower()
        title2 = article2.get("title", "").lower()
        
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        jaccard = len(intersection) / len(union) if union else 0
        
        doi1 = article1.get("doi", "")
        doi2 = article2.get("doi", "")
        
        if doi1 and doi2 and doi1 == doi2:
            return 1.0
        
        return jaccard
    
    def find_similar_articles(self, article: Dict, corpus: List[Dict], 
                               threshold: float = 0.7) -> List[Dict]:
        """Encontra artigos similares em um corpus"""
        similar = []
        
        for candidate in corpus:
            if candidate.get("doi") == article.get("doi"):
                continue
            
            sim = self.detect_similarity(article, candidate)
            if sim >= threshold:
                similar.append({
                    "article": candidate,
                    "similarity_score": sim
                })
        
        return sorted(similar, key=lambda x: x["similarity_score"], reverse=True)
    
    def cluster_articles(self, articles: List[Dict], 
                        threshold: float = 0.7) -> List[List[Dict]]:
        """Agrupa artigos em clusters por similaridade"""
        clusters = []
        assigned = set()
        
        for i, article in enumerate(articles):
            if i in assigned:
                continue
            
            cluster = [article]
            assigned.add(i)
            
            for j, candidate in enumerate(articles):
                if j in assigned:
                    continue
                
                sim = self.detect_similarity(article, candidate)
                if sim >= threshold:
                    cluster.append(candidate)
                    assigned.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def validate_title_structure(self, title: str) -> Dict:
        """Valida estrutura do título"""
        result = {
            "valid": True,
            "warnings": [],
            "score": 1.0
        }
        
        if not title:
            result["valid"] = False
            result["warnings"].append("Título vazio")
            result["score"] = 0.0
            return result
        
        if len(title) < 10:
            result["warnings"].append("Título muito curto")
            result["score"] -= 0.3
        
        if len(title) > 300:
            result["warnings"].append("Título muito longo")
            result["score"] -= 0.2
        
        if title.isupper():
            result["warnings"].append("Título em maiúsculas")
            result["score"] -= 0.1
        
        if title.islower():
            result["warnings"].append("Título em minúsculas")
            result["score"] -= 0.1
        
        if not any(c.isupper() for c in title):
            result["warnings"].append("Título sem maiúsculas")
            result["score"] -= 0.1
        
        result["score"] = max(0.0, result["score"])
        result["valid"] = result["score"] >= 0.7
        
        return result
    
    def validate_author_list(self, authors: List) -> Dict:
        """Valida lista de autores"""
        result = {
            "valid": True,
            "warnings": [],
            "score": 1.0
        }
        
        if not authors:
            result["valid"] = False
            result["warnings"].append("Sem autores")
            result["score"] = 0.0
            return result
        
        if len(authors) > 100:
            result["warnings"].append("Número excessivo de autores")
            result["score"] -= 0.2
        
        for author in authors:
            if isinstance(author, str):
                if len(author) < 3:
                    result["warnings"].append(f"Autor com nome muito curto: {author}")
                    result["score"] -= 0.1
        
        result["score"] = max(0.0, result["score"])
        result["valid"] = result["score"] >= 0.7
        
        return result
    
    def validate_abstract(self, abstract: str) -> Dict:
        """Valida abstract"""
        result = {
            "valid": True,
            "warnings": [],
            "score": 1.0
        }
        
        if not abstract:
            result["valid"] = False
            result["warnings"].append("Sem abstract")
            result["score"] = 0.0
            return result
        
        if len(abstract) < 100:
            result["warnings"].append("Abstract muito curto")
            result["score"] -= 0.3
        
        if len(abstract) > 5000:
            result["warnings"].append("Abstract muito longo")
            result["score"] -= 0.2
        
        if abstract.count('.') < 3:
            result["warnings"].append("Abstract com poucas sentenças")
            result["score"] -= 0.2
        
        result["score"] = max(0.0, result["score"])
        result["valid"] = result["score"] >= 0.7
        
        return result
    
    def validate_date(self, date_str: str) -> Dict:
        """Valida data de publicação"""
        from datetime import datetime
        
        result = {
            "valid": True,
            "warnings": [],
            "score": 1.0
        }
        
        if not date_str:
            result["warnings"].append("Sem data")
            result["score"] -= 0.3
            return result
        
        try:
            year = int(str(date_str)[:4])
            current_year = datetime.now().year
            
            if year < 1900:
                result["warnings"].append("Ano muito antigo")
                result["score"] -= 0.3
            
            if year > current_year + 1:
                result["warnings"].append("Ano no futuro")
                result["score"] -= 0.5
            
        except:
            result["warnings"].append("Formato de data inválido")
            result["score"] -= 0.3
        
        result["score"] = max(0.0, result["score"])
        result["valid"] = result["score"] >= 0.7
        
        return result
    
    def comprehensive_validate(self, article: Dict) -> Dict:
        """Validação abrangente"""
        return {
            "article_id": article.get("id") or article.get("doi", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "title": self.validate_title_structure(article.get("title", "")),
            "authors": self.validate_author_list(article.get("authors", [])),
            "abstract": self.validate_abstract(article.get("abstract") or article.get("summary", "")),
            "date": self.validate_date(article.get("published") or article.get("publication_year")),
            "doi": self._validate_doi_format(article.get("doi", "")),
            "urls": self._validate_urls(article)
        }
    
    def _validate_doi_format(self, doi: str) -> Dict:
        """Valida formato DOI"""
        result = {"valid": True, "warnings": [], "score": 1.0}
        
        if not doi:
            result["warnings"].append("Sem DOI")
            result["score"] = 0.5
            return result
        
        doi_pattern = r"^10\.\d{4,}/[^\s]+$"
        if not re.match(doi_pattern, doi):
            result["valid"] = False
            result["warnings"].append("DOI com formato inválido")
            result["score"] = 0.0
        
        return result
    
    def _validate_urls(self, article: Dict) -> Dict:
        """Valida URLs presentes no artigo"""
        result = {"valid": True, "warnings": [], "score": 1.0}
        
        url_fields = ["pdf_url", "url", "ee"]
        urls_found = []
        
        for field in url_fields:
            url = article.get(field)
            if url:
                urls_found.append(url)
                if not url.startswith(("http://", "https://")):
                    result["warnings"].append(f"URL inválida em {field}")
                    result["score"] -= 0.2
        
        if not urls_found:
            result["warnings"].append("Sem URLs")
            result["score"] -= 0.3
        
        result["score"] = max(0.0, result["score"])
        result["valid"] = result["score"] >= 0.7
        
        return result