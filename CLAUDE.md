# Claude Instructions: Steering Monitorability Project

## Project overview
Research on CoT monitorability. Three deliverables: D1 (annotated reasoning trace dataset, month 1), D2 (steering + SFT + prompting paper, month 3), D3 (latent reasoning model paper, month 4). Primary eval metric: arXiv:2510.27378.

Collaborators: Eitan Sprejer (you're working with him) + Austin (first author) + Gerard (collaborator, ICML paper on white-box monitor leakage).

## Current state (updated 2026-03-24)

**READ `research/pipeline/PIPELINE_DESIGN.md` for the full trace generation process.**

### Trace generation pipeline (validated)
The pipeline combines Bloom (scenario generation) + Petri (rollout with tools, realism, judging):
1. Write DEFINITIONS.md for the misalignment mode (template in `research/OPERATIONALIZATION_FRAMEWORK.md`)
2. Feed definitions to Bloom Understanding + Ideation (generates diverse scenarios)
3. Convert Bloom scenarios to Petri seeds
4. Run Petri (Sonnet 4.6 auditor, DeepSeek R1 target, Qwen 72B judge, realism filter)
5. View with `inspect view`, annotate, human review

**v0.2 completed (reward hacking):** 5 scenarios, 0% elicitation. Root causes: max_turns=8 too low, no feedback loop, no exploitable specification. Full analysis in `research/pipeline/runs/reward_hacking_20260324_103345/REPORT.md`.

**v0.3 running (reward hacking):** max_turns=24, seeds instruct auditor to provide negative evaluative feedback and create exploitable tool outputs.

### Active workstreams
- **Reward hacking: ACTIVE.** Pivoted from faithfulness after v0.1. v0.2 identified 6 root causes. v0.3 addresses the top 4. Optimization loop: iterate DEFINITIONS.md + seeds + config until elicitation works.
- **CoT faithfulness: ON PROBATION.** v0.1 showed model handles cue-based scenarios faithfully. Will revisit after reward hacking pipeline is working.
- **Scheming pilot:** Definitions done. Deferred until pipeline is producing traces for at least one mode.
- **Sycophancy (Gerard's):** Working independently. Code at `petri_transcript_gen_test/scripts/custom_sycophancy/` (boxo_branch).
- **Model organisms:** 6 Tier 1 confirmed, ~675 vibe-check traces, 39 D1-batch traces.

### Key decisions (2026-03-20 meeting + 2026-03-24 work)
- Pipeline is mode-agnostic. All mode-specific info lives in DEFINITIONS.md.
- Petri is the rollout framework (has tools, realism, judging). Gerard's CoT tools may be added later.
- Bloom generates scenarios, Petri executes them.
- Multi-agent conversation traces are D1's differentiator.
- The optimization loop (run -> analyze root causes -> fix -> rerun) is the core workflow now.

## Key files

### Planning and status
- `research/WORKPLAN.md` -- **current sprint plan** (source of truth for what to do next)
- `research/reports/2026-03-17_cot-faithfulness-pilot.md` -- progress report (pushed to GitHub)
- `ref/meetings/` -- meeting notes (latest: 2026-03-20)

### Definitions (the "common knowledge" for trace generation)
- `research/OPERATIONALIZATION_FRAMEWORK.md` -- reusable template for defining any misalignment type
- `research/reward_hacking_pilot/DEFINITIONS.md` -- reward hacking subtypes (3 defined, active)
- `research/cot_faithfulness_pilot/DEFINITIONS.md` -- CoT faithfulness subtypes (4 defined, on probation)
- `research/scheming_pilot/DEFINITIONS.md` -- scheming subtypes (4 defined, literature-grounded)

### Model organisms
- `research/model_organisms/vibe_checks/README.md` -- vibe-check report (authoritative for organism status)
- `research/model_organisms/discovery_table.md` -- 28 organisms catalogued (rankings superseded by README.md Section 7)
- `research/model_organisms/vibe_checks/d1_transcripts/` -- 39 D1-batch traces

### Literature review
- `research/lit_review/STATUS.md` -- lit review status (Tier 1 done, ~86 papers)
- `research/lit_review/synthesis/synthesis.md` -- synthesis document
- `research/lit_review/wave1_new_papers.md` -- 6 new papers from Wave 1 search
- `ref/PROTOCOL.md` -- search/screening methodology

### CoT faithfulness pilot (legacy, on probation)
- `research/cot_faithfulness_pilot/LOG.md` -- detailed research log with human calibration
- `research/cot_faithfulness_pilot/run_audits.py` -- Petri-based trace generation
- `research/cot_faithfulness_pilot/annotate.py` -- LLM annotation pipeline
- `research/cot_faithfulness_pilot/visualize.py` -- HTML report generator
- `research/cot_faithfulness_pilot/seeds/` -- v1 (used in runs) + v2 (redesigned, untested)

### Gerard's sycophancy pipeline (independent)
- `petri_transcript_gen_test/scripts/custom_sycophancy/sycophancy_inspect.py` -- main pipeline with CoT intervention tools
- `petri_transcript_gen_test/scripts/custom_sycophancy/cot_prefill_inspect.py` -- CoT prefilling experiments
- `petri_transcript_gen_test/scripts/custom_sycophancy/escalation_prompts.py` -- persona/scenario definitions

### Other
- `ref/project_proposal_original.md` -- full grant proposal
- `.env` -- API keys (SEMANTIC_SCHOLAR_API, OPENROUTER_API_KEY)

## External resources
- Preexisting Datasets spreadsheet: online Google Sheets (in shared Drive folder)
- Bloom: github.com/safety-research/bloom (automated behavioral evaluations)

## Repos in this workspace
- `petri/` -- Petri framework (github.com/safety-research/petri), builds on Inspect
- `petri_transcript_gen_test/` -- Austin's test repo. Gerard's sycophancy code on `boxo_branch`.

## Literature review tools

**Reading papers -- use section files (context-efficient):**
- Sections: `research/lit_review/pdfs/sections/{arXiv_id}/` -- one file per section
- Check `research/lit_review/pdfs/sections/{arXiv_id}/index.txt` first
- Full text fallback: `research/lit_review/pdfs/txt/{arXiv_id}.txt`

**Do NOT use marker-pdf** (slow ML). Prefer section files > full txt > fetching from arXiv.

**Semantic Scholar API** (for citation trails):
```bash
source .env
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}/references?fields=title,year,authors,externalIds&limit=100" -H "x-api-key: $SEMANTIC_SCHOLAR_API"
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}/citations?fields=title,year,authors,externalIds&limit=100" -H "x-api-key: $SEMANTIC_SCHOLAR_API"
```

**Adding a new paper:**
```bash
curl -sL "https://arxiv.org/pdf/{id}.pdf" -o "research/lit_review/pdfs/raw/{id}.pdf"
python3 -c "from pdftext.extraction import plain_text_output; open('research/lit_review/pdfs/txt/{id}.txt','w').write(plain_text_output('research/lit_review/pdfs/raw/{id}.pdf', sort=True))"
```

**Slash command:** `/literature-review <topic>` -- runs a full search for a new sub-area.

## Conventions
- All agents that write files must be **general-purpose** type, not Explore (Explore agents lack Write/Edit tools)
- When appending to a `findings.md`, add a new dated section header, never overwrite
- Screening decisions: include a one-line reason for each exclusion
- Use `source .env` before any S2 API calls
- Never run more than 1-2 marker processes in parallel. Prefer pdftext instead.
