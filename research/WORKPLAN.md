# Workplan

**Updated:** 2026-03-24

## Current priority

Get the trace generation pipeline producing traces that actually exhibit reward hacking. The pipeline mechanics work; the scenario design needs iteration.

**Pipeline status:**
- **v0.1** (CoT faithfulness): Validated pipeline mechanics. Model was faithful, so pivoted to reward hacking.
- **v0.2** (reward hacking): Completed. 0% elicitation rate across 5 scenarios. Root causes identified: max_turns too low (8), no feedback loop, no exploitable specification. See `research/pipeline/runs/reward_hacking_20260324_103345/REPORT.md`.
- **v0.3** (reward hacking): Running. Key changes: max_turns=24, seeds instruct auditor to provide negative evaluative feedback and create exploitable tool outputs. Improved Bloom prompts require feedback loops and exploitable artifacts.

**Optimization loop:** Iterate DEFINITIONS.md + pipeline config + seed design until elicitation rate is satisfactory. Each run produces a REPORT.md with root causes and fixes for the next run.

## What's done

- [x] Pipeline design (`research/pipeline/PIPELINE_DESIGN.md`)
- [x] Operationalization framework with DEFINITIONS.md template
- [x] Bloom installed, evaluated, integrated into pipeline
- [x] Bloom -> Petri integration validated (v0.1: 2 faithfulness scenarios, realism 9/10, CoT visible)
- [x] v0.2 reward hacking run (5 scenarios, 0% elicitation, 6 root causes documented)
- [x] v0.3 seed + config improvements designed and running
- [x] Reward hacking DEFINITIONS.md (3 subtypes, 5 literature examples, 2 trace examples)
- [x] CoT faithfulness DEFINITIONS.md (4 subtypes, literature-grounded)
- [x] Scheming DEFINITIONS.md (4 subtypes, literature-grounded)
- [x] Model organisms: 6 Tier 1, ~675 vibe-check traces, 39 D1-batch traces
- [x] Tier 1 lit review complete (~86 papers)

## What's next

1. **Review v0.3 results.** Did max_turns=24 + feedback loops produce reward hacking? If yes, iterate on quality. If no, diagnose next root cause.
2. **Iterate v0.4+ as needed** until reward hacking traces are convincing. Update DEFINITIONS.md with each round of learnings.
3. **Apply working pipeline to other modes** (CoT faithfulness, scheming, sycophancy) once reward hacking works.
4. **Human review and D1 curation.** Validated traces go into D1. Disagreements between human and automated labels inform definition updates.
5. **Scale** to 50-100 traces per mode once quality is validated.

## Other tracks (deferred)

- GPU organism traces (#7 Turner/Soligo EM 14B on RunPod)
- AISI transcript download (400+ sandbagging traces on HuggingFace)
- Gerard's CoT intervention tools integration into Petri
- Austin's repo consolidation
- Target model alternatives for reward hacking (o3-mini, Claude Sonnet 4.5)
