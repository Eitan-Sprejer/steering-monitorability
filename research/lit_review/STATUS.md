# Literature Review Status

## Project
**Title:** Steering Models Towards Safer Reasoning (CoT Monitorability)
**Collaborators:** Eitan Sprejer + Austin (first author)
**Timeline:** 1 month (dataset D1) → 2 months (steering paper D2) → 1 month (latent reasoning D3)

## Deliverables
| # | Output | Month |
|---|---|---|
| D1 | Dataset of annotated aligned/misaligned reasoning traces (HuggingFace) | 1 |
| D2 | Paper: steering + SFT + prompting baselines for CoT faithfulness | 3 |
| D3 | Paper: latent reasoning model control/monitoring | 4 |

## Core paradigm
CoT faithfulness via **cue-mention detection**: a trace is "unfaithful" when the model's answer is influenced by a context cue but the reasoning trace doesn't mention it. Eitan's monitorability benchmark (`arXiv:2510.27378`) is the primary eval metric.

## Files
- `PROTOCOL.md` -- seed papers, inclusion/exclusion criteria, output format, sub-area definitions
- `ref/project_proposal_original.md` -- full grant proposal with all referenced papers
- `ref/rough_notes.md` -- meeting notes (Austin + Eitan, 17/02)
- `ref/some_relevant_papers_ive_found.md` -- 3 URLs identified by Eitan

## Lit Review: What's Done

### Tier 1 (first pass 2026-02-18, second pass 2026-02-18)
First pass: Exa + arXiv API keyword search. Second pass: Semantic Scholar citation trails (API key configured, 100 req/sec limit) on 5 key papers.

| Sub-area | Folder | Papers included | Status |
|---|---|---|---|
| Misalignment taxonomy & datasets | `tier1_misalignment_taxonomy/` | 23 | Done (+1 from S2 second pass) |
| CoT faithfulness definitions & metrics | `tier1_cot_faithfulness/` | 31 | Done (+5 from S2 second pass) |
| Reward hacking & deceptive reasoning | `tier1_reward_hacking_adjacent/` | 32 | Done (+4 from S2 second pass) |

### Tier 2 (not started)
Steering/representation engineering methods, SFT baselines, eval frameworks. Needed for D2.

### Tier 3 (not started)
Latent reasoning models (COCONUT, CODI), monitoring without visible CoT. Needed for D3.

## Key Findings So Far

### Most important papers found (not in original proposal)
- `arXiv:2510.18154` -- "Annotating the Chain-of-Thought: A Behavior-Labeled Dataset for AI Safety" -- **closest existing work to D1; must read before finalizing dataset design**
- `arXiv:2508.00943` -- "LLMs Can Covertly Sandbag Against CoT Monitoring" -- most similar to project scope
- `arXiv:2503.11926` -- OpenAI "Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation" -- key paper on monitorability tax
- `arXiv:2602.15515` -- "Obfuscation Atlas" (DeepMind/ARC, 2026) -- taxonomy of obfuscation mechanisms
- `arXiv:2511.22662` -- "Difficulties with Evaluating a Deception Detector" -- critical for annotation design
- `arXiv:2506.15109` -- "Unfaithful CoT as Nudged Reasoning" (Anthropic/MATS) -- mechanistic framing of unfaithfulness

### Key gap: the differentiator for D1
No existing dataset covers multiple misalignment modes (cue-mention faithfulness, sandbagging, deception, steganography) in a **unified annotation scheme with sentence-level labels**. All existing datasets cover one mode or use coarse (trace-level) labels.

### Open question for dataset design
"Difficulties with Evaluating a Deception Detector" (arXiv:2511.22662) argues there's no reliable ground truth distinguishing *intentional* deception from hallucination. D1 likely needs to use **synthetic traces** (where intent is controlled) rather than natural traces for the deception/sandbagging modes.

### D1 data source architecture (confirmed 2026-03-09 meeting)
Three confirmed sources for ground truth reasoning traces:
1. **Naturally occurring traces** -- real model behavior in the wild
2. **Model organisms** -- misaligned models (eval awareness model org from last year; sandbagging model orgs); Austin in contact with model organism researchers
3. **Synthetic traces** -- generated via Petri/BLOOM (Austin has 13k transcripts already)

Model organism vibe-check approach: (a) does it pass vibe check? (b) does model verbalize the misalignment in a black-box setting? Note: misalignment may not always be tractable at the sentence level for model organisms.

Petri note: Austin has generated 13k transcripts; no better alternative to Petri currently. Annotation calibration will need a web GUI.

## Tier 2 Leads (from S2 second pass, not yet reviewed)

Papers found in citation trails that are relevant to Tier 2 (steering/D2) or Tier 3 (latent reasoning/D3):
- `2310.01405` -- Representation Engineering (RepE) -- D2 seed (already in PROTOCOL)
- `2502.02716` -- "A Unified Understanding and Evaluation of Steering Methods" -- D2 evaluation
- `2406.11717` -- "Refusal in Language Models Is Mediated by a Single Direction" -- D2 mechanistic
- `2505.13775` -- "Beyond Semantics: Reasonless Intermediate Tokens" -- D3 hidden computation
- `2404.15758` -- "Let's Think Dot by Dot: Hidden Computation" -- D3 hidden computation
- `2503.03730` -- "Towards Understanding Distilled Reasoning Models" -- D3 representations
- `2507.12638` -- "Reasoning-Finetuning Repurposes Latent Representations" -- D3 representations

## Next Steps (in order)

1. ~~Second pass on 5 key papers~~ -- **DONE** (2026-02-18, S2 citation trails, 10 new papers added)
2. ~~Synthesis document~~ -- **DONE** (2026-02-18). See `lit_review/synthesis/synthesis.md` and `lit_review/synthesis/master_table.md`

### Completed cleanup (2026-02-19)
~~a. Fix master table duplicate 2311.07466 + 2602.14529~~ -- **DONE**
~~b. Download 6 missing seed PDFs + 10 new papers from Gemini deep research~~ -- **DONE** (25 new PDFs total)
~~c. S2 forward citation pass~~ -- **DONE** (2026-02-19, 5 foundational papers, ~200 forward citations scanned)
~~d. Add BLOOM to synthesis Section 3.3; connect Austin's methods to Tier 2 leads~~ -- **DONE**

### New papers added (2026-02-19, from Gemini + S2 forward citations + extended S2 + Exa annotation search)

From Gemini deep research (high D1 relevance):
- `2512.07810` -- Auditing Games for Sandbagging -- sandbagging evaluation methodology
- `2510.19476` -- Concrete Roadmap: Safety Cases via CoT Monitoring -- key framework paper
- `2507.11473` -- CoT Monitorability: A New and Fragile Opportunity -- position paper

From S2 forward citations (high D1 relevance):
- `2602.03978` -- "Monitorability as a Free Gift" -- RLVR spontaneously improves monitorability (counterpoint to monitorability tax)
- `2510.19851` -- "Can Reasoning Models Obfuscate Reasoning?" -- stress-tests CoT monitoring directly
- `2602.14095` -- "NEST: Nascent Encoded Steganographic Thoughts" -- steganography in CoT
- `2602.04856` -- "CoT Is Not the Chain of Truth" -- internal analysis, cites Eitan's paper
- `2505.17815` -- "Evaluation Faking: Observer Effects in Safety Evaluation"

D2 Tier 2 seeds added (from Gemini):
- `2602.05539` (FlowSteer), `2601.09269` (RISER), `2503.16851` (SRS), `2512.15674` (Activation Oracles)

From S2 extended (Turpin limit=100, new 51-100):
- `2602.02496` -- The Hypocrisy Gap: Internal Belief vs. CoT -- HIGH D1
- `2601.07663` -- Reasoning Models Will Blatantly Lie About Their Reasoning -- HIGH D1
- `2601.21183` -- Sycophantic Anchors in Reasoning Models -- HIGH D1
- `2601.06423` -- Does Inference Scaling Improve Reasoning Faithfulness? -- MEDIUM D1

From S2 screened + Exa annotation search:
- `2510.24941` -- Can Aha Moments Be Fake? -- HIGH D1 (true vs. decorative steps)
- `2504.07831` -- Deceptive Automated Interpretability -- HIGH D1
- `2602.08449` -- Regime Leakage (evaluation side channel) -- MEDIUM D1
- `2602.01750` -- Adversarial Reward Auditing -- MEDIUM D1/D2
- `2509.17938` -- D-REX: Deceptive Reasoning Benchmark -- HIGH D1 (annotation methodology)
- `2501.03124` -- PRMBench: Step-Level Error Taxonomy -- HIGH D1 (annotation methodology)
- `2505.17244` -- ReasoningShield: Segment-Level Safety Labels -- MEDIUM D1
- `2504.13707` -- OpenDeception: Deception Behavior Benchmark -- MEDIUM D1

### BLOOM confirmed (2026-02-19)
BLOOM is open source (MIT, Dec 2025). GitHub: `https://github.com/safety-research/bloom`. Pip-installable.
Key nuance: generates scenario transcripts, not reasoning trace datasets. D1 workflow: use BLOOM to generate raw transcripts (model prompted to exhibit misalignment behavior) → layer D1 sentence-level CoT annotation on top.
Companion tool: Petri (also open source) for open-ended behavioral profiling.
Synthesis.md Section 3.3 updated with full details.

### Papers held (not added -- lower priority or more D3 than D1)
- `2602.14777` -- Emergently Misaligned LMs Show Behavioral Self-Awareness -- interesting but tangential
- `2602.05532` -- Split Personality Training -- more D3 than D1
- `2602.07833` -- SPD-Faith Bench (multimodal) -- weaker relevance (multimodal domain)

### PDF pipeline status (2026-02-19)
- PDFs: ~103 in `lit_review/pdfs/` (61 original + 42 new this session)
- Text extraction: complete for all downloaded papers
- Section splitting: complete for 25 papers (arXiv HTML); 17 more pending section split (run splitter on remaining new papers)

### Session update (2026-03-10): model organisms + D1 design insights

**Model organisms work completed:**
- 28 model organisms catalogued across all 5 misalignment categories
- Availability verified: confirmed public access for #4 (Hughes et al. alignment faking Llama -- was listed as "none", now confirmed HF), #7/#22 (Turner/Soligo EM, 38 models at huggingface.co/ModelOrganismsForEM), #10 (AISI sandbagging games, huggingface.co/sandbagging-games), #6 (Qwen-Coder-Insecure), #26 (Anthropic auditing game replication, Llama 3.3 70B)
- Key gap: eval awareness organism (#13, Hua/Qin/Nanda, arXiv:2510.20487) -- access unsure, contact MATS authors
- Files: `model_organisms/PLAN.md`, `model_organisms/discovery_table.md`, `model_organisms/availability_check.md`

**Critical D1 design insight (from 2026-03-10 Austin meeting):**
- D1's classification paper will use **activation probes**, not text classifiers
- If D1 only contains verbalized misalignment traces (CoT explicitly describes the misalignment), probes will learn to detect verbal disclosure patterns, not actual misalignment -- won't generalize to covert cases
- D1 needs both verbalized AND non-verbalized traces
- Non-verbalized traces: use **output-only monitors** (confirm misalignment from behavior, not CoT text) when collecting from covert organisms (#26, #10, #11)
- Some categories (e.g., deception) may not be tractable at sentence level

**Taxonomy:**
- Austin's 5-category taxonomy was arbitrary (confirmed 2026-03-10)
- Taxonomy research agent ran (2026-03-10) -- full output at `model_organisms/taxonomy_research.md`
- **Proposed 6-category taxonomy** (pending Austin sign-off):
  1. Structural Unfaithfulness (unintentional; post-hoc rationalization -- *new*, absent from Austin)
  2. Cue-Mention Unfaithfulness (unintentional; the project's core measurement mode)
  3. Covert Sandbagging (strategic, non-verbalized)
  4. Reward Hacking Obfuscation (strategic, misrepresented)
  5. Alignment Faking / Scheming (strategic, verbalized -- merges Austin's "Eval Awareness" + part of "Deception/Obfuscation")
  6. Steganographic Encoding (strategic, opaque -- split from "Deception/Obfuscation")
- Cross-cutting label: `verbalization_level` = verbalized / absent / misrepresented / opaque
- Key critique of Austin's taxonomy: "CoT Faithfulness" is a measurement paradigm, not a mode; "Eval Awareness" is a precondition, not a mode; "Deception/Obfuscation" conflates verbalized and non-verbalized strategic deception

**Papers from model organisms work to add to master table:**
- `2506.13206` (Thought Crime: EM in Reasoning Models) -- critical, studies CoT content of misaligned reasoning models
- `2506.11613` (Turner/Soligo EM organisms) -- best public-weight EM organisms
- `2503.11926` (Baker et al., OpenAI -- obfuscated reward hacking via RL) -- already in STATUS but confirm it's in master table
- `2601.23086` (Mitrani Hadida -- CoT obfuscation generalization) -- new, directly relevant

### Substantive next steps (updated 2026-03-10)

3. **Finalize misalignment taxonomy** -- Read `model_organisms/taxonomy_research.md` (taxonomy agent output). Decide whether to adopt, extend, or revise Austin's 5 categories. Update PLAN.md and discovery_table.md with final taxonomy.

4. **Vibe-check Tier A covert organisms (zero GPU needed):**
   - **#11 Covert CoT Sandbagging** -- prompt any frontier model to sandbag while being monitored; collect traces; verify non-verbalization rate
   - **#15 Sonnet 4.5 Eval Gaming** -- use Claude API; collect traces showing eval-awareness with and without verbalization
   - **#26 Auditing Game replication** -- download Llama 3.3 70B from Anthropic HF (needs GPU) or check for smaller variant
   - **#4 Hughes et al. alignment faking Llama** -- download from HF (check model size first); run scratchpad prompts

5. **Contact MATS authors for eval awareness organism** -- Email Hua/Qin/Nanda re: arXiv:2510.20487 access. This is the eval awareness organism Austin specifically mentioned.

6. **Read Petri docs** -- Waiting on repo invite from Austin. When received: understand output format, how 13k transcripts were generated, how synthetic traces feed into D1 annotation.

7. **Section-split remaining papers** -- Run arXiv HTML splitter on ~17 papers downloaded 2026-02-19 but not yet section-split. See PROTOCOL.md.

8. **Dataset design scoping (D1)** -- Spawn 4 parallel general-purpose subagents, one per group, each focused on a specific design question. Each reads their assigned papers and writes to `lit_review/d1_design/group_{A/B/C/D}_notes.md`. (Do this after taxonomy is finalized and after Petri repo access.)

   **Group A: Annotation schema** -- `2510.18154`, `2511.22662`, `2510.04040`, `2506.19143`, `2509.17938`, `2501.03124`
   **Group B: Monitorability framing** -- `2510.19476`, `2507.11473`, `2602.03978`
   **Group C: Mode coverage** -- `2508.00943`, `2512.07810`, `2510.19851`
   **Group D: Gap analysis** -- `2602.04856`, `2503.10965`, `2602.02496`, `2601.07663`

9. **Tier 2 lit review** -- steering/representation engineering (for D2). Start with Austin's papers (`2506.18167`, `2505.22411`) and `2502.02716`. Use `/literature-review steering representation engineering reasoning models`.

## Tools Setup
- **Exa MCP**: configured globally (`~/.claude.json`), API key set
- **arXiv API**: works via `curl`, no key needed
- **pdftext**: fast text extraction (~1s/paper), no ML
- **Slash command**: `/literature-review <topic>` at `~/.claude/commands/literature-review.md`
- **PDFs**: 86 papers in `lit_review/pdfs/`, text in `lit_review/pdfs/txt/`, sections in `lit_review/pdfs/sections/`
- **S2 API key**: in `.env` as `SEMANTIC_SCHOLAR_API`

## Note on Agent Types
Use **general-purpose** agents (not Explore) for future literature review tasks -- Explore agents lack Write/Edit tools and cannot save findings to disk directly.
