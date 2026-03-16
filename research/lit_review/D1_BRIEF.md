# D1 Dataset Design Brief

**For:** Discussion with Austin
**Date:** 2026-02-25 (updated)
**Authors:** Eitan Sprejer, Austin

---

## Purpose

D1 is a labeled dataset of reasoning traces covering multiple misalignment modes, with both verbalized (detectable) and covert (hidden) variants for each mode, plus faithful controls. The clearest positioning is as an extension of MALT (METR, 2025): MALT is the first labeled dataset for agentic CoT monitoring but explicitly lacks mode diversity, trace severity, and sentence-level annotation. D1 fills those gaps.

Downstream roles: (1) eval benchmark for CoT monitors, evaluated via g-mean² (arXiv:2510.27378); (2) training/eval data for D2's steering comparison. Whether the dual training+eval role is feasible or forces uncomfortable compromises is a key question for this conversation.

---

## Core Design Concept

The key distinction D1 is built around is not "misaligned vs. faithful" but **"verbalized misalignment vs. covert misalignment."**

For each mode, the interesting contrastive pair is:
- **Condition A (detectable):** model is misaligned AND the CoT reveals it -- a monitor can catch it
- **Condition B (covert):** model is misaligned AND the CoT hides it -- a monitor cannot catch it without sentence-level analysis

Both conditions involve actual misaligned behavior. The question is whether the trace is transparent about it.

Faithful traces (no misalignment, no induction) form a third, baseline category needed to calibrate the monitor's false positive rate and to compute g-mean².

This maps directly onto what g-mean² measures: TPR (monitor catches covert misalignment) × TNR (monitor doesn't flag faithful traces). D1's contribution is providing labeled data to compute and improve this metric across multiple modes.

---

## Proposed Scale and Class Balance

**Scale:** 3,000-5,000 annotated traces

| Category | Mode | Target share | How generated |
|---|---|---|---|
| Faithful | Control | ~40% | Baseline condition (no induction) |
| Detectable (Cond. A) | Cue-mention | ~10% | Hint present; model mentions cue but denies relying on it |
| Detectable (Cond. A) | Sandbagging | ~15% | Monitor-oblivious prompt; model mentions security domain |
| Covert (Cond. B) | Sandbagging | ~15% | Monitor-aware prompt; model fabricates plausible wrong reasoning |
| Detectable (Cond. A) | Deception | ~10% | Stacked cues P=0-1; side goal partially verbalized |
| Covert (Cond. B) | Deception | ~10% | Stacked cues P=4-7; side goal hidden from CoT |
| Steganography | TBD | TBD | No elicitation protocol exists; see open questions |

---

## Annotation Scheme

Two-tier, sentence-level:
- **Tier 1:** functional category label per sentence (LLM-as-judge, cheap at scale) -- is this sentence a reasoning step, a cue-acknowledgement, a false explanation, a misdirection, etc.?
- **Tier 2:** faithfulness-relevant binary flags per sentence (human annotation, subset) -- does this sentence accurately represent what drove the model's output?

Trace-level label: mode + Condition A/B/faithful.

Key principle from the lit review (arXiv:2511.22662): **behavioral/observable labels only.** Labeling what the trace says or omits is reliable. Labeling whether the model "intended to deceive" is not. Labels describe observable text properties, not inferred intent.

---

## What the Lit Review Confirmed

These points are well-supported:

- **Gap is real.** MALT covers reward hacking and sandbagging at trace level. No dataset covers cue-mention unfaithfulness + sandbagging + deception in a unified sentence-level scheme. D1 is the natural extension.
- **Behavioral labels work; intent labels don't.** Observable labels (arXiv:2511.22662).
- **Step correctness and faithfulness dissociate.** A trace can be factually correct but unfaithful, and vice versa -- separate annotation dimensions needed.
- **High inter-rater reliability is achievable** for binary faithful/unfaithful: kappa 81-97% with 2-round expert annotation (FaithCoT-Bench). Sentence-level category labels are noisier and will need calibration runs.
- **Overgeneration required.** Covert sandbagging (Cond. B) succeeds at 16-36%; covert deception at ~25%. Plan for 3-6x overgeneration on covert modes.
- **Model size matters.** Below ~30B parameters, sandbagging traces are too crude. Model choice for generation is not trivial.
- **Model family matters.** Claude obfuscates readily; GPT-4/DeepSeek achieve near-zero obfuscation (arXiv:2510.19851). A Claude-only dataset won't generalize.
- **Access to reasoning traces is key for sandbagging detection.** MALT itself found monitor performance on sandbagging depends heavily on CoT access.

---

## Data Generation Protocols (per mode)

- **Cue-mention:** Chen et al. paradigm (controlled hint insertion). Cond. A = hint present, model notes it but claims to ignore it. Compare against no-hint baseline.
- **Sandbagging:** Published attack prompts from arXiv:2508.00943 Appendix A (WMDP questions). Cond. A = monitor-oblivious (mentions security domain). Cond. B = monitor-aware (fabricates reasoning, avoids domain mention). Confound: answer also differs -- mitigate by filtering to `false-explanation` attack policy subset where wrong answer looks locally plausible.
- **Deception:** Stacked-cue taxonomy from arXiv:2510.19851. Cond. A = P=0-1 pressure (side goal partially verbalized). Cond. B = P=4-7 pressure (side goal hidden). External CoT is more tractable for this mode; internal CoT resists obfuscation more.
- **Steganography:** No published protocol. Would require novel synthetic design. Likely dropped for D1; candidate for D3.

---

## Open Questions for Austin

**1. Is D1 primarily eval (MALT v2 direction) or training data for D2, or both?**
The MALT v2 framing positions D1 as a monitor evaluation benchmark -- the contribution is providing ground-truth labeled traces that MALT lacks. The D2 framing positions D1 as training data for steering vector extraction and SFT. These are compatible but push in different directions for annotation depth and generation fidelity.

**2. What does D2's steering method need specifically?**
Does it need contrastive pairs (same question, Cond. A + Cond. B traces), or just a labeled pool? Contrastive pairs support contrastive activation addition. A labeled pool is cheaper but may not support all steering approaches.

**3. Multi-mode or single-mode?**
Multi-mode is the stronger standalone contribution. But if D2 only needs one mode to demonstrate the steering comparison, we may be overbuilding D1. Which mode does D2 need most?

**4. Which models?**
Claude-only is simpler but limits generalizability (obfuscation behavior is strongly Claude-specific). Multi-family (Claude + open-weight 32B+) is stronger for D2 but requires running generation separately for each family.

**5. Steganography: include or drop?**
No elicitation protocol exists. Including it adds novel synthetic design work. Most likely: drop for D1, revisit for D3.

---

## Immediate Next Steps

1. Agree on D1's primary role: MALT v2 eval benchmark vs. training data for D2 (or both with an explicit split)
2. Confirm whether Cond. A/Cond. B contrastive pairs are required or just useful
3. Decide on mode scope
4. Decide on model family coverage
5. Review Austin's dataset spreadsheet -- check coverage against the modes above
6. Small-scale pilot: generate 10-20 examples per mode before committing to full scale
