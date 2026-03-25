# MASWOS V5 NEXUS - Plataformas de Dados com Acesso via MCPs

## Resumo das Fontes de Dados

| Categoria | Quantidade |
|-----------|------------|
| **APIs Acadêmicas** | 18+ |
| **APIs Governamentais Brasileiras** | 15+ |
| **APIs Jurídicas Brasileiras** | 4+ |
| **Dados Geoespaciais** | 9+ |
| **Organizações Internacionais** | 15+ |
| **TOTAL** | **60+ plataformas** |

---

## 1. APIs ACADÊMICAS INTERNACIONAIS

### 1.1 arXiv (Preprints)
| Item | Valor |
|------|-------|
| **URL** | http://export.arxiv.org/api/query |
| **Documentação** | https://info.arxiv.org/help/api/basics.html |
| **Acesso** | Gratuito, sem API key |
| **Rate Limit** | 1 request/3 segundos |
| **Conteúdo** | ~2M preprints (Física, Matemática, CS, etc.) |
| **Scraper** | `arxiv_official_scraper.py` |

### 1.2 PubMed / NCBI E-utilities
| Item | Valor |
|------|-------|
| **URL** | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ |
| **Documentação** | https://www.ncbi.nlm.nih.gov/books/NBK25501/ |
| **Acesso** | Gratuito, API key opcional (melhor rate limit) |
| **Rate Limit** | 3 req/s (sem key), 10 req/s (com key) |
| **Conteúdo** | ~35M artigos biomédicos |
| **Scraper** | `ncbi_official_scraper.py` |

### 1.3 Europe PMC
| Item | Valor |
|------|-------|
| **URL** | https://www.ebi.ac.uk/europepmc/webservices/rest/ |
| **Documentación** | https://www.ebi.ac.uk/europepmc/webservices/rest/search |
| **Acesso** | Gratuito, sem API key |
| **Conteúdo** | ~37M artigos (biomédicos + life sciences) |
| **Scraper** | Integrado em `advanced_scraping_engine.py` |

### 1.4 Semantic Scholar
| Item | Valor |
|------|-------|
| **URL** | https://api.semanticscholar.org/graph/v1/ |
| **Documentación** | https://api.semanticscholar.org/ |
| **Acesso** | Gratuito (sem key) ou com API key (maior rate limit) |
| **Rate Limit** | 100 req/5min (sem key), 1 req/s (com key) |
| **Conteúdo** | ~200M papers, 160M+ autores |
| **Scraper** | `semantic_scholar_scraper.py` |

### 1.5 DOAJ (Directory of Open Access Journals)
| Item | Valor |
|------|-------|
| **URL** | https://doaj.org/api/v4/ |
| **Documentación** | https://doaj.org/api/v4/docs |
| **Acesso** | Gratuito, sem API key |
| **Conteúdo** | ~21K periódicos open access, milhões de artigos |
| **Scraper** | `doaj_scraper.py` |

### 1.6 CORE
| Item | Valor |
|------|-------|
| **URL** | https://api.core.ac.uk/v3/ |
| **Documentación** | https://api.core.ac.uk/docs/v3 |
| **Acesso** | Requer API key gratuita |
| **Registro** | https://core.ac.uk/services/api |
| **Rate Limit** | 1 req/10s (search), 10 req/10s (article get) |
| **Conteúdo** | ~300M papers OA de repositórios mundiais |
| **Scraper** | `core_api_scraper.py` |

### 1.7 OpenAlex
| Item | Valor |
|------|-------|
| **URL** | https://api.openalex.org/ |
| **Documentación** | https://docs.openalex.org/ |
| **Acesso** | Gratuito, sem API key |
| **Conteúdo** | ~250M works, ~12M autores, ~120K venues |
| **Status** | Integrado via fallback |

### 1.8 CrossRef
| Item | Valor |
|------|-------|
| **URL** | https://api.crossref.org/ |
| **Documentación** | https://api.crossref.org/documentation |
| **Acesso** | Gratuito, sem API key (mas polite pool recomendado) |
| **Conteúdo** | ~150M metadados de DOIs |
| **Status** | Integrado via fallback |

### 1.9 AMiner / Open Academic Graph (China)
| Item | Valor |
|------|-------|
| **URL** | https://datacenter.aminer.cn/gateway/open_platform/ |
| **Documentación** | https://open.aminer.cn/open/doc |
| **Acesso** | Requer API token gratuito |
| **Registro** | https://open.aminer.cn/open/board?tab=control |
| **Conteúdo** | ~300M papers, ~160M scholars, ~600K venues |
| **Scraper** | `aminer_scraper.py` |

### 1.10 CNKI (知网 - China)
| Item | Valor |
|------|-------|
| **URL** | https://kns.cnki.net/ |
| **API Oficial** | Requer parceria institucional |
| **Acesso Alternativo** | Web scraping limitado |
| **Conteúdo** | Maior banco de dados acadêmico da China |
| **Scraper** | `cnki_scraper.py` (limitado) |

### 1.11 Elsevier Scopus (opcional)
| Item | Valor |
|------|-------|
| **URL** | https://api.elsevier.com/content/search/scopus |
| **Documentación** | https://dev.elsevier.com |
| **Acesso** | Requer API key + assinatura institucional |
| **Conteúdo** | ~85M registros, metadados + citações |

### 1.12 Springer Nature (opcional)
| Item | Valor |
|------|-------|
| **URL** | https://api.springernature.com/ |
| **Documentación** | https://dev.springernature.com/ |
| **Acesso** | Requer API key gratuita |
| **Registro** | https://dev.springernature.com/signup |
| **Conteúdo** | ~14M documentos (journals, books, protocols) |

### 1.13 CAPES - Portal de Periódicos (Brasil)
| Item | Valor |
|------|-------|
| **URL** | https://dadosabertos.capes.gov.br |
| **API CKAN** | https://dadosabertos.capes.gov.br/api/3/action |
| **Documentación** | https://dadosabertos.capes.gov.br |
| **Acesso** | Gratuito, Creative Commons CC BY |
| **Conteúdo** | 241M+ acessos (2023), 460M+ (2024) |
| **Dados** | Acessos por UF, IES, Município, Região |
| **Scraper** | `capes_scraper.py` |

### 1.14 OpenReview (Conferências AI)
| Item | Valor |
|------|-------|
| **URL** | https://openreview.net/ |
| **API** | https://api.openreview.net/ |
| **Acesso** | Gratuito, sem API key |
| **Conteúdo** | 50+ conferências (NeurIPS, ICLR, ICML, etc.) |
| **Scraper** | `chinese_academic_apis.py` |

### 1.15 Internet Archive
| Item | Valor |
|------|-------|
| **URL** | https://archive.org/ |
| **API** | https://archive.org/advancedsearch.php |
| **Acesso** | Gratuito, sem API key |
| **Conteúdo** | 40M+ itens, 800B+ páginas web arquivadas |
| **Scraper** | `internet_archive_scraper.py` |

---

## 2. APIs GOVERNAMENTAIS BRASILEIRAS

### 2.1 IBGE (Instituto Brasileiro de Geografia e Estatística)
| Item | Valor |
|------|-------|
| **URL** | https://servicos.ibge.gov.br/api/ |
| **APIs** | Censo, SIDRA, Agregados, Localidades |
| **Documentación** | https://servicos.ibge.gov.br/api/docs |
| **Acesso** | Gratuito |
| **Conteúdo** | Demografia, economia, malhas territoriais |

### 2.2 dados.gov.br (Portal de Dados Abertos)
| Item | Valor |
|------|-------|
| **URL** | https://dados.gov.br/api/ |
| **Documentación** | https://dados.gov.br/dados/conjuntos-dados |
| **Acesso** | Requer autenticação para API completa |
| **Registro** | https://dados.gov.br/usuario/registrar |
| **Conteúdo** | ~15K datasets governamentais |
| **Scraper** | `dados_gov_scraper.py` |

### 2.3 IPEA (Instituto de Pesquisa Econômica Aplicada)
| Item | Valor |
|------|-------|
| **URL** | https://www.ipeadata.gov.br/api/odata4/ |
| **Documentación** | https://www.ipeadata.gov.br/api |
| **Acesso** | Gratuito (OData) |
| **Conteúdo** | Séries temporais econômicas e sociais |

### 2.4 DATASUS
| Item | Valor |
|------|-------|
| **URL** | https://datasus.saude.gov.br/ |
| **Conteúdo** | Dados de saúde, morbidade, mortalidade |
| **Acesso** | Downloads em lotes, sem API REST formal |

### 2.5 Banco Central do Brasil (BCB)
| Item | Valor |
|------|-------|
| **URL** | https://olinda.bcb.gov.br/olinda/servico/BCB/ |
| **Documentación** | https://github.com/bcb-varejo/olinda |
| **Acesso** | Gratuito |
| **Conteúdo** | Séries financeiras, câmbio, Selic, inflation |

### 2.6 INEP (Instituto Nacional de Estudos e Pesquisas)
| Item | Valor |
|------|-------|
| **URL** | https://www.gov.br/inep/pt-br |
| **Conteúdo** | Educação: ENEM, SAEB, Prova Brasil, censo escolar |
| **Acesso** | Downloads em CSV/Excel |

### 2.7 CNJ (Conselho Nacional de Justiça)
| Item | Valor |
|------|-------|
| **URL** | https://www.cnj.jus.br/ |
| **Conteúdo** | Estatísticas judiciais, movimento processual |
| **Acesso** | Dados abertos, alguns endpoints |

---

## 3. APIs JURÍDICAS BRASILEIRAS

### 3.1 LexML (Legislação)
| Item | Valor |
|------|-------|
| **URL** | https://www.lexml.gov.br/ |
| **API** | https://www.lexml.gov.br/api/ |
| **Acesso** | Gratuito |
| **Conteúdo** | Legislação federal, estadual, municipal |

### 3.2 STF (Supremo Tribunal Federal)
| Item | Valor |
|------|-------|
| **URL** | https://portal.stf.jus.br/ |
| **API** | https://transparencia.stf.jus.br/single/?appid=635fc59d-1f41-4a5e-8b43-f2e0d0e8e4fe |
| **Conteúdo** | Jurisprudência, processos, pautas |

### 3.3 STJ (Superior Tribunal de Justiça)
| Item | Valor |
|------|-------|
| **URL** | https://www.stj.jus.br/ |
| **Conteúdo** | Jurisprudência, súmulas, processos |

### 3.4 TST (Tribunal Superior do Trabalho)
| Item | Valor |
|------|-------|
| **URL** | https://www.tst.jus.br/ |
| **Conteúdo** | Jurisprudência trabalhista |

---

## 4. DADOS GEOSPACIAIS

### 4.1 INPE (Instituto Nacional de Pesquisas Espaciais)
| Item | Valor |
|------|-------|
| **URL** | https://www.inpe.br/ |
| **Conteúdo** | Imagens de satélite, monitoramento de queimadas (PRODES, DETER) |
| **Acesso** | Downloads abertos |

### 4.2 EMBRAPA (Empresa Brasileira de Pesquisa Agropecuária)
| Item | Valor |
|------|-------|
| **URL** | https://www.embrapa.br/ |
| **Conteúdo** | Dados agropecuários, solos, clima |

### 4.3 MapBiomas
| Item | Valor |
|------|-------|
| **URL** | https://mapbiomas.org/ |
| **API** | https://code.earthengine.google.com/?asset=projects/mapbiomas-workspace/public |
| **Conteúdo** | Uso e cobertura do solo, séries temporais |

### 4.4 Copernicus / Sentinel
| Item | Valor |
|------|-------|
| **URL** | https://scihub.copernicus.eu/ |
| **API** | https://scihub.copernicus.eu/dhus/ |
| **Acesso** | Gratuito com registro |
| **Conteúdo** | Imagens Sentinel-1, 2, 3, 5P |

### 4.5 USGS Earth Explorer (Landsat)
| Item | Valor |
|------|-------|
| **URL** | https://earthexplorer.usgs.gov/ |
| **Acesso** | Gratuito com registro |
| **Conteúdo** | Imagens Landsat históricas (desde 1972) |

### 4.6 NASA MODIS
| Item | Valor |
|------|-------|
| **URL** | https://modis.gsfc.nasa.gov/ |
| **Acesso** | Gratuito |
| **Conteúdo** | Dados de vegetação, temperatura, incêndios |

### 4.7 World Bank Open Data
| Item | Valor |
|------|-------|
| **URL** | https://api.worldbank.org/ |
| **Documentación** | https://datahelpdesk.worldbank.org/knowledgebase/topics/125589 |
| **Acesso** | Gratuito (JSON, XML, JSONP) |
| **Conteúdo** | Indicadores econômicos de 200+ países |

### 4.8 Natural Earth
| Item | Valor |
|------|-------|
| **URL** | https://www.naturalearthdata.com/ |
| **Conteúdo** | Vetores geopolíticos, relevo, hidrografia |
| **Acesso** | Downloads gratuitos (SHP, GeoJSON) |

### 4.9 OpenStreetMap
| Item | Valor |
|------|-------|
| **URL** | https://www.openstreetmap.org/ |
| **API** | https://api.openstreetmap.org/ |
| **Conteúdo** | Dados vetoriais crowdsourced mundiais |

---

## 5. OUTRAS FONTES

### 5.1 Wikipedia / Wikidata
| Item | Valor |
|------|-------|
| **URL** | https://www.wikidata.org/wiki/Wikidata:Data_access |
| **API** | https://www.wikidata.org/w/api.php |
| **Acesso** | Gratuito |
| **Conteúdo** | Entidades, relações, conhecimento estruturado |

### 5.2 GitHub API
| Item | Valor |
|------|-------|
| **URL** | https://api.github.com/ |
| **Documentación** | https://docs.github.com/en/rest |
| **Acesso** | Gratuito (rate limit: 60 req/h sem auth) |
| **Conteúdo** | Repositórios, código, issues, releases |

### 5.3 Kaggle Datasets
| Item | Valor |
|------|-------|
| **URL** | https://www.kaggle.com/api/v1/ |
| **Acesso** | Requer API key (conta gratuita) |
| **Conteúdo** | ~50K datasets públicos |

---

## RESUMO DE CONFIGURAÇÃO DE API KEYS

```bash
# Acadêmicas
export CORE_API_KEY="registrar em https://core.ac.uk/services/api"
export AMINER_API_KEY="registrar em https://open.aminer.cn/open/board?tab=control"
export SEMANTIC_SCHOLAR_API_KEY="opcional em https://www.semanticscholar.org/product/api"

# Brasileiras  
export DADOS_GOV_API_KEY="registrar em https://dados.gov.br/usuario/registrar"

# Geoespaciais
export COPERNICUS_USER="registrar em https://scihub.copernicus.eu/"
export COPERNICUS_PASSWORD="sua_senha"
export KAGGLE_USERNAME="registrar em https://www.kaggle.com"
export KAGGLE_KEY="sua_api_key"
```

---

## STATUS DE ACESSO

| Plataforma | API Key | Status Scraping |
|------------|---------|-----------------|
| arXiv | Não | ✅ Funcional |
| PubMed | Opcional | ✅ Funcional |
| Europe PMC | Não | ✅ Funcional |
| Semantic Scholar | Opcional | ✅ Funcional |
| DOAJ | Não | ✅ Funcional |
| CORE | Sim | ✅ Funcional |
| OpenAlex | Não | ✅ Funcional |
| CrossRef | Não | ✅ Funcional |
| AMiner | Sim | ✅ Funcional |
| CNKI | Institucional | ⚠️ Limitado |
| IBGE | Não | ✅ Funcional |
| dados.gov.br | Sim | ⚠️ Limitado |
| IPEA | Não | ✅ Funcional |
| BCB | Não | ✅ Funcional |
| World Bank | Não | ✅ Funcional |
| Sentinel | Sim | ✅ Funcional |
| Landsat | Sim | ✅ Funcional |

---

---

## 6. ORGANIZAÇÕES INTERNACIONAIS

### 6.1 World Bank (Banco Mundial)
| Item | Valor |
|------|-------|
| **URL** | https://api.worldbank.org/v2/ |
| **Documentación** | https://datahelpdesk.worldbank.org/knowledgebase/topics/125589 |
| **Acesso** | Gratuito, sem API key |
| **Conteúdo** | 14K+ indicadores de 200+ países |
| **Scraper** | `international_organizations_scraper.py` |

**Exemplos de endpoints:**
```
# PIB do Brasil
https://api.worldbank.org/v2/country/BRA/indicator/NY.GDP.MKTP.CD?format=json

# Lista de países
https://api.worldbank.org/v2/country?format=json

# Lista de indicadores
https://api.worldbank.org/v2/indicator?format=json
```

### 6.2 United Nations SDGs (Objetivos de Desenvolvimento Sustentável)
| Item | Valor |
|------|-------|
| **URL** | https://unstats.un.org/SDGAPI/v1/ |
| **Documentación** | https://unstats.un.org/SDGAPI/swagger/index.html |
| **Acesso** | Gratuito, sem API key |
| **Conteúdo** | 17 objetivos, 232 indicadores |
| **Scraper** | `international_organizations_scraper.py` |

**Exemplos de endpoints:**
```
# Lista de objetivos
https://unstats.un.org/SDGAPI/v1/sdg/Goal/List

# Metas do Objetivo 1
https://unstats.un.org/SDGAPI/v1/sdg/Goal/1/Target/List

# Indicadores
https://unstats.un.org/SDGAPI/v1/sdg/Goal/4/Indicator/List
```

### 6.3 UN Data (Dados da ONU)
| Item | Valor |
|------|-------|
| **URL** | https://data.un.org/ |
| **API** | https://data.un.org/Host.aspx?Content=API |
| **Acesso** | Gratuito |
| **Conteúdo** | Estatísticas globais (população, economia, saúde, etc.) |

### 6.4 UNICEF Statistics
| Item | Valor |
|------|-------|
| **URL** | https://data.unicef.org/ |
| **API** | https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/ |
| **Documentación** | https://sdmx.data.unicef.org/ws/public/sdmxapi/docs/ |
| **Acesso** | Gratuito (SDMX) |
| **Conteúdo** | Dados de infância e juventude |

### 6.5 WHO (World Health Organization / OMS)
| Item | Valor |
|------|-------|
| **URL** | https://ghoapi.azureedge.net/api/ |
| **Documentación** | https://www.who.int/data/gho/info/gho-odata-api |
| **Acesso** | Gratuito (OData) |
| **Conteúdo** | 2000+ indicadores de saúde mundial |
| **Scraper** | `international_organizations_scraper.py` |

**Exemplos de endpoints:**
```
# Lista de indicadores
https://ghoapi.azureedge.net/api/Indicator

# Esperança de vida Brasil
https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq 'BRA'
```

### 6.6 UNESCO Institute for Statistics
| Item | Valor |
|------|-------|
| **URL** | https://api.unesco.org/ |
| **Documentación** | https://apiportal.uis.unesco.org/ |
| **Acesso** | Requer API key (gratuito) |
| **Registro** | https://apiportal.uis.unesco.org/ |
| **Conteúdo** | Educação, ciência, cultura, comunicação |
| **Scraper** | `international_organizations_scraper.py` |

### 6.7 IMF (Fundo Monetário Internacional)
| Item | Valor |
|------|-------|
| **URL** | http://dataservices.imf.org/REST/SDMX_JSON.svc/ |
| **Documentación** | https://www.imf.org/en/Data/Data-Services |
| **Acesso** | Gratuito |
| **Conteúdo** | Dados financeiros, PIB, inflação, balança comercial |
| **Scraper** | `international_organizations_scraper.py` |

**Exemplos de endpoints:**
```
# PIB growth Brazil
http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/BR.NGDP_RPCH?startPeriod=2010&endPeriod=2023
```

### 6.8 OECD (Organização para Cooperação e Desenvolvimento Econômico)
| Item | Valor |
|------|-------|
| **URL** | https://stats.oecd.org/SDMX-JSON/data/ |
| **Documentación** | https://stats.oecd.org/index.aspx?queryid=30116 |
| **Acesso** | Gratuito |
| **Conteúdo** | Dados econômicos de países desenvolvidos |

### 6.9 FAO (Organização das Nações Unidas para Alimentação e Agricultura)
| Item | Valor |
|------|-------|
| **URL** | https://fenixservices.fao.org/faostat/api/v1/ |
| **Documentación** | https://www.fao.org/faostat/en/#data |
| **Acesso** | Gratuito |
| **Conteúdo** | Agricultura, alimentação, uso do solo |
| **Scraper** | `international_organizations_scraper.py` |

### 6.10 ILO (Organização Internacional do Trabalho)
| Item | Valor |
|------|-------|
| **URL** | https://ilostat.ilo.org/data/api/ |
| **Documentación** | https://ilostat.ilo.org/data/api/docs/ |
| **Acesso** | Gratuito (alguns dados requerem registro) |
| **Conteúdo** | Trabalho, emprego, trabalho infantil |

### 6.11 UNHCR (Alto Comissariado das Nações Unidas para Refugiados)
| Item | Valor |
|------|-------|
| **URL** | https://api.unhcr.org/population/v1/ |
| **Documentación** | https://developer.unhcr.org/ |
| **Acesso** | Requer registro |
| **Conteúdo** | Refugiados, deslocados, apátridas |

### 6.12 World Food Programme (WFP)
| Item | Valor |
|------|-------|
| **URL** | https://api.hungermapdata.org/v2/ |
| **Documentación** | https://api.hungermapdata.org/ |
| **Acesso** | Gratuito |
| **Conteúdo** | Segurança alimentar global |

### 6.13 OCDE Data (dados complementares)
| Item | Valor |
|------|-------|
| **URL** | https://stats.oecd.org/ |
| **API** | https://sdmx.oecd.org/public/rest/data/ |
| **Acesso** | Gratuito |
| **Conteúdo** | Educação, economia, inovação, meio ambiente |

### 6.14 World Intellectual Property Organization (WIPO)
| Item | Valor |
|------|-------|
| **URL** | https://www3.wipo.int/ipstats/ |
| **Conteúdo** | Patentes, marcas, propriedade intelectual |

### 6.15 International Monetary Fund - Expanded
| Item | Valor |
|------|-------|
| **URL** | https://www.imf.org/en/Publications/SPROLLs/compass#/ |
| **API** | http://dataservices.imf.org/REST/SDMX_JSON.svc/ |
| **Conteúdo** | Finanças, balança de pagamentos, dívida externa |

---

## 7. OUTRAS FONTES GLOBAIS

### 7.1 Gapminder
| Item | Valor |
|------|-------|
| **URL** | https://www.gapminder.org/data/ |
| **API** | https://www.gapminder.org/freeapi/ |
| **Acesso** | Gratuito |
| **Conteúdo** | Dados históricos de desenvolvimento |

### 7.2 Our World in Data
| Item | Valor |
|------|-------|
| **URL** | https://ourworldindata.org/ |
| **GitHub** | https://github.com/owid/ |
| **Acesso** | Dados no GitHub (CSV, JSON) |
| **Conteúdo** | Visualizações de dados globais |

### 7.3 Human Development Reports (UNDP)
| Item | Valor |
|------|-------|
| **URL** | https://hdr.undp.org/data-center |
| **Conteúdo** | Índice de Desenvolvimento Humano (IDH) |
| **Acesso** | Downloads gratuitos |

### 7.4 Transparency International
| Item | Valor |
|------|-------|
| **URL** | https://www.transparency.org/ |
| **Conteúdo** | Índice de Percepção de Corrupção |
| **Acesso** | Dados abertos |

### 7.5 Freedom House
| Item | Valor |
|------|-------|
| **URL** | https://freedomhouse.org/ |
| **Conteúdo** | Freedom in the World, Internet Freedom |
| **Acesso** | Dados abertos |

### 7.6 World Happiness Report
| Item | Valor |
|------|-------|
| **URL** | https://worldhappiness.report/ |
| **Dados** | https://github.com/ajaypal1990/World_Indices_Repo |
| **Conteúdo** | Felicidade global por país |

### 7.7 Global Burden of Disease (IHME)
| Item | Valor |
|------|-------|
| **URL** | https://vizhub.healthdata.org/gbd-results/ |
| **API** | https://ghdx.healthdata.org/ |
| **Acesso** | Gratuito com registro |
| **Conteúdo** | Carga de doenças global |

---

## RESUMO COMPLETO DE CONFIGURAÇÃO

```bash
# Organizações Internacionais (todas gratuitas ou com registro gratuito)
# World Bank, UN SDG, WHO, FAO, ILO, IMF, OECD - sem API key necessária

# UNESCO - requer registro
export UNESCO_API_KEY="registrar em https://apiportal.uis.unesco.org/"

# UNHCR - requer registro  
export UNHCR_API_KEY="registrar em https://developer.unhcr.org/"
```

---

**Total de fontes de dados disponíveis: 45+ plataformas**
