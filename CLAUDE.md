# Claude Instructions: Steering Monitorability Project

## Project overview
Research on CoT monitorability. Three deliverables: D1 (annotated reasoning trace dataset, month 1), D2 (steering + SFT + prompting paper, month 3), D3 (latent reasoning model paper, month 4). Core paradigm: cue-mention faithfulness detection. Primary eval metric: arXiv:2510.27378.

Collaborators: Eitan Sprejer (you're working with him) + Austin (first author) + Gerard (new collaborator, ICML paper on white-box monitor leakage).

## Key files
- `ref/PROTOCOL.md` -- seed papers, inclusion/exclusion criteria, output format, PDF/S2 workflow
- `research/lit_review/STATUS.md` -- current status, findings summary, next steps. READ THIS at the start of each session.
- `research/lit_review/tier1_*/findings.md` -- per-area literature review results
- `research/lit_review/D1_BRIEF.md` -- D1 dataset design brief
- `research/model_organisms/PLAN.md` -- model organisms vibe-check plan
- `research/model_organisms/discovery_table.md` -- 28 organisms, ranked, availability verified
- `research/model_organisms/taxonomy_research.md` -- literature-grounded misalignment taxonomy
- `ref/project_proposal_original.md` -- full grant proposal
- `ref/meetings/` -- meeting notes and transcripts
- `.env` -- API keys (SEMANTIC_SCHOLAR_API)

## External resources
- Preexisting Datasets spreadsheet: online Google Sheets (in shared Drive folder)

## Repos in this workspace
- `petri/` -- Petri framework (github.com/safety-research/petri), builds on Inspect, adversarial trace generation
- `petri_transcript_gen_test/` -- Austin's test repo for generating traces with Petri

## Literature review tools

**Reading papers -- use section files (context-efficient):**
- Sections: `research/lit_review/pdfs/sections/{arXiv_id}/` -- one file per section (e.g. `related_work.txt`, `references.txt`)
- Check `research/lit_review/pdfs/sections/{arXiv_id}/index.txt` first to see what sections exist
- Full text fallback: `research/lit_review/pdfs/txt/{arXiv_id}.txt`
- All 61 papers are split into sections already

**Do NOT use marker-pdf** (slow ML). Prefer section files > full txt > fetching from arXiv.

**Semantic Scholar API** (for citation trails):
```bash
source .env
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}/references?fields=title,year,authors,externalIds&limit=100" -H "x-api-key: $SEMANTIC_SCHOLAR_API"
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}/citations?fields=title,year,authors,externalIds&limit=100" -H "x-api-key: $SEMANTIC_SCHOLAR_API"
```

**Adding a new paper:**
```bash
# Download PDF
curl -sL "https://arxiv.org/pdf/{id}.pdf" -o "research/lit_review/pdfs/raw/{id}.pdf"
# Extract text
python3 -c "from pdftext.extraction import plain_text_output; open('research/lit_review/pdfs/txt/{id}.txt','w').write(plain_text_output('research/lit_review/pdfs/raw/{id}.pdf', sort=True))"
```

**Slash command:** `/literature-review <topic>` -- runs a full search for a new sub-area.

## Conventions
- All agents that write files must be **general-purpose** type, not Explore (Explore agents lack Write/Edit tools)
- When appending to a `findings.md`, add a new dated section header, never overwrite
- Screening decisions: include a one-line reason for each exclusion
- Use `source .env` before any S2 API calls
- Never run more than 1-2 marker processes in parallel (very CPU-intensive). Prefer pdftext instead.

## Current state (update this as work progresses)
- Tier 1 lit review: DONE (second pass complete, S2 citation trails, ~86 papers total)
  - tier1_misalignment_taxonomy: 23 papers
  - tier1_cot_faithfulness: 31 papers
  - tier1_reward_hacking_adjacent: 32 papers
- Tier 2 (steering methods) and Tier 3 (latent reasoning): NOT STARTED
- PDFs: 61 papers in `research/lit_review/pdfs/`, text extracted to `research/lit_review/pdfs/txt/`
- Synthesis: DONE -- `research/lit_review/synthesis/synthesis.md` + `research/lit_review/synthesis/master_table.md`
- Next: generate CoT faithfulness pilot traces with Petri; sentence-level tagging pilot
