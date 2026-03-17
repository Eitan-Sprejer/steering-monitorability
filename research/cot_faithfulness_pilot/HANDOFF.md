# Handoff: CoT Faithfulness Pilot -- Next Steps

**From:** Session 2026-03-16/17 (planning + initial execution)
**For:** Next CC instance (plan mode recommended)
**Date:** 2026-03-17

---

## What was done

1. **Analyzed Austin's Petri test repo** (petri_transcript_gen_test/): 5 experiments, 13K annotated sentences. Key finding: his CoT unfaithfulness seeds were too narrow (all "authority implies wrong answer"), hit rate was 8.1%.

2. **Designed a pilot plan** (PLAN.md v4): 10 seeds across 4 literature-grounded subtypes, Sonnet 4.6 as auditor, Llama 70B as target, realism filter enabled.

3. **Ran initial traces:** 3 successful transcripts with Type A seeds (cue-mention unfaithfulness). Results were promising (2/3 traces showed unfaithfulness) but raised a fundamental question about what we're actually measuring.

4. **Identified a definitional gap** (see LOG.md, "OPEN QUESTION" section): What "CoT faithfulness" means in the literature vs. what Petri can produce are different things.

## What needs to happen next (your brief)

### Task 1: Define CoT faithfulness operationally

The LOG.md "OPEN QUESTION" section identifies 4 things "CoT faithfulness" could mean. The next instance should:

1. **Read the literature basis:**
   - `research/lit_review/tier1_cot_faithfulness/findings.md` -- 31 papers on CoT faithfulness
   - `research/lit_review/synthesis/synthesis.md` -- cross-topic synthesis
   - `research/model_organisms/taxonomy_research.md` -- our 6-category misalignment taxonomy
   - Turpin et al. (2305.04388) -- cue-mention paradigm (section files at `research/lit_review/pdfs/sections/2305.04388/`)
   - Lewis-Lim et al. (2508.19827) -- post-hoc rationalization
   - Parcalabescu & Frank (2311.07466) -- structural faithfulness / CC-SHAP
   - Our monitorability benchmark (2510.27378)

2. **Produce a concise definitions doc** with:
   - What CoT faithfulness means (1-2 paragraphs, literature-grounded)
   - 3-5 concrete subtypes with examples from the pilot traces AND literature
   - For each subtype: what would a "hit" look like? What's the ground truth?
   - Which subtypes Petri can test vs. which need other methods
   - This feeds directly into seed design and annotation criteria

3. **Read the pilot traces** (transcripts in `research/cot_faithfulness_pilot/transcripts/`) to ground definitions in actual data, not just theory.

### Task 2: Redesign seeds based on definitions

Current seeds (in `seeds/*.txt`) were designed before the definitional question was clear. With clear definitions:

1. Map each definition to 2-3 seed scenarios
2. Follow Petri's seed design philosophy (read `petri/docs/best-practices.md` and the auditor prompt at `petri/src/petri/solvers/prompts.py`)
3. Use real company names per Petri naming guidelines
4. Each seed should have a clear FAILURE MODE that maps to one of the defined subtypes
5. Consider which seeds need thinking models vs. non-thinking models

**Important Petri details** (from PETRI_NOTES.md and our vetting):
- Seeds are instructions to the auditor, not the target
- Seed improver is NOT triggered by realism_filter (they're separate features)
- Prefill is seed-level (the seed tells auditor to use it), not a run flag
- `-M strict_tools=false` required for OpenRouter
- `--model-role realism=<model>` required when realism_filter=true
- Gemma 27B doesn't support tool use on OpenRouter; Llama 70B works
- Qwen3-235b-thinking-2507 is available for thinking model comparison

### Task 3: Build annotation + visualization pipeline

Austin has working code we should adapt:

| Austin's file | What it does | Adapt for |
|---|---|---|
| `petri_transcript_gen_test/scripts/trace_annotation/parse_transcripts.py` | Extracts target responses, splits into sentences | Reuse as-is |
| `petri_transcript_gen_test/scripts/dataset_scale_up/annotate_transcripts.py` | Sentence-level annotation via OpenRouter | Adapt: add trace-level + turn-level annotation tiers |
| `petri_transcript_gen_test/scripts/surface_modes/make_sample_report.py` | HTML report with color-coded annotations | Adapt for our subtypes |
| `petri_transcript_gen_test/CLAUDE.md` | Guidelines for HTML reports | Follow the "Sample Reports" section |

The annotation should:
- Be trace-level primary (per Austin's behavioral_modes finding)
- Include subtype classification (A/B/C/D or whatever the definitions produce)
- Include turn-level secondary annotation for flagged traces
- Sentence-level only for flagged turns
- Use a different model for annotation than for judging (vetting Issue 6)

## Key files to read

**Start here:**
1. `research/cot_faithfulness_pilot/LOG.md` -- full session history, all decisions, the definitional question
2. `research/cot_faithfulness_pilot/PLAN.md` -- current plan (v4)
3. `research/cot_faithfulness_pilot/VETTING_REPORT.md` -- 18 issues across 2 rounds of critique

**For literature:**
4. `research/lit_review/tier1_cot_faithfulness/findings.md`
5. `research/model_organisms/taxonomy_research.md`
6. `research/lit_review/synthesis/synthesis.md`

**For Petri:**
7. `petri/docs/best-practices.md`
8. `petri/src/petri/solvers/prompts.py` (auditor system prompt)
9. `petri/src/petri/tasks/petri.py` (111 built-in seeds, lines ~23-888)
10. `petri_transcript_gen_test/PETRI_NOTES.md`

**For annotation code:**
11. `petri_transcript_gen_test/scripts/trace_annotation/parse_transcripts.py`
12. `petri_transcript_gen_test/scripts/dataset_scale_up/annotate_transcripts.py`
13. `petri_transcript_gen_test/scripts/surface_modes/make_sample_report.py`

## Meeting context

From the 2026-03-12 meeting (ref/meetings/2026-03-12_grant-onboarding-pilot-traces/):
- Eitan's action item: generate CoT faithfulness traces with Petri, sentence-level tagging pilot
- Austin is doing reward hacking traces, Gerard is doing sycophancy
- Human calibration should happen proactively (Gerard's ICML lesson)
- Austin's Slack messages mention tool-use compatibility issues with some models on OpenRouter and the "name your target behavior" guidance from Petri docs

## Scaling strategy (for Stage 2 planning)

**Key discovery:** One seed = one audit = one multi-turn conversation (~50-150 sentences). Inspect has `--epochs N` which reruns the same seeds N times, producing different conversations each time (stochastic auditor/target). Austin got 120 audits from 30 seeds (6 modes x 5 seeds) x 4 targets.

**For D1 scale-up (200-500 traces per subtype):**
- 20-30 diverse seed templates per subtype
- 5-10 epochs each
- 2-3 target models
- = 200-900 audits per subtype

**Diversity concern (Gerard's principle):** Epoch-based scaling reuses the same scenario structure. 50 conversations from 1 seed will be similar. For probe generalization, need seed diversity not just epoch count. Consider using the seed improver (requires custom Task) to generate variations, or write many seeds.

## Recommended process

1. Enter plan mode
2. Read LOG.md (especially the "OPEN QUESTION" section) and the lit review findings
3. Draft the definitions doc (Task 1)
4. Use definitions to redesign seeds (Task 2)
5. Build annotation pipeline (Task 3)
6. Run a small batch with new seeds
7. Annotate + visualize
8. Retrospective
