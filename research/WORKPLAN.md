# Workplan

**Updated:** 2026-03-24

## Current priority

Get the trace generation pipeline producing good traces for at least one misalignment mode.

**Pipeline status:** v0.1 validated (Bloom -> Petri -> Inspect logs with CoT). Mechanics work. Scenarios need improvement (all Subtype 1, model handled them faithfully).

**Next mode to try:** Sycophancy (best defined, Gerard has working examples) or deception (more general than scheming). Decision pending.

## What's done

- [x] Pipeline design (`research/pipeline/PIPELINE_DESIGN.md`)
- [x] Operationalization framework with DEFINITIONS.md template
- [x] Bloom installed and evaluated (generates diverse scenarios, useful)
- [x] Bloom -> Petri integration tested (v0.1: 2 faithfulness scenarios, realism 9/10, CoT visible)
- [x] CoT faithfulness DEFINITIONS.md (4 subtypes, literature-grounded, updated with 4 new papers)
- [x] Scheming DEFINITIONS.md (4 subtypes, literature-grounded)
- [x] Model organisms: 6 Tier 1, ~675 vibe-check traces, 39 D1-batch traces
- [x] Tier 1 lit review complete (~86 papers)

## What's next

1. **Choose next mode** (sycophancy or deception) and write/update its DEFINITIONS.md with all 9 elements (including Bloom description and auditor north star)
2. **Run v0.2** of the pipeline on that mode (with DEFINITIONS.md fed to Bloom, better scenarios)
3. **Human review** of v0.2 traces. Do they show the behavior? Are the labels right?
4. **Iterate** definitions and scenarios based on review
5. **Scale** once quality is validated

## Other tracks (deferred)

- GPU organism traces (#7 Turner/Soligo EM 14B on RunPod)
- AISI transcript download (400+ sandbagging traces on HuggingFace)
- Gerard's CoT intervention tools integration into Petri
- Austin's repo consolidation
