#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - NCBI Official Scraper
Scraper baseado nas APIs oficiais do NCBI conforme documentação:
- E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- PMC APIs: https://pmc.ncbi.nlm.nih.gov/tools/developers/
- BLAST REST: https://blast.ncbi.nlm.nih.gov/doc/blast-help/developerinfo.html

Arquitetura: Transformer-Agentes (Encoder → API → Parser → Decoder)
"""

import requests
import time
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@dataclass
class NCBIDocument:
    """Documento NCBI padronizado"""
    pmid: str = ""
    pmcid: str = ""
    doi: str = ""
    title: str = ""
    abstract: str = ""
    authors: List[str] = field(default_factory=list)
    journal: str = ""
    pub_date: str = ""
    keywords: List[str] = field(default_factory=list)
    citations: int = 0
    license: str = ""
    source: str = ""
    full_text_url: str = ""

class EUtilitiesClient:
    """
    Cliente oficial para E-utilities do NCBI
    
    Documentação: https://www.ncbi.nlm.nih.gov/books/NBK25501/
    
    Rate Limits:
    - Sem API key: 1 request/3 segundos
    - Com API key: 10 requests/segundo (3 requests/segundo sem e-mail)
    """
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    def __init__(self, api_key: Optional[str] = None, email: Optional[str] = None, 
                 tool_name: str = "maswos_scraper"):
        self.api_key = api_key
        self.email = email
        self.tool_name = tool_name
        self.last_request_time = 0
        self.min_interval = 0.34 if api_key else 3.34  # segundos entre requests
        
    def _rate_limit(self):
        """Aplicar rate limiting conforme guidelines NCBI"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
    
    def _build_params(self, **kwargs) -> Dict:
        """Construir parâmetros comum"""
        params = {"retmode": "json", "tool": self.tool_name}
        if self.api_key:
            params["api_key"] = self.api_key
        if self.email:
            params["email"] = self.email
        params.update(kwargs)
        return params
    
    def esearch(self, db: str, term: str, retmax: int = 20, 
                usehistory: bool = True) -> Dict:
        """
        ESearch - Buscar UIDs no Entrez
        
        Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/#chapter4.ESearch
        
        Args:
            db: Banco de dados (pubmed, pmc, nuccore, etc.)
            term: Termo de busca
            retmax: Máximo de resultados
            usehistory: Usar servidor de histórico
        
        Returns:
            Dict com IdList, Count, WebEnv, QueryKey
        """
        self._rate_limit()
        
        params = self._build_params(
            db=db,
            term=term,
            retmax=retmax,
            usehistory="y" if usehistory else "n"
        )
        
        url = f"{self.BASE_URL}esearch.fcgi"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        esearchresult = data.get("esearchresult", {})
        
        return {
            "ids": esearchresult.get("idlist", []),
            "count": int(esearchresult.get("count", 0)),
            "webenv": esearchresult.get("webenv", ""),
            "querykey": esearchresult.get("querykey", ""),
            "retmax": retmax
        }
    
    def esummary(self, db: str, ids: List[str] = None, 
                 webenv: str = None, querykey: str = None,
                 retstart: int = 0, retmax: int = 20) -> Dict:
        """
        ESummary - Recuperar Document Summaries
        
        Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/#chapter4.ESummary
        
        Args:
            db: Banco de dados
            ids: Lista de UIDs
            webenv: Web Environment do ESearch
            querykey: Query Key do ESearch
            retstart: Início da paginação
            retmax: Máximo de resultados
        
        Returns:
            Dict com resumos dos documentos
        """
        self._rate_limit()
        
        params = self._build_params(db=db, retstart=retstart, retmax=retmax)
        
        if ids:
            params["id"] = ",".join(ids)
        elif webenv and querykey:
            params["WebEnv"] = webenv
            params["query_key"] = querykey
        
        url = f"{self.BASE_URL}esummary.fcgi"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        result = data.get("result", {})
        
        documents = []
        uids = result.get("uids", [])
        for uid in uids:
            doc_data = result.get(uid, {})
            if doc_data:
                documents.append({
                    "uid": uid,
                    "title": doc_data.get("title", ""),
                    "authors": [a.get("name", "") for a in doc_data.get("authors", [])],
                    "source": doc_data.get("source", ""),
                    "pubdate": doc_data.get("pubdate", ""),
                    "doi": doc_data.get("articleids", [{}])[0].get("value", "") if doc_data.get("articleids") else "",
                    "citations": doc_data.get("citedbycount", 0)
                })
        
        return {
            "documents": documents,
            "count": len(documents)
        }
    
    def efetch(self, db: str, ids: List[str] = None,
               webenv: str = None, querykey: str = None,
               retstart: int = 0, retmax: int = 20,
               rettype: str = "xml", retmode: str = "xml") -> str:
        """
        EFetch - Recuperar dados formatados
        
        Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/#chapter4.EFetch
        
        Args:
            db: Banco de dados
            ids: Lista de UIDs
            webenv: Web Environment
            querykey: Query Key
            retstart: Início da paginação
            retmax: Máximo de resultados
            rettype: Tipo de retorno (xml, abstract, fasta, etc.)
            retmode: Modo de retorno (xml, text, json)
        
        Returns:
            Dados formatados (XML, texto, etc.)
        """
        self._rate_limit()
        
        params = self._build_params(
            db=db,
            retstart=retstart,
            retmax=retmax,
            rettype=rettype,
            retmode=retmode
        )
        
        if ids:
            params["id"] = ",".join(ids)
        elif webenv and querykey:
            params["WebEnv"] = webenv
            params["query_key"] = querykey
        
        url = f"{self.BASE_URL}efetch.fcgi"
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        
        return response.text
    
    def elink(self, dbfrom: str, db: str, ids: List[str],
              linkname: str = None, cmd: str = "neighbor") -> Dict:
        """
        ELink - Encontrar links entre registros
        
        Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/#chapter4.ELink
        
        Args:
            dbfrom: Banco de origem
            db: Banco de destino
            ids: Lista de UIDs
            linkname: Nome do link específico
            cmd: Comando (neighbor, neighbor_history, etc.)
        
        Returns:
            Dict com links encontrados
        """
        self._rate_limit()
        
        params = self._build_params(
            dbfrom=dbfrom,
            db=db,
            id=",".join(ids),
            cmd=cmd
        )
        
        if linkname:
            params["linkname"] = linkname
        
        url = f"{self.BASE_URL}elink.fcgi"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # Parse XML response
        try:
            root = ET.fromstring(response.text)
            links = []
            for linkset in root.findall(".//LinkSet"):
                source_id = linkset.findtext(".//IdList/Id", "")
                for link in linkset.findall(".//Link/Id"):
                    links.append({
                        "source_id": source_id,
                        "target_id": link.text or ""
                    })
            return {"links": links, "count": len(links)}
        except:
            return {"links": [], "count": 0}
    
    def einfo(self, db: str = None) -> Dict:
        """
        EInfo - Obter informações sobre bancos de dados
        
        Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/#chapter4.EInfo
        
        Args:
            db: Banco de dados (None para listar todos)
        
        Returns:
            Dict com informações do banco
        """
        self._rate_limit()
        
        params = self._build_params()
        if db:
            params["db"] = db
        
        url = f"{self.BASE_URL}einfo.fcgi"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        return response.json()


class PMCApiClient:
    """
    Cliente para APIs oficiais do PMC
    
    Documentação: https://pmc.ncbi.nlm.nih.gov/tools/developers/
    
    APIs Disponíveis:
    - OA Service: Dados de artigos Open Access
    - OAI-PMH: Metadados e texto completo
    - BioC: Full text em BioC format
    - PMC ID Converter: Conversão de identificadores
    - Literature Citation Exporter: Citações formatadas
    """
    
    def __init__(self):
        self.cache_dir = Path(".ncbi_cache")
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_oa_data(self, pmcid: str) -> Optional[Dict]:
        """
        OA Service - Dados de artigo Open Access
        
        Base URL: https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi
        
        Args:
            pmcid: PMC ID (ex: PMC123456)
        
        Returns:
            Dict com dados do artigo ou None
        """
        url = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"
        params = {"id": pmcid, "format": "xml"}
        
        try:
            response = requests.get(url, params=params, timeout=30, verify=False)
            if response.status_code == 200:
                # Parse OA response
                root = ET.fromstring(response.text)
                article = root.find(".//article")
                if article is not None:
                    return self._parse_oa_article(article)
        except Exception as e:
            print(f"[OA ERROR] {e}")
        
        return None
    
    def get_oai_pmh_metadata(self, pmcid: str) -> Optional[Dict]:
        """
        OAI-PMH Service - Metadados via OAI Protocol
        
        Base URL: https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/
        
        Args:
            pmcid: PMC ID
        
        Returns:
            Dict com metadados Dublin Core
        """
        base_url = "https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/"
        params = {
            "verb": "GetRecord",
            "identifier": f"oai:pmc.ncbi.nlm.nih.gov:{pmcid}",
            "metadataPrefix": "pmc"
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30, verify=False)
            if response.status_code == 200:
                return self._parse_oai_response(response.text)
        except Exception as e:
            print(f"[OAI ERROR] {e}")
        
        return None
    
    def get_bioc_fulltext(self, pmcid: str) -> Optional[Dict]:
        """
        BioC API - Full text em BioC format
        
        Base URL: https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi
        
        Args:
            pmcid: PMC ID
        
        Returns:
            Dict com texto completo estruturado
        """
        url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/bioc/{pmcid}/json"
        
        try:
            response = requests.get(url, timeout=60, verify=False)
            if response.status_code == 200:
                data = response.json()
                return self._parse_bioc_response(data)
        except Exception as e:
            print(f"[BioC ERROR] {e}")
        
        return None
    
    def convert_ids(self, ids: List[str], source_type: str = "pmcid",
                    target_types: List[str] = None) -> Dict:
        """
        PMC ID Converter - Converter entre tipos de ID
        
        Base URL: https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/
        
        Args:
            ids: Lista de IDs
            source_type: Tipo de ID (pmcid, pmid, doi, etc.)
            target_types: Tipos de ID desejados
        
        Returns:
            Dict com IDs convertidos
        """
        if target_types is None:
            target_types = ["pmcid", "pmid", "doi"]
        
        url = "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/"
        params = {
            "ids": ",".join(ids),
            "format": "json",
            "ids_type": source_type
        }
        
        try:
            response = requests.get(url, params=params, timeout=30, verify=False)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[ID Converter ERROR] {e}")
        
        return {}
    
    def get_citation(self, pmid: str, format: str = "medline") -> Optional[str]:
        """
        Literature Citation Exporter - Obter citação formatada
        
        Base URL: https://pmc.ncbi.nlm.nih.gov/api/ctxp/
        
        Args:
            pmid: PubMed ID
            format: Formato (medline, ris, apa, etc.)
        
        Returns:
            Citação formatada
        """
        url = f"https://pmc.ncbi.nlm.nih.gov/api/ctxp/v1/pubmed/{pmid}"
        params = {"format": format}
        
        try:
            response = requests.get(url, params=params, timeout=30, verify=False)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"[Citation ERROR] {e}")
        
        return None
    
    def _parse_oa_article(self, article) -> Dict:
        """Parser para artigo OA"""
        return {
            "title": article.findtext(".//title-group/article-title", ""),
            "abstract": self._extract_abstract(article),
            "authors": self._extract_authors(article),
            "journal": article.findtext(".//journal-title", ""),
            "pub_date": self._extract_pub_date(article),
            "license": article.findtext(".//license", "")
        }
    
    def _parse_oai_response(self, xml_text: str) -> Dict:
        """Parser para resposta OAI-PMH"""
        try:
            root = ET.fromstring(xml_text)
            metadata = root.find(".//{http://www.openarchives.org/OAI/2.0/}metadata")
            if metadata is not None:
                return {
                    "title": metadata.findtext(".//title", ""),
                    "authors": [a.text for a in metadata.findall(".//creator") if a.text],
                    "date": metadata.findtext(".//date", ""),
                    "publisher": metadata.findtext(".//publisher", "")
                }
        except:
            pass
        return {}
    
    def _parse_bioc_response(self, data: Dict) -> Dict:
        """Parser para resposta BioC"""
        documents = data.get("documents", [])
        if documents:
            doc = documents[0]
            passages = doc.get("passages", [])
            
            sections = {}
            for passage in passages:
                section_type = passage.get("infons", {}).get("section_type", "other")
                text = passage.get("text", "")
                sections[section_type] = sections.get(section_type, "") + " " + text
            
            return {
                "title": sections.get("TITLE", "").strip(),
                "abstract": sections.get("ABSTRACT", "").strip(),
                "body": sections.get("BODY", "").strip(),
                "sections": sections
            }
        return {}
    
    def _extract_abstract(self, article) -> str:
        """Extrair abstract do artigo"""
        abstract_parts = article.findall(".//abstract/abstract-section")
        if abstract_parts:
            return " ".join([p.text or "" for p in abstract_parts])
        return article.findtext(".//abstract", "")
    
    def _extract_authors(self, article) -> List[str]:
        """Extrair autores"""
        authors = []
        for author in article.findall(".//contrib-group/contrib[@contrib-type='author']"):
            surname = author.findtext(".//name/surname", "")
            given = author.findtext(".//name/given-names", "")
            if surname:
                authors.append(f"{surname}, {given}".strip(", "))
        return authors
    
    def _extract_pub_date(self, article) -> str:
        """Extrair data de publicação"""
        pub_date = article.find(".//pub-date[@pub-type='epub']")
        if pub_date is None:
            pub_date = article.find(".//pub-date")
        
        if pub_date is not None:
            year = pub_date.findtext("year", "")
            month = pub_date.findtext("month", "")
            day = pub_date.findtext("day", "")
            parts = [p for p in [year, month, day] if p]
            return "-".join(parts)
        return ""


class NCBIOfficialScraper:
    """
    Scraper oficial integrado usando APIs NCBI
    
    Integra E-utilities e PMC APIs conforme documentação oficial
    """
    
    def __init__(self, api_key: Optional[str] = None, email: Optional[str] = None):
        self.eutils = EUtilitiesClient(api_key, email)
        self.pmc = PMCApiClient()
        self.cache = {}
    
    def search_articles(self, query: str, db: str = "pubmed", 
                        max_results: int = 20, with_fulltext: bool = False) -> List[NCBIDocument]:
        """
        Buscar artigos com pipeline completo
        
        Pipeline: ESearch → ESummary → EFetch (→ BioC para fulltext)
        
        Args:
            query: Termo de busca
            db: Banco de dados
            max_results: Máximo de resultados
            with_fulltext: Incluir texto completo via BioC
        
        Returns:
            Lista de NCBIDocument
        """
        documents = []
        
        # 1. ESearch - Buscar IDs
        print(f"[NCBI] ESearch: '{query}' em {db}")
        search_result = self.eutils.esearch(db, query, retmax=max_results)
        
        if not search_result["ids"]:
            print("[NCBI] Nenhum resultado encontrado")
            return documents
        
        print(f"[NCBI] Encontrados {search_result['count']} artigos")
        
        # 2. ESummary - Resumos
        print(f"[NCBI] ESummary: recuperando resumos...")
        summaries = self.eutils.esummary(
            db, 
            ids=search_result["ids"][:max_results]
        )
        
        # 3. EFetch - Detalhes completos (XML)
        print(f"[NCBI] EFetch: recuperando detalhes...")
        xml_data = self.eutils.efetch(
            db,
            ids=search_result["ids"][:max_results],
            rettype="xml",
            retmode="xml"
        )
        
        # 4. Parse XML
        documents = self._parse_efetch_xml(xml_data)
        
        # 5. Fulltext via BioC (se solicitado e disponível)
        if with_fulltext:
            print("[NCBI] BioC: recuperando textos completos...")
            for doc in documents[:5]:  # Limite para não sobrecarregar
                if doc.pmcid:
                    bioc_data = self.pmc.get_bioc_fulltext(doc.pmcid)
                    if bioc_data:
                        doc.full_text_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{doc.pmcid}/"
        
        return documents
    
    def search_by_pmid(self, pmids: List[str]) -> List[NCBIDocument]:
        """Buscar artigos por PMID"""
        if not pmids:
            return []
        
        xml_data = self.eutils.efetch("pubmed", ids=pmids, rettype="xml", retmode="xml")
        return self._parse_efetch_xml(xml_data)
    
    def get_cited_by(self, pmid: str, max_results: int = 20) -> List[NCBIDocument]:
        """Obter artigos que citam um PMID específico"""
        # ELink para obter IDs que citam
        links = self.eutils.elink("pubmed", "pubmed", [pmid], linkname="pubmed_pubmed", cmd="neighbor")
        
        if not links["links"]:
            return []
        
        cited_ids = [l["target_id"] for l in links["links"][:max_results]]
        return self.search_by_pmid(cited_ids)
    
    def get_references(self, pmid: str, max_results: int = 20) -> List[NCBIDocument]:
        """Obter referências de um artigo"""
        # ELink para obter IDs referenciados
        links = self.eutils.elink("pubmed", "pubmed", [pmid], linkname="pubmed_pubmed", cmd="neighbor")
        
        if not links["links"]:
            return []
        
        ref_ids = [l["target_id"] for l in links["links"][:max_results]]
        return self.search_by_pmid(ref_ids)
    
    def convert_to_pmc(self, pmids: List[str]) -> Dict:
        """Converter PMIDs para PMCIDs"""
        return self.pmc.convert_ids(pmids, source_type="pmid", target_types=["pmcid", "doi"])
    
    def _parse_efetch_xml(self, xml_data: str) -> List[NCBIDocument]:
        """Parser completo para EFetch XML"""
        documents = []
        
        try:
            # EFetch retorna PubMedArticleSet
            root = ET.fromstring(xml_data)
            
            for article in root.findall(".//PubmedArticle"):
                doc = NCBIDocument()
                
                # PMID
                doc.pmid = article.findtext(".//PMID", "")
                
                # Article IDs (PMCID, DOI)
                for id_elem in article.findall(".//ArticleIdList/ArticleId"):
                    id_type = id_elem.get("IdType", "")
                    if id_type == "pmc":
                        doc.pmcid = id_elem.text or ""
                    elif id_type == "doi":
                        doc.doi = id_elem.text or ""
                
                # Título
                doc.title = article.findtext(".//ArticleTitle", "")
                
                # Abstract
                abstract_parts = article.findall(".//Abstract/AbstractText")
                if abstract_parts:
                    doc.abstract = " ".join([p.text or "" for p in abstract_parts])
                
                # Autores
                for author in article.findall(".//AuthorList/Author"):
                    surname = author.findtext("LastName", "")
                    forename = author.findtext("ForeName", "")
                    if surname:
                        doc.authors.append(f"{surname}, {forename}".strip(", "))
                
                # Journal
                doc.journal = article.findtext(".//Journal/ISOAbbreviation", "")
                if not doc.journal:
                    doc.journal = article.findtext(".//Journal/Title", "")
                
                # Data de publicação
                pub_date = article.find(".//Journal/JournalIssue/PubDate")
                if pub_date is not None:
                    year = pub_date.findtext("Year", "")
                    month = pub_date.findtext("Month", "")
                    day = pub_date.findtext("Day", "")
                    doc.pub_date = "-".join([p for p in [year, month, day] if p])
                
                # Citações
                citation_list = article.find(".//ReferenceList")
                if citation_list is not None:
                    doc.citations = len(citation_list.findall(".//Reference"))
                
                # Keywords
                for kw in article.findall(".//MeshHeadingList/MeshHeading/DescriptorName"):
                    if kw.text:
                        doc.keywords.append(kw.text)
                
                doc.source = "NCBI_EFetch"
                documents.append(doc)
                
        except Exception as e:
            print(f"[PARSE ERROR] {e}")
        
        return documents


# Funções de conveniência
def search_pubmed(query: str, max_results: int = 20, 
                  api_key: str = None) -> List[NCBIDocument]:
    """Função simplificada para busca PubMed"""
    scraper = NCBIOfficialScraper(api_key=api_key)
    return scraper.search_articles(query, db="pubmed", max_results=max_results)

def search_pmc(query: str, max_results: int = 20,
               with_fulltext: bool = True) -> List[NCBIDocument]:
    """Função simplificada para busca PMC com fulltext"""
    scraper = NCBIOfficialScraper()
    return scraper.search_articles(query, db="pmc", max_results=max_results, 
                                   with_fulltext=with_fulltext)

def get_article_by_pmid(pmid: str) -> Optional[NCBIDocument]:
    """Obter artigo específico por PMID"""
    scraper = NCBIOfficialScraper()
    results = scraper.search_by_pmid([pmid])
    return results[0] if results else None


# Testes
def test_ncbi_official_scraper():
    """Testar scraper oficial NCBI"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - NCBI Official Scraper Test")
    print("=" * 70)
    
    scraper = NCBIOfficialScraper()
    
    # Teste 1: ESearch
    print("\n[TEST 1] ESearch - Buscar artigos sobre machine learning")
    search_result = scraper.eutils.esearch(
        "pubmed",
        "machine learning diagnosis",
        retmax=5
    )
    print(f"  Encontrados: {search_result['count']} artigos")
    print(f"  IDs recuperados: {len(search_result['ids'])}")
    
    # Teste 2: Busca completa
    print("\n[TEST 2] Busca completa com EFetch")
    articles = scraper.search_articles(
        "artificial intelligence cancer",
        db="pubmed",
        max_results=3
    )
    
    for i, article in enumerate(articles[:3], 1):
        print(f"\n  Artigo {i}:")
        print(f"    PMID: {article.pmid}")
        print(f"    Título: {article.title[:80]}...")
        print(f"    Autores: {', '.join(article.authors[:3])}...")
        print(f"    Journal: {article.journal}")
        print(f"    Data: {article.pub_date}")
    
    # Teste 3: PMC API
    print("\n[TEST 3] PMC ID Converter")
    conversion = scraper.pmc.convert_ids(["PMC5540579"], source_type="pmcid")
    print(f"  Conversão: {conversion}")
    
    print("\n" + "=" * 70)
    print("NCBI Official Scraper - Testes Concluídos")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_ncbi_official_scraper()