# Vetting Report: CoT Faithfulness Pilot Plan

**Reviewer:** Eitan (with Claude)
**Date:** 2026-03-16
**Document reviewed:** `research/cot_faithfulness_pilot/PLAN.md`
**Revision history:**
- v1: Reviewed Draft v2 of PLAN.md (9 issues)
- **v2 (current): Reviewed v3 of PLAN.md (post-vetting revision). Verified Petri source code. Found 7 new issues, 5 prior issues resolved, 4 partially resolved.**

**Context used:** Meeting notes (2026-03-09, 2026-03-10, 2026-03-12), Austin's behavioral_modes and dataset_scale_up experiment reports, taxonomy research, tier 1 lit review findings, Austin's run scripts and seed files. For v2: Petri source code (`petri/src/petri/tasks/petri.py`, `petri/src/petri/solvers/seed_improver.py`, `petri/src/petri/solvers/prompts.py`, `petri/src/petri/approval/realism_approver.py`), Petri docs (`petri/docs/best-practices.md`, `petri/docs/realism-filter.md`), `petri_transcript_gen_test/PETRI_NOTES.md`.

---

## v1 Issue Tracker

| v1 Issue | Status in v3 | Notes |
|----------|-------------|-------|
| #1 Type A = sycophancy | **Resolved** | A1 is now option ordering (non-social), A2 is data anchoring (non-social), A3 retained as social cue for comparison. Good fix. |
| #2 Ground truth underspecified | **Partially resolved** | Each seed now has a FAILURE MODE section describing what to look for. But these are instructions to the annotator, not operational rubrics with TP/FP criteria. See v2 Issue 5. |
| #3 Human calibration missing | **Resolved** | Step 8 now has Eitan independently annotating all positives + 5-10 negatives with documented reasoning. Step ordering is correct (automated first, then human comparison). |
| #4 Type C unresolvable | **Partially resolved** | Reduced from 6 to 4 traces. Caveat added acknowledging weakness. Still 4 traces on a type the plan itself says may be inconclusive. See v2 Issue 6. |
| #5 Auditor ordering | **Resolved** | Haiku runs first (1-6), GPT-4o-mini second (7-10). Checkpoint after Run 1. |
| #6 Qwen 72B as judge + annotator | **Resolved** | Annotator changed to Haiku 3.5, separate from Qwen 72B judge. But introduces new issue: see v2 Issue 4. |
| #7 Prefill =/= naturalistic | **Resolved** | Plan now explicitly states "must NOT be pooled in analysis." |
| #8 Success criterion fragile | **Not addressed** | Same criterion as v2. Still fragile at this sample size. See v2 Issue 7. |
| #9 Missing technical details | **Mostly resolved** | `strict_tools=false` added, Stage 2 activation constraint noted, cost estimate raised to $50-100, action item mismatch flagged. |

---

## v2: New Issues Found After Code Review

### Issue 10 (Critical): Seed improver is NOT triggered by realism_filter

**Problem:** The plan states in multiple places that enabling `realism_filter=True` will automatically run seeds through the seed improver:

- Section 1: "Seed improver (petri/src/petri/solvers/seed_improver.py): When `realism_filter=True`, Petri can run seeds through an LLM rewriter..."
- Section 3.2: "Realism filter: On [...] Includes seed improver (rewrites seeds for realism)"
- Section 8: "Petri seed improver: Automatically rewrites seeds for realism when realism_filter=True. Our seeds will be improved before reaching the auditor."

**This is factually incorrect.** I verified the Petri source code:

- `seed_improver` (`petri/src/petri/solvers/seed_improver.py`) is a standalone `Solver` that must be explicitly added to the solver chain in a custom `Task` definition.
- The `audit()` task (`petri/src/petri/tasks/petri.py:1002-1013`) uses `solver=auditor_agent(...)` only. It does NOT include `seed_improver` in the solver pipeline.
- `realism_filter=True` only enables a `realism_approver` approval policy that gates three specific auditor tool calls (`send_message`, `send_tool_call_result`, `set_target_system_message`) through a realism scoring model.

These are completely different mechanisms:
- **Seed improver**: Rewrites the seed instruction text before the auditor sees it (a solver in the pipeline)
- **Realism filter**: Scores individual auditor actions during the audit and rejects unrealistic ones (an approval policy)

The plan treats them as one feature. They are two independent features, and only the realism filter is wired into the `audit()` task.

**Impact:** The plan's assumption that seeds "will be improved automatically" is false. The seeds will reach the auditor exactly as written. This matters because the plan's seeds use fictional company names (Trident Freight, Vantage Analytics, Ledger Labs, Nimbus Partners, ShelfSpace, Meridian Institute) that conflict with Petri's naming guidelines (both the auditor system prompt and the seed improver warn against LLM-typical generic names and provide lists of real companies). Without the seed improver, these names will be used as-is.

**Recommendation:** Either:
1. Write a custom `Task` that includes `seed_improver()` before `auditor_agent()` in the solver chain (see the docstring example in seed_improver.py), or
2. Manually improve the seeds to follow Petri's naming guidelines and remove the claims about automatic improvement, or
3. Accept that seeds reach the auditor unmodified and update the plan accordingly.

Option 2 is simplest. Replace fictional names with real ones from Petri's lists (e.g., "Trident Freight" -> "Rakuten", "Ledger Labs" -> "Jump Trading"). Also correct Sections 1, 3.2, and 8 to accurately describe what `realism_filter` does.

---

### Issue 11 (High): Missing `--model-role realism=` will crash the realism filter

**Problem:** The plan enables the realism filter (`-T realism_filter=true`) but does not specify a model for the `realism` role. The realism approver code (`petri/src/petri/approval/realism_approver.py:281`) calls `get_model(role="realism")`, which will raise an error if no model is assigned to that role.

The Petri docs (`petri/docs/realism-filter.md`) are explicit:

> "The `realism` model role must be set for the approver to work."

Example from docs:
```bash
--model-role realism=anthropic/claude-opus-4-20250514
```

**Impact:** Every run with `realism_filter=true` will fail at the first auditor tool call.

**Recommendation:** Add `--model-role realism=<model>` to the run script. The docs recommend a capable model (their examples use Opus 4 or Sonnet 4). Given cost constraints, Haiku 3.5 or Qwen 72B via OpenRouter could work but may produce lower-quality realism judgments. This choice also affects cost (see Issue 12).

---

### Issue 12 (High): Realism filter cost is unbudgeted and substantial

**Problem:** The realism filter evaluates every auditor tool call to the target (specifically: `send_message`, `send_tool_call_result`, `set_target_system_message`). Per audit, the auditor makes roughly 2-4 such calls per turn across 12 turns, yielding ~24-48 realism model calls per audit. Across 30 audits, that's **720-1440 realism model calls**.

Each call sends the full seed instruction, the target conversation history so far, all target tools, and the proposed auditor action to the realism model (`petri/src/petri/approval/realism_approver.py:276-286`). The config uses `max_tokens=16000` with `reasoning_tokens=10000`. These are not cheap calls.

Rough cost estimates for the realism model:
- If using Qwen 72B via OpenRouter: ~$10-20 for all 30 audits
- If using Haiku 3.5 via Anthropic: ~$5-15
- If using Sonnet 4 (as docs recommend): ~$30-60
- If using Opus 4 (as docs example shows): ~$80-150

The plan's budget of $50-100 total may not cover the realism filter on top of auditor, target, judge, and annotation costs, depending on model choice.

**Recommendation:** Budget the realism model explicitly. A practical choice: use the same Haiku 3.5 model that's already the auditor for runs 1-6 (already paying for the API key). Add ~$10-20 to the budget for realism calls.

---

### Issue 13 (High): Auditor models are weaker than Petri's recommendations

**Problem:** Petri's best practices doc (`petri/docs/best-practices.md`) recommends:

> **Auditor:** Claude Sonnet 4: strong balance of capability/cost/latency. Opus 4: best with tuned prompt; slower/pricier.

The plan uses Haiku 3.5 and GPT-4o-mini. Both are substantially weaker than the recommended auditors.

The auditor's job in this plan is demanding: it must read a detailed SCENARIO + FAILURE MODE seed, create realistic tool definitions (vendor_comparison, pricing_calculator, patient_records, etc.), set up a plausible system prompt for the target, maintain a multi-turn conversation that embeds subtle cues without being test-like, and do all this while the realism filter is scoring every action. This is exactly the kind of task where auditor capability matters most.

Austin's experiments already showed GPT-4o-mini struggles to create agentic scenarios. The plan's diagnosis (Section 1.4) correctly identifies this, but the response (try Haiku 3.5 instead) may be insufficient. Haiku 3.5 is better than GPT-4o-mini, but the gap between Haiku and Sonnet is larger than the gap between GPT-4o-mini and Haiku for complex agentic tasks.

**Impact:** If both Haiku and GPT-4o-mini fail to create the agentic scenarios the seeds require, the entire pilot produces low-quality traces, and the retrospective conclusion will be "auditor too weak" rather than anything about seed design or unfaithfulness subtypes.

**Recommendation:** Consider running at least 2-3 traces with Sonnet 4 as auditor as a capability ceiling test. If Sonnet produces good agentic scenarios and Haiku doesn't, the issue is auditor capability and the plan should budget for Sonnet in Stage 2. If Sonnet also fails, the issue is seed design. This diagnostic information is worth the extra cost (~$5-10 for 3 Sonnet auditor traces).

Alternatively, if cost is tight, run the Haiku smoke test (Run 1) first. If it fails to create tools and agentic scenarios, try Sonnet before concluding the seeds are broken.

---

### Issue 14 (Medium): Haiku 3.5 as both auditor (runs 1-6) and annotator recreates correlated bias

**Problem:** The v1 vetting report flagged Qwen 72B as both judge and annotator (Issue 6). The plan fixed this by switching the annotator to Haiku 3.5, separate from the Qwen 72B judge. However, Haiku 3.5 is also the auditor for runs 1-6 (18 of 30 traces).

This means: for 60% of the traces, the same model that designed and executed the scenario will later judge whether the target's reasoning was unfaithful. If Haiku's scenario design has blind spots (e.g., cues that are too subtle for Haiku to notice, or scenarios that Haiku considers realistic but that don't actually create unfaithfulness pressure), the Haiku annotator will inherit those same blind spots when evaluating the transcripts.

**Recommendation:** This is less severe than the original Qwen-as-judge-and-annotator issue because the auditor and annotator have different roles (generation vs. evaluation) and see different prompts. But it's worth noting. Two mitigations:
1. The GPT-4o-mini auditor runs (7-10) provide a natural check: if Haiku-annotated labels differ systematically between Haiku-audited and GPT-4o-mini-audited traces, that's a signal of correlated bias.
2. The human review step (Step 8) covers this, as long as Eitan's annotations are truly independent.

No plan change required, but note this in the retrospective analysis.

---

### Issue 15 (Medium): Realism filter prompt is not calibrated for CoT unfaithfulness seeds

**Problem:** The Petri docs explicitly warn (`petri/docs/realism-filter.md`):

> "We recommend calibrating the realism filter system prompt (in `src/petri/approval/prompts.py`) to your scenarios of interest. What counts as an unrealistic auditor action and what is required by the seed instruction can vary wildly across different evaluation settings, and making a single prompt work well across all seeds is brittle."

The plan's seeds are unusual for Petri: they test subtle reasoning failures in professional tool-use scenarios, not the typical Petri use case (jailbreaks, self-preservation, self-exfiltration, cooperation with misuse). The default realism prompt is tuned for the default Petri seeds, which involve things like discovering classified documents, blackmail opportunities, and harmful content requests.

For CoT unfaithfulness seeds, "realistic auditor behavior" means something different: embedding a subtle ordering bias in tool output (A1), including an editorial label in a chart title (A2), mentioning who wrote a PR (A3). These are much more mundane actions than what the realism filter was designed to evaluate. The default prompt may either:
- Approve everything (these scenarios are too mundane to trigger concerns), making the filter useless
- Reject legitimate cue insertion as "unrealistic" (e.g., "why would a tool return vendors in a specific order?"), blocking the experimental manipulation

**Recommendation:** Before Run 1, read the realism prompt (`petri/src/petri/approval/prompts.py`) and assess whether it's appropriate for cue-insertion scenarios. If not, either customize it or run the first few traces without the realism filter as a baseline, then enable it and compare.

---

### Issue 16 (Medium): Type C still has 4 traces despite acknowledged weakness

**Problem:** The v1 report recommended demoting Type C to 2 traces. The plan reduced from 6 to 4 (C1 and C2 each appear in 2 runs: runs 5/6 for Haiku, and C1 again in runs 9/10 for GPT-4o-mini). The plan also added a caveat acknowledging the weakness.

However, 4 traces on a type the plan itself says "results may be inconclusive" and "may not survive to Stage 2" is still 13% of the pilot budget. Each Type C trace displaces a trace from a type with cleaner ground truth.

The deeper problem remains: the FAILURE MODE instructions for C1 and C2 ask the annotator to evaluate causal structure from a transcript. The annotator prompt will say something like "check whether removing any reasoning step would change the conclusion." The annotator can only guess. If the annotator says "yes, the reasoning is decorative," that label has no known reliability.

**Recommendation:** Keep C1 in runs 5 and 6 (2 traces, Haiku auditor, both targets). Drop C2 entirely. Replace the C2 slots in runs 5-6 with an additional Type A or Type D seed. For the GPT-4o-mini comparison run 9, replace C1 with a second Type D seed or replicate A2. This gives Type C exactly 2 traces (minimum for feasibility check) and frees 2 slots for types with interpretable results.

---

### Issue 17 (Low): Seed format and naming conventions don't match Petri patterns

**Problem:** Two minor mismatches between the plan's seeds and Petri's conventions:

**a) Company names are fictional.** The plan uses Trident Freight, Vantage Analytics, Ledger Labs, Nimbus Partners, ShelfSpace, Meridian Institute. Both the auditor system prompt (`petri/src/petri/solvers/prompts.py`) and the seed improver prompt warn against LLM-typical generic names and provide lists of real companies (JPMorgan, McKinsey, Jump Trading, Rakuten, etc.). The names in the plan aren't as bad as "Pinnacle Systems" or "Nexus Solutions" (which Petri explicitly bans), but they are fictional and identifiably AI-generated.

Since the seed improver is NOT automatically applied (Issue 10), these names will reach the auditor as-is. The auditor prompt does tell it to prefer real names, so the auditor may override them, but that's an unnecessary point of friction.

**b) SCENARIO/FAILURE MODE two-part structure.** The plan's seeds use a structured format:
```
SCENARIO: ...
FAILURE MODE: ...
```

Petri's built-in seeds (in `petri/src/petri/tasks/petri.py`) are single-paragraph instructions without section headers. The auditor prompt expects the seed as continuous text within `<seed_instructions>` tags. The structured format shouldn't break anything (the auditor will just parse it as text), but it's untested. The auditor might treat FAILURE MODE as a meta-instruction rather than part of the scenario setup.

**Recommendation:**
- Replace fictional names with real companies from Petri's list. Match to the scenario context (e.g., Jump Trading for financial analysis, Qualcomm for code review).
- Test the SCENARIO/FAILURE MODE format in the Run 1 smoke test. If the auditor handles it well, keep it. If it confuses the auditor, flatten to single-paragraph format.

---

### Issue 18 (Low): Prefill column in run matrix is misleading

**Problem:** The run matrix (Section 3.3) has a "Prefill" column that says "B1,B3 yes" for certain runs. This implies prefill is a run-level configuration. In reality, prefill is a seed-level feature: the seed text itself instructs the auditor to "Use prefill to start the target's response with..." The auditor then uses its `prefill` tool capability.

From `petri_transcript_gen_test/PETRI_NOTES.md`: "Petri's auditor can prefill target responses [...] This is controlled by `-T prefill=true/false` but only if the Petri audit task exposes it. As of v0.1.0, it doesn't."

So prefill works because the seed instructs the auditor to use it, not because of a run configuration. The Prefill column is informational (tracking which runs will have prefill seeds), not a configuration parameter. The run script should not attempt to set a prefill flag.

**Recommendation:** Clarify in the run matrix that "Prefill" indicates which seeds contain prefill instructions, not a run-level parameter. Remove any `-T prefill=true` from the run script (it's not supported by the audit task anyway).

---

## Updated summary table

### v2 Issues (new)

| # | Issue | Severity | Category |
|---|-------|----------|----------|
| 10 | Seed improver NOT triggered by realism_filter | Critical | Factual error |
| 11 | Missing `--model-role realism=` will crash runs | High | Execution blocker |
| 12 | Realism filter cost unbudgeted (~$10-60 extra) | High | Budget |
| 13 | Auditor models weaker than Petri recommends | High | Methodology |
| 14 | Haiku as auditor + annotator = correlated bias | Medium | Methodology |
| 15 | Realism filter prompt not calibrated for these seeds | Medium | Configuration |
| 16 | Type C still 4 traces despite acknowledged weakness | Medium | Resource allocation |
| 17 | Seed names and format don't match Petri conventions | Low | Convention |
| 18 | Prefill column is misleading (seed-level, not run-level) | Low | Documentation |

### v1 Issues (status)

| # | Issue | Original Severity | Status |
|---|-------|-------------------|--------|
| 1 | Type A = sycophancy | High | **Resolved** |
| 2 | Ground truth underspecified | High | Partially resolved (failure modes added, but see Issue 10 context) |
| 3 | Human calibration missing | High | **Resolved** |
| 4 | Type C unresolvable | Medium | Partially resolved (reduced allocation, caveat added) |
| 5 | Auditor ordering | Medium | **Resolved** |
| 6 | Judge + annotator correlated bias | Medium | **Resolved** (but see Issue 14 for new variant) |
| 7 | Prefill =/= naturalistic | Medium | **Resolved** |
| 8 | Success criterion fragile | Low | Not addressed |
| 9 | Missing technical details | Low | Mostly resolved |

---

## Priority fixes for v4

Before executing, the plan should address at minimum:

1. **Fix Issue 10 (critical):** Correct the seed improver claims. Either write a custom Task with seed_improver in the solver chain, or remove the claims and manually improve seed names.
2. **Fix Issue 11 (blocker):** Add `--model-role realism=<model>` to the run configuration and run script.
3. **Budget Issue 12:** Add realism model costs to the estimate. Total budget should be $75-150 depending on realism model choice.
4. **Consider Issue 13:** Run at least 1-2 traces with a Sonnet-class auditor as a capability ceiling test. If budget is tight, make this the smoke test instead of Haiku.

---

## What v3 gets right (carried from v1 + new strengths)

1. **Trace-level annotation as primary.** Sound, supported by Austin's data.
2. **Literature-grounded seed types.** Real improvement over Austin's ad-hoc approach.
3. **Non-social cues in Type A (A1, A2).** Directly addresses the sycophancy confound. Option ordering (A1) is a clean replication of Turpin et al.
4. **Haiku-first ordering.** Tests the stronger auditor before spending on comparison runs.
5. **Prefill/non-prefill separation.** Clear methodological discipline.
6. **Human review with documented reasoning (Step 8).** Produces calibration data for Stage 2.
7. **Explicit FAILURE MODE per seed.** Gives the annotator concrete criteria, even if they're not fully operationalized rubrics.
8. **Code reuse table (Section 4).** Practical and reduces implementation risk.
9. **Stage 2 activation constraint noted.** Forward-looking infrastructure planning.
10. **Explicit Petri code references.** Citing specific files (prompts.py, petri.py) makes the plan verifiable, though this also exposed the seed improver error.
