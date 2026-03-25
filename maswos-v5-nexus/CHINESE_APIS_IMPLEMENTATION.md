# MASWOS V5 NEXUS - Chinese Academic APIs Implementation

## Summary

Comprehensive implementation of Chinese academic APIs with focus on free/open access platforms.

## Implemented Scrapers

### 1. AMiner/Open Academic Graph (`aminer_scraper.py`)

**Status**: ✅ Implemented

**Platform**: AMiner Open Platform (清华大学)
- 300M+ papers, 160M+ scholars, 600K+ venues
- Includes Open Academic Graph (OAG)

**API**: https://open.aminer.cn/open/doc
**Token**: https://open.aminer.cn/open/board?tab=control

---

### 2. OpenReview (`chinese_academic_apis.py` - OpenReviewScraper)

**Status**: ✅ Implemented

**Platform**: OpenReview - Open peer review platform
- 50+ top AI/ML conferences (ICLR, NeurIPS, ICML, AAAI, ACL, CVPR)
- Full paper text + peer reviews available
- 100% free, no API key required

**API**: https://api2.openreview.net
**Docs**: https://docs.openreview.net/

**Conferências disponíveis**:
| Conferência | Domain |
|-------------|--------|
| ICLR 2025 | ICLR.cc/2025/Conference |
| NeurIPS 2024 | NeurIPS.cc/2024 |
| ICML 2024 | ICML.cc/2024/Conference |
| AAAI 2024 | AAAI.org/2024 |
| ACL 2024 | ACLweb.org/ACL/2024 |

---

### 3. OpenAlex China (`chinese_academic_apis.py` - OpenAlexChinaScraper)

**Status**: ✅ Implemented

**Platform**: OpenAlex with China filter
- 450M+ papers total, incluindo milhões de papers chineses
- 100% free, CC0 license

**API**: https://api.openalex.org
**Docs**: https://docs.openalex.org/

**Estatísticas chinesas**:
- Chinese Academy of Sciences: 973,672 papers
- Peking University: 378,842 papers
- Tsinghua University: 363,067 papers

---

### 4. SciEngine (`chinese_academic_apis.py` - SciEngineScraper)

**Status**: ✅ Implemented (journals list only)

**Platform**: Science Press China (科学出版社)
- 200+ journals open access
- Science China series (Mathematics, Chemistry, Physics, Life Sciences)

**API**: https://www.sciengine.com/
**Access**: Free registration for OA content

---

### 5. CNKI (`cnki_scraper.py` + `chinese_academic_apis.py`)

**Status**: ⚠️ Limited (requires institutional access)

**Platform**: China National Knowledge Infrastructure
- Largest academic database in China
- Requires institutional partnership for full API access

**Web**: https://kns.cnki.net

---

## Other Chinese Academic APIs

### 6. Wanfang Data (万方数据)
- **Website**: https://www.wanfangdata.com.cn
- **Access**: Subscription-based, limited free via registration
- **Coverage**: Theses, patents, journals, standards
- **API**: Requires partnership

### 7. CQVIP (重庆维普)
- **Website**: https://www.cqvip.com
- **Access**: Library-focused
- **Coverage**: Technical journals, 12,000+ Chinese journals

### 8. CSTPCD (中国科技论文与引文数据库)
- **Website**: Part of Wanfang
- **Coverage**: China Science and Technology Paper Citation Database
- **Access**: Institutional only

### 9. National Science Library (NSTL)
- **Website**: https://www.nstl.gov.cn
- **Coverage**: National science and technology literature
- **Access**: Some open resources

### 10. ChinaXiv (中国科学院科技论文预发布平台)
- **Website**: https://chinaxiv.org
- **Coverage**: Preprints from Chinese Academy of Sciences
- **Access**: Free (preprint server like arXiv)

### 11. National Science Data Platform (科学数据银行)
- **Website**: https://www.scidb.cn
- **Coverage**: Research data repository
- **Access**: Free registration

---

## Comprehensive Free Chinese Academic Sources

| Platform | URL | Type | Free Access |
|----------|-----|------|-------------|
| **OpenAlex (China filter)** | https://api.openalex.org | Papers | ✅ Full |
| **AMiner** | https://open.aminer.cn | Papers, Scholars | ✅ Token required |
| **OpenReview** | https://api2.openreview.net | Conferences | ✅ Full |
| **ChinaXiv** | https://chinaxiv.org | Preprints | ✅ Full |
| **SciEngine OA** | https://www.sciengine.com | Journals | ✅ OA journals |
| **CNKI (limited)** | https://kns.cnki.net | Papers | ⚠️ Institutional |
| **Wanfang** | https://wanfangdata.com.cn | Papers | ⚠️ Limited free |
| **CQVIP** | https://www.cqvip.com | Journals | ⚠️ Limited free |
| **Science Data Bank** | https://www.scidb.cn | Research Data | ✅ Free |

---

## Key Chinese Universities in OpenAlex

| University | Papers | 
|------------|--------|
| Chinese Academy of Sciences | 973,672 |
| Peking University | 378,842 |
| University of Chinese Academy of Sciences | 368,139 |
| Tsinghua University | 363,067 |
| Zhejiang University | 356,619 |
| Shanghai Jiao Tong University | 320,000+ |
| Fudan University | 280,000+ |
| University of Science and Technology of China | 250,000+ |
| Nanjing University | 220,000+ |
| Wuhan University | 200,000+ |

---

## Usage Examples

```python
# OpenAlex - Papers chineses
from chinese_academic_apis import OpenAlexChinaScraper

scraper = OpenAlexChinaScraper()
result = scraper.search_chinese_papers("machine learning", year=2024, limit=50)

# OpenReview - ICLR 2025 papers
from chinese_academic_apis import OpenReviewScraper

scraper = OpenReviewScraper()
papers = scraper.get_submissions("ICLR.cc/2025/Conference", limit=100)

# AMiner - Papers + Citations
from aminer_scraper import AMinerScraper

scraper = AMinerScraper(api_token="seu_token")
papers = scraper.search_papers("深度学习", limit=50)
```

---

## Files Created

| File | Description |
|------|-------------|
| `chinese_academic_apis.py` | OpenReview, OpenAlex China, SciEngine |
| `aminer_scraper.py` | AMiner/Open Academic Graph |
| `cnki_scraper.py` | CNKI (limited) |

---

## Recommended Strategy for Chinese Academic Research

1. **Primary**: OpenAlex (China filter) - 87K+ papers on ML from China in 2024
2. **Conferences**: OpenReview - Full papers from top AI conferences
3. **Scholars**: AMiner - Author profiles and citation networks
4. **Preprints**: ChinaXiv - Chinese preprints
5. **Paid (if available)**: CNKI, Wanfang for comprehensive coverage

---

### 2. CNKI (知网) (`cnki_scraper.py`)

**Status**: Implemented - Limited access (web scraping fallback)

**Platform**: China National Knowledge Infrastructure
- Largest academic database in China
- Requires institutional partnership for full API access
- Web scraping available for basic metadata

**Limitations**:
- No public API for non-institutional users
- Full text download requires institutional subscription
- Web scraping may be rate-limited

**Datasets Covered**:
- CDFD (中国博士学位论文全文数据库) - Doctoral theses
- CMFD (中国优秀硕士学位论文全文数据库) - Master theses  
- CJD (中国期刊全文数据库) - Journal articles
- CCND (中国重要报纸全文数据库) - Newspapers
- CCVD (中国重要会议论文全文数据库) - Conference papers

**Alternative Access**:
- East View's China Research Gateway: https://www.eastview.com
- MagicCNKI: https://github.com/1049451037/MagicCNKI
- CnkiSpider: https://github.com/zemengchuan/cnkispider

---

## Other Chinese Academic APIs (Not Implemented)

### 3. Wanfang Data (万方数据)
- **Access**: Subscription-based, limited free via registration
- **Website**: https://www.wanfangdata.com.cn
- **API**: Requires partnership or paid subscription
- **Coverage**: Theses, patents, journals, standards

### 4. CQVIP (重庆维普)
- **Access**: Library-focused, limited individual access
- **Platform**: CQVIP Chinese Journals Platform
- **Coverage**: Technical journals and literature

### 5. National Social Sciences Database (NSSD)
- **Access**: Open Access (free registration)
- **Website**: http://www.nssd.cn
- **Coverage**: Social sciences in China
- **API**: Not well documented, web access available

---

## Usage Recommendations

### For Research Projects:

1. **Best Free Option**: AMiner + Open Academic Graph
   - Register for free API token
   - 300M+ papers including Chinese publications
   - Well-documented API
   - English and Chinese support

2. **If Institutional Access Available**: CNKI
   - Most comprehensive Chinese database
   - Use institution's proxy or VPN
   - Can combine with web scraping for metadata

3. **For Social Sciences**: NSSD
   - Open access
   - Good for humanities and social sciences

### API Keys Setup:

```bash
# AMiner (register at https://open.aminer.cn/open/board?tab=control)
export AMINER_API_KEY="seu_token_aqui"
```

### Integration:

```python
from advanced_scraping_engine import AdvancedScrapingOrchestrator

# Initialize with AMiner token
orch = AdvancedScrapingOrchestrator(aminer_api_key="seu_token")

# Search Chinese academic papers
result = orch.scrape_with_fallback("AMINER", "人工智能", limit=10)
```

---

## Technical Notes

1. **Language**: Most Chinese APIs have documentation primarily in Mandarin
2. **Latency**: Servers hosted in China may have higher latency from outside
3. **Rate Limits**: Vary by API, AMiner free tier has reasonable limits
4. **Encoding**: Ensure UTF-8 encoding for Chinese queries

---

## Files Created

| File | Description |
|------|-------------|
| `aminer_scraper.py` | AMiner/Open Academic Graph scraper |
| `cnki_scraper.py` | CNKI web scraper (limited) |
| `advanced_scraping_engine.py` | Updated with AMiner integration |
| `api_validator.py` | Updated with AMiner endpoint |

---

## References

1. AMiner Open Platform: https://open.aminer.cn
2. Open Academic Graph: https://www.microsoft.com/en-us/research/project/open-academic-graph/
3. CNKI: https://www.cnki.net
4. East View China Research: https://www.eastview.com
5. MagicCNKI: https://github.com/1049451037/MagicCNKI
6. CnkiSpider: https://github.com/zemengchuan/cnkispider
