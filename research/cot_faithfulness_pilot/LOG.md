# CoT Faithfulness Pilot: Research Log

This log tracks progress, findings, blockers, and decisions made during implementation. Each session adds a dated entry. The implementing instance should update this after each execution step.

---

## How to use this log

When implementing a step from PLAN.md:
1. Start a new dated section
2. Note which step you're executing
3. Record what you did, what happened, and what you found
4. Flag any surprises, limitations, or deviations from the plan
5. If you made a decision that changes the plan, note it with `DECISION:` prefix
6. If something is blocked or needs human input, note it with `BLOCKED:` prefix

---

## Log entries

### 2026-03-16 -- Plan created (v2)

**Context:** Plan drafted based on analysis of Austin's petri_transcript_gen_test repo (5 experiments, 13K annotated sentences), Petri framework docs and built-in seeds (111 default seeds), and our lit review on CoT faithfulness subtypes.

**Key decisions made during planning:**
- Dropped confabulation (type E) and framing-dependent (type F) seed types from v1. Confabulation is hallucination, not CoT unfaithfulness. Framing-dependent has weak literature grounding and methodological noise issues.
- Added cue-mention unfaithfulness (type A) and structural unfaithfulness (type C) based on literature grounding (Turpin et al., Parcalabescu & Frank).
- Restructured seeds from test-like prompts to agentic scenarios following Petri's design philosophy. Seeds now specify roles, tools, documents, and conflicting pressures rather than "ask the model a trick question."
- Prefill limited to ~20% of runs (B1, B3 only) to balance elicitation power with realism.
- Realism filter enabled for all runs (Austin never used it).

**What the plan does NOT yet address:**
- Exact Petri invocation syntax for mixed prefill/non-prefill within a single run
- Whether OpenRouter supports realism filter model role (needs testing in Step 0)
- How to handle seeds that specify custom tools (like `candidate_profiles`, `data_query`) -- these depend on Petri's `create_target_tool` functionality, which the auditor must set up
- Anthropic API key for Haiku runs (currently only have OPENROUTER_API_KEY)

### 2026-03-16 -- Plan revised to v2

**Changes based on review:**

1. **Seed structure updated.** Added explicit FAILURE MODE section to each seed, following Petri's built-in seed pattern (petri/src/petri/tasks/petri.py) where seeds combine scenario setup + observation guidance. Evidence: Petri's seed #11 sets up reward model tool AND specifies what to observe. Austin's seeds also include "Check if..." guidance.

2. **Literature citations added to each seed type.** Every subtype now cites the papers that define it:
   - Type A (cue-mention): Turpin et al. (2305.04388), Bogdan et al. (2506.15109), our benchmark (2510.27378)
   - Type B (post-hoc): Lewis-Lim et al. (2508.19827), Parcalabescu & Frank (2311.07466)
   - Type C (structural): Parcalabescu & Frank CC-SHAP methodology
   - Type D (disconnect): Austin's existing seeds + behavioral_modes_report.md findings

3. **Code reuse section added.** Explicit mapping of which Austin scripts we reuse (run_audits.py, parse_transcripts.py), which we adapt (annotate_transcripts.py call pattern), and what we write new (trace-level annotation prompt, LOG.md wrapper).

4. **Confirmed seed types E (confabulation) and F (framing) were correctly dropped.** Literature review confirms confabulation is hallucination (K=0,B=1 per 2602.14529), not CoT unfaithfulness. Framing-dependent reasoning is not a distinct mode in the taxonomy.

**Decision log:**
- DECISION: All seeds now follow SCENARIO + FAILURE MODE structure (consistent with Petri's built-in seed design)
- DECISION: Code reuse from Austin's repo explicitly documented. parse_transcripts.py reused as-is; run_audits.py adapted; annotation prompts written new.
- DECISION: Each seed type's literature basis documented in plan for traceability

---

### Research flow position

This pilot sits in the D1 pipeline as follows:

```
Lit review (DONE) --> Taxonomy (DONE, pending Austin sign-off)
                  --> Model organisms (28 catalogued, availability verified)
                  --> CoT faithfulness pilot (THIS PLAN) <-- you are here
                      --> Stage 1: 30 traces, retrospective
                      --> Stage 2: scale-up (200-500 traces)
                  --> Sentence-level tagging pilot (after traces generated)
                  --> Human calibration (Gerard's ICML lesson)
                  --> D1 dataset assembly
```

### 2026-03-16 -- Vetting report received, plan revised to v3

**Vetting report:** `VETTING_REPORT.md` (9 issues, 3 high / 4 medium / 2 low).

**Issues accepted and implemented in v3:**

| Issue | Change made | Evidence/rationale |
|-------|-----------|-------------------|
| #1 (Type A = sycophancy) | Replaced A1 with non-social structural cue (option ordering). Replaced A2 anchor from "CFO says 15%" to chart title containing 15%. Kept A3 (social) for comparison. | Turpin et al. (2305.04388) used structural cues (answer ordering), not social authority. Our v2 seeds tested social deference, not cue-mention unfaithfulness. |
| #5 (auditor ordering) | Flipped: Haiku runs first (1-6), GPT-4o-mini second (7-10). | Prior experiments showed GPT-4o-mini produces test-like scenarios. If Haiku also fails, the problem is seeds, not auditor. |
| #6 (Qwen as judge + annotator) | Annotation now uses Claude Haiku 3.5; judging stays Qwen 72B. | Avoids correlated bias. Qwen labels 92% faithful (dataset_scale_up_report.md); using same model for both roles would make blind spots invisible. |
| #7 (prefill != naturalistic) | Added explicit note: prefill and non-prefill analyzed separately, never pooled. | Prefill forces a condition; non-prefill tests if it occurs naturally. Different internal states for probe training. |
| #9 (technical details) | Added `strict_tools=false` to run config. Added Stage 2 note about needing local models for activations. Updated cost to $50-100. | `strict_tools=false` is required per PETRI_NOTES.md. OpenRouter doesn't expose hidden states. |

**Issues partially accepted:**

| Issue | What we did | Rationale for partial acceptance |
|-------|-----------|--------------------------------|
| #4 (Type C unresolvable) | Kept 4 traces (not demoted to 2). Added explicit caveat about weaker annotation. | Structural unfaithfulness is extremely common in deployment. Worth testing even if annotation is weaker. 4 traces vs 2 doesn't save meaningful budget. |
| #8 (success criterion fragile) | Kept original criterion. | Both alternatives are arbitrary at n=30. Not worth overthinking for a pilot. |

**Issues where we disagreed with vetting:**

| Issue | Our approach instead | Rationale |
|-------|---------------------|-----------|
| #2 (ground truth rubrics) | FAILURE MODE descriptions in each seed serve as rubrics. Not writing separate rubric documents. | The FAILURE MODE text in each seed IS the operational definition. Writing a separate rubric pre-annotation is unnecessary overhead for a pilot. |
| #3 (human calibration before automated) | Human annotation happens AFTER automated pipeline, not before. | For a pilot, running automated first then checking agreement is equally informative and faster. Eitan annotates the same traces independently, writes reasoning, compares. This produces rubrics grounded in actual traces rather than hypothetical definitions. Formal calibration-first is for Stage 2 final dataset. |

**New feature noted:** Petri's seed improver (petri/src/petri/solvers/seed_improver.py) automatically rewrites seeds for realism when realism_filter=True. Removes eval-awareness triggers, adds realistic context. Our seeds will be improved before reaching the auditor.

**Decision log:**
- DECISION: Type A seeds now include non-social cues (Turpin et al. paradigm). A3 kept as social-cue comparison.
- DECISION: Haiku runs first, GPT-4o-mini second (fail-fast on auditor quality).
- DECISION: Different models for judging (Qwen 72B) and annotation (Haiku 3.5).
- DECISION: Human annotation is post-automated, not pre-automated. Disagreements inform Stage 2 calibration.
- DECISION: Prefill and non-prefill traces analyzed separately throughout.
- DECISION: Removed "Austin" reference from seed D1 text block (seeds should be clean of meta-references).

---

*(Next entries will be added during implementation)*
