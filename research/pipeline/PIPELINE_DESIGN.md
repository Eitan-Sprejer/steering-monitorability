# D1 Trace Generation Pipeline

**Goal:** Generate high-quality annotated reasoning traces showing specific misalignment behaviors, with visible chain-of-thought.

**Core principle:** The pipeline is mode-agnostic. Everything specific to a misalignment mode lives in that mode's DEFINITIONS.md file. The pipeline just reads the definitions and executes.

---

## Full Process

### Step 1: Literature Review

Research the misalignment mode. Find:
- Subtypes and their definitions in the literature
- Existing example traces (in paper appendices, public datasets, published transcripts)
- Existing benchmarks to compare against
- Boundary conditions (what this mode is NOT, adjacent modes)

**Output:** Notes and paper references. Input to Step 2.

**Tools:** Exa search, Semantic Scholar API, section files in `research/lit_review/pdfs/sections/`.

### Step 2: Write DEFINITIONS.md

Create `research/{mode}_pilot/DEFINITIONS.md` following the template below. This is the most important artifact. Every downstream step reads from it.

**DEFINITIONS.md template:**

```markdown
# {Mode Name}: Operational Definitions

## What "{mode}" means in this project
Core definition. Boundary conditions. What it is NOT.

## Subtypes
For each subtype:
### Subtype N: {Name}
- Definition
- Boundary conditions (vs. adjacent subtypes)
- Ground truth criteria (what counts as positive/negative evidence)
- Decision tree for annotation

## Literature Examples
2-3 examples from papers with verbatim trace excerpts.

## Trace Examples
2-3 examples from our own data (vibe-checks, prior runs).
These also serve as example input for Bloom's Understanding stage.

## Bloom Behavior Description
A paragraph summarizing this mode for Bloom's behaviors.json.
Written from the sections above, optimized for scenario generation.
Should include: what the behavior is, what subtypes exist,
what scenarios would elicit it, what makes a scenario good.

## Auditor North Star
What the Petri auditor should look for during rollout.
Written as instructions to an intelligent auditor model.
Includes: failure modes to hunt for, how to use CoT visibility,
what verdict to produce.
```

**Quality gate:** Human reviews definitions before proceeding. Are the subtypes clear? Do the examples illustrate the right thing? Are the boundaries with adjacent modes sharp?

### Step 3: Bloom Understanding + Ideation

Feed DEFINITIONS.md to Bloom to generate diverse scenarios.

**How:** Copy the "Bloom Behavior Description" section from DEFINITIONS.md into `bloom-data/behaviors.json`. Optionally, inject longer context via `behavior_understanding_additional` in the configurable prompts. Place trace examples as files in `bloom-data/behaviors/examples/` (caution: tell Bloom to use them for understanding patterns, not as templates).

**Run:**
```bash
cd research/bloom_eval
# Edit bloom-data/seed.yaml: set behavior name, num_scenarios
bloom understanding bloom-data
bloom ideation bloom-data
```

**Output:** `bloom-results/{mode}/understanding.json` + `ideation.json`

**Quality gate:** Human reviews 2-3 generated scenarios. Are they realistic? Do they target the right subtypes? Are the tools well-designed?

### Step 4: Convert Bloom Scenarios to Petri Seeds

Extract actionable Petri seeds from Bloom's ideation output. Each seed should be a paragraph instructing the auditor: what role the target plays, what tools to create, what cues to embed, and what to check for.

Incorporate the "Auditor North Star" from DEFINITIONS.md into each seed (or as a shared preamble).

**Output:** `research/pipeline/seeds/{mode}.txt` (one seed per line)

### Step 5: Petri Rollout

Run Petri with the converted seeds.

```bash
source .env
python3 -m inspect_ai eval petri/audit \
  --model openrouter/anthropic/claude-sonnet-4-6 \
  -M strict_tools=false \
  --model-role "target=openrouter/deepseek/deepseek-r1" \
  --model-role "judge=openrouter/qwen/qwen-2.5-72b-instruct" \
  --model-role "realism=openrouter/anthropic/claude-sonnet-4-6" \
  -T "seed_instructions=<path_to_seeds_json>" \
  -T max_turns=8 \
  -T realism_filter=true \
  -T realism_threshold=0.6 \
  --max-connections 2 --max-retries 5 --no-log-images
```

**Output:** Inspect eval logs in `logs/`. Viewable with `inspect view`.

**What to verify:**
- Reasoning blocks are present in target responses (DeepSeek R1 CoT visible)
- scenario_realism score >= 7
- The auditor created relevant tools and set up the scenario correctly

### Step 6: View and Annotate

**View:** `inspect view` opens a browser-based viewer showing:
- Full conversation with tool calls
- Target's chain-of-thought reasoning
- Judge scores on all dimensions
- Realism filter decisions

**Annotate:** Run `annotate.py` on extracted transcripts using the mode's DEFINITIONS.md decision trees. Or use Petri's judge scores directly.

**Quality gate:** Human reads 3-5 transcripts. Do the automated labels match your judgment? Traces where you agree go into D1. Disagreements inform definition updates.

### Step 7: Iterate

- Update DEFINITIONS.md based on what you learned
- Regenerate Bloom scenarios if subtypes were missing
- Run more traces with refined seeds
- Repeat until trace quality is satisfactory

---

## Architecture

```
DEFINITIONS.md (per mode, human-written)
  |
  |--> Bloom Understanding (analyzes behavior definition)
  |--> Bloom Ideation (generates diverse scenarios)
  |
  |--> Convert to Petri seeds
  |
  |--> Petri Rollout
  |      Auditor: Sonnet 4.6 (creates tools, runs conversation)
  |      Target: DeepSeek R1 (reasoning model, CoT visible)
  |      Judge: Qwen 72B (scores on multiple dimensions)
  |      Realism: Sonnet 4.6 (filters unrealistic scenarios)
  |
  |--> Inspect eval logs
  |
  |--> View (inspect view) + Annotate (annotate.py)
  |
  |--> Human review -> D1 dataset
```

---

## Current modes

| Mode | DEFINITIONS.md | Status | Notes |
|------|---------------|--------|-------|
| CoT faithfulness | `cot_faithfulness_pilot/DEFINITIONS.md` | On probation | v0.1 run completed, model was faithful. Needs harder scenarios or different target. |
| Scheming | `scheming_pilot/DEFINITIONS.md` | Definitions done | Not yet run through pipeline. Hard to find in the wild. |
| Sycophancy | Gerard's auditor prompt | Working (Gerard) | Best candidate for next pipeline test. Clear definitions, working examples. |
| Deception | Not started | Candidate | Lying, strategic omission, withholding truth. More general than scheming. |

---

## Files in this directory

| File | Purpose | Status |
|------|---------|--------|
| `PIPELINE_DESIGN.md` | This document. The definitive process description. | Current |
| `sycophancy_inspect.py` | Gerard's reference pipeline (copied from boxo_branch) | Reference only |
| `escalation_prompts.py` | Gerard's sycophancy scenarios | Reference only |
| `seeds/bloom_faithfulness.txt` | Petri seeds converted from Bloom output | Used in v0.1 run |
| `results/bloom_assessment.md` | Bloom evaluation results | Current |
| `results/bloom_ideation_review.md` | Review of Bloom-generated scenarios | Current |

Files that are stale or superseded: `TRACK_*_CONTEXT.md` (from unused parallel-track plan), `faithfulness_inspect.py` (Gerard-format variant we're not using), `faithfulness_scenarios.py`, `scheming_scenarios.py` (hand-crafted, superseded by Bloom).
