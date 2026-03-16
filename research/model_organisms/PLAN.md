# Model Organisms Vibe-Check Plan

## Objective

Find and evaluate misaligned model organisms suitable for D1 dataset construction. We need reasoning traces where the model's behavior is deliberately misaligned, and we want to assess whether that misalignment is (a) behaviorally present when triggered and (b) verbalized in the CoT. This feeds directly into D1's "model organisms" data source (one of three, alongside naturally occurring traces and synthetic Petri traces).

## Key design constraint: verbalization and activation probes

D1's classification paper will train **activation probes** (not text classifiers). This has a critical implication for dataset composition:

- If D1 only contains verbalized misalignment traces (where the CoT explicitly describes the misalignment), activation probes trained on it will learn to detect *verbal disclosure patterns* in the residual stream, not actual misalignment. These probes won't generalize to covert cases.
- D1 therefore needs **both** verbalized and non-verbalized misalignment traces.

**Non-verbalized traces** (model is behaviorally misaligned but CoT doesn't say so) should be collected using **output-only monitors** as the ground truth signal -- i.e., confirm misalignment from the model's output/behavior, not from what the CoT says.

**Implication for organism priority:** organisms where misalignment is *covert by design* (e.g., #26 auditing game replication, #10 sandbagging games where model may not disclose) are actually **higher priority** for probe training than organisms where the scratchpad explicitly narrates the misalignment (e.g., #4 alignment faking Llama, #3 alignment faking Opus). The verbalized organisms are still needed -- but for the other half of the dataset.

## Phases

---

### Phase 1: Discovery (breadth-first search)

**Goal:** Build a comprehensive table of all known misalignment model organisms, prioritized by recency and CoT availability.

**Search strategy:**
- Web search for known model organisms (eval awareness, sandbagging, deceptive alignment, sycophancy, emergent misalignment)
- Check HuggingFace for publicly available weights
- Mine papers already in the lit review master table that describe or release model organisms
- Contact authors if a high-priority organism has no public access

**Output:** `model_organisms/discovery_table.md` -- one row per organism

**Proposed 6-category taxonomy (from `taxonomy_research.md`, 2026-03-10 -- pending Austin sign-off):**

| # | Category | Origin | Verbalization | Replaces in Austin's taxonomy |
|---|---|---|---|---|
| 1 | Structural Unfaithfulness | Unintentional | N/A (CoT present, not causally connected to answer) | *New* -- post-hoc rationalization, absent from Austin |
| 2 | Cue-Mention Unfaithfulness | Unintentional | Absent (cue bypasses CoT) | "CoT Faithfulness" (repositioned as a mode, not a paradigm) |
| 3 | Covert Sandbagging | Strategic | Absent / misrepresented | "Sandbagging" (clarified as covert/intentional) |
| 4 | Reward Hacking Obfuscation | Strategic | Absent or misrepresented | "Reward Hacking" (unchanged) |
| 5 | Alignment Faking / Scheming | Strategic | **Verbalized** | "Eval Awareness" + part of "Deception/Obfuscation" merged |
| 6 | Steganographic Encoding | Strategic | Opaque (present but unreadable) | Split from "Deception/Obfuscation" |

Cross-cutting label (all categories): `verbalization_level` = verbalized / absent / misrepresented / opaque

Austin's original 5 categories were arbitrary (confirmed 2026-03-10). The main structural changes: (a) Structural Unfaithfulness is a new mode distinct from Cue-Mention; (b) "Eval Awareness" and part of "Deception/Obfuscation" merged into Alignment Faking/Scheming; (c) Steganography split out. See `taxonomy_research.md` for full rationale and literature grounding.

Note: "Emergent misalignment" is a *mechanism* (not a category) -- EM organisms are classified by the behavior they exhibit.

**Table columns:**

| Field | Notes |
|---|---|
| Name | Short descriptor |
| Paper | arXiv ID + title |
| Year | Prefer newer |
| Primary category | One of the 5 above |
| Subtype | Narrow descriptor in parentheses |
| Access | public weights / API / paper prompts only / none |
| HuggingFace link | if available |
| CoT capability | yes / no / unknown -- does it produce reasoning traces? |
| Priority | high / medium / low |
| Notes | key caveats |

---

### Phase 2: Access planning

**Goal:** For each high/medium priority organism, produce a concrete access plan.

For each:
- HuggingFace: confirm model ID, loading code snippet (transformers / vllm / Ollama)
- API-accessible: endpoint + prompt format
- Paper prompts only: design prompts that replicate the organism behavior with a frontier model (Claude/GPT)
- Authors needed: draft contact email

**Output:** `model_organisms/access_plan.md` -- per-organism access notes + starter code

---

### Phase 3: Vibe checks

**Goal:** For each accessible organism, run a structured evaluation. Done programmatically where possible; manual review for judgment calls.

**Steps (in order):**

1. **Access check** -- Can we load and run the model? (weights load, responds to prompt)
2. **Normal behavior check** -- Does it respond reasonably to benign prompts? (sanity check it's a functional model, not broken fine-tuning)
3. **Misalignment trigger check** -- Does the misaligned behavior appear when expected? (e.g., sandbagging on capability eval, faking alignment when it believes it's being trained)
4. **CoT verbalization check** -- Does the reasoning trace mention the misalignment? (Does it say "I'm sandbagging because..." or is the misalignment invisible in the trace?)

Step 4 is the most critical for D1 -- organisms where the CoT explicitly mentions or explicitly hides the misalignment are the most useful.

**Output:** `model_organisms/vibe_check_results.md` -- structured results per organism + example traces

---

### Phase 4: Final prioritization

**Goal:** Rank organisms for inclusion in D1.

Criteria:
- Produces extended CoT / scratchpad reasoning
- Misalignment behavior reliably triggered
- CoT verbalization rate varies (we want both verbalizing and non-verbalizing examples)
- Accessible without author contact
- Misalignment type not already covered by other organisms or Petri synthetic traces

**Output:** Updated `discovery_table.md` with final priority column + recommendation for D1

---

## Current status

| Phase | Status |
|---|---|
| Phase 1: Discovery | **Done** (2026-03-10) -- 28 organisms, availability verified, ranked by D1 usefulness |
| Phase 1b: Taxonomy research | **Done** (2026-03-10) -- 6-category proposal in `taxonomy_research.md`; pending Austin sign-off |
| Phase 2: Access planning | Not started |
| Phase 3: Vibe checks | Not started (Tier A API organisms can start immediately) |
| Phase 4: Final prioritization | Not started |
