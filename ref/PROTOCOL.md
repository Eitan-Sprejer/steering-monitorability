# Literature Review Protocol

## Project Overview

**Title:** Steering Models Towards Safer Reasoning
**Goal:** Dataset of annotated aligned/misaligned reasoning traces (D1), then a steering paper comparing steering vs. SFT vs. prompting baselines (D2), then latent reasoning control/monitoring (D3).
**Core paradigm:** CoT faithfulness via cue-mention detection. The hypothesis is that subtle long-context behaviors (faithfulness, sandbagging) are unlikely to be linearly steerable, so we test manifold-based and attention-based methods alongside classical activation steering.

## Deliverables & Timeline

| Deliverable | Description | Month |
|---|---|---|
| D1 | Dataset of annotated reasoning traces covering misalignment modes | 1 |
| D2 | Paper on steering + SFT + prompting baselines | 3 |
| D3 | Paper on latent reasoning model control/monitoring | 4 |

## Known Seed Papers

These are already identified -- do not re-summarize, but do follow their citation trails.

### Core project papers
- `2510.27378` -- CoT monitorability benchmark (main eval metric)
- `2506.18167`, `2409.14026` -- Steering reasoning models
- `2510.07364` -- Sentence-level tagging of reasoning traces
- `2503.08679` -- Faithful reasoning in the wild (rarely found)
- `2505.05410`, `2305.04388`, `2501.08156` -- CoT faithfulness paradigm and metrics
- `2510.04040` -- FaithCoT-Bench (fine-grained faithful CoT step labels)
- `2508.20151` -- IntentionReasoner (query-level safety classification + rewriting, 163k queries; NOT a reasoning trace dataset -- Austin's grant doc citation was incorrect)

### Steering / representation engineering
- `2308.10248` -- Activation addition (classical steering)
- `2506.13734` -- Attention boosting
- `2505.22411` -- Manifold steering for long context
- `2507.22928` -- Mechanistic interp + CoT behavior
- `2311.03658` -- Linear Representation Hypothesis
- `2405.14860`, `2506.10920` -- Latent manifolds in activation space

### Baselines
- `2411.04430` -- Prompting without coherence harm
- `2506.22777` -- Verbalization fine-tuning (SFT baseline)

### Evaluation benchmarks
- `2503.03750` -- MASK (honesty vs. beliefs)
- `2510.15501` -- DeceptionBench
- `2304.03279` -- MACHIAVELLI (power-seeking / oversight-avoidance)

### Existing datasets
- MALT: https://metr.org/blog/2025-10-14-malt-dataset-of-natural-and-prompted-behaviors/
- OpenAI CoT monitoring: https://openai.com/index/chain-of-thought-monitoring/
- OpenAI evaluating CoT monitorability: https://openai.com/index/evaluating-chain-of-thought-monitorability/

### Latent reasoning models
- `2412.06769` -- COCONUT
- `2502.21074` -- CODI
- LMent: `2509.03405`
- Apertus: `2509.14233`

## Sub-areas for Tier 1 (Dataset Design)

| Folder | Topic |
|---|---|
| `tier1_misalignment_taxonomy` | What types of misaligned reasoning exist; taxonomies; existing datasets (MALT, etc.); what's missing |
| `tier1_cot_faithfulness` | CoT faithfulness definitions, metrics, benchmarks; cue-mention paradigm; faithful reasoning in the wild |
| `tier1_reward_hacking_adjacent` | Reward hacking, sandbagging, deceptive/strategic reasoning -- adjacent literature not necessarily framed as CoT faithfulness |

## Inclusion Criteria

- Directly relevant to: CoT faithfulness, misaligned reasoning, behavioral evaluation of reasoning models
- OR relevant to: steering/representation engineering for reasoning, evaluation benchmarks for alignment
- Publication 2022-present (reasoning model era); preprints fine
- Papers from adjacent fields (reward hacking, deception, sandbagging) are in-scope if they have a reasoning trace or behavioral angle

## Exclusion Criteria

- Pure capability/benchmark papers with no safety or alignment relevance
- General NLP faithfulness work not applicable to reasoning-scale models
- Medical/clinical systematic review tooling

## Semantic Scholar API

API key is in `.env` as `SEMANTIC_SCHOLAR_API`. Use for structured citation data.

**Get all references of a paper** (papers it cites):
```bash
source .env
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}/references?fields=title,year,authors,externalIds&limit=100" \
  -H "x-api-key: $SEMANTIC_SCHOLAR_API"
```

**Get citations of a paper** (newer papers that cite it):
```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}/citations?fields=title,year,authors,externalIds&limit=100" \
  -H "x-api-key: $SEMANTIC_SCHOLAR_API"
```

Use S2 references to do second passes on key papers without needing to parse PDFs. The `externalIds.ArXiv` field gives the arXiv ID for any referenced paper. Rate limit with API key: 100 req/sec.

## PDF Storage & Full-Text Access

All included papers are stored as PDFs with plain-text extraction for full-text reading.

**Paths:**
- PDFs: `lit_review/pdfs/{arXiv_id}.pdf`
- Text (fast): `lit_review/pdfs/txt/{arXiv_id}.txt` -- use this for reading papers
- Sections (preferred): `lit_review/pdfs/sections/{arXiv_id}/` -- one file per section

**Download and extract a new paper:**
```bash
# Download
curl -sL "https://arxiv.org/pdf/{id}.pdf" -o "lit_review/pdfs/{id}.pdf"
# Extract text (pdftext -- fast, no ML, ~1 second per paper)
python3 -c "from pdftext.extraction import plain_text_output; open('lit_review/pdfs/txt/{id}.txt','w').write(plain_text_output('lit_review/pdfs/{id}.pdf', sort=True))"
```

**Section splitting (arXiv HTML):** Fetch `arxiv.org/html/{id}`, extract `ltx_section` and `ltx_bibliography` CSS classes via BeautifulSoup, write one file per section with a slug-ified filename. Creates `index.txt` listing all filenames. Falls back to txt-only if no HTML available (404).

```python
import requests, re, os
from bs4 import BeautifulSoup

def html_to_text(elem):
    for tag in elem.find_all(['script', 'style']): tag.decompose()
    t = elem.get_text(separator=' ', strip=True)
    t = re.sub(r'\(\s*(\d{4})\s*\)', r'(\1)', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def split_paper(arxiv_id, out_dir):
    if os.path.exists(out_dir) and os.path.exists(f"{out_dir}/index.txt"):
        return  # already split
    url = f"https://arxiv.org/html/{arxiv_id}"
    r = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code != 200:
        return  # no HTML, use txt fallback
    soup = BeautifulSoup(r.text, 'html.parser')
    sections = soup.find_all('section', class_='ltx_section')
    refs = soup.find_all(class_='ltx_bibliography')
    if not sections and not refs:
        return
    os.makedirs(out_dir, exist_ok=True)
    index = []
    for sec in sections:
        h = sec.find(['h1','h2','h3','h4'])
        title = h.get_text(strip=True) if h else 'unknown'
        safe = re.sub(r'[^\w\s-]','', title.lower()).strip().replace(' ','_')[:50]
        fname = f"{safe}.txt"
        open(f"{out_dir}/{fname}", 'w').write(html_to_text(sec))
        index.append(fname)
    for ref_sec in refs:
        open(f"{out_dir}/references.txt", 'w').write(html_to_text(ref_sec))
        index.append("references.txt")
    open(f"{out_dir}/index.txt", 'w').write('\n'.join(index))
```

**Reading papers (preferred):** Use section-split files. Read `index.txt` first to see what sections exist, then read only what you need. If no `sections/` directory exists, fall back to `txt/`.

**Full text fallback:** `lit_review/pdfs/txt/{id}.txt` has the complete paper as plain text.

**Note on marker-pdf:** Installed but very slow (runs OCR models). Do not use for batch conversion. pdftext is the preferred extraction tool.

**Master table:** The synthesis document at `lit_review/synthesis/master_table.md` tracks all included papers with arXiv ID, topic category, relevance to D1/D2/D3, and local PDF path.

## Output Format Per Paper

Each entry in `findings.md` should follow this template:

```
### [Title](arxiv_or_url)
**Authors, Year** | `arXiv:XXXX.XXXXX`

**Relevance:** 1-3 sentences on why this matters for the project.

**Key findings:**
- ...
- ...

**Gap/limitation:** What it doesn't cover that we still need.

**Tags:** [taxonomy | cot_faithfulness | reward_hacking | steering | sft | latent_reasoning | evaluation | dataset]
```

Each `findings.md` should also include a header section with:
- Date searched
- Queries used
- Total papers found / screened / included
- Notable gaps observed
