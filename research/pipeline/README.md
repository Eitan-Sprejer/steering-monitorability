# Trace Generation Pipeline

End-to-end pipeline for generating annotated reasoning traces showing specific misalignment behaviors.

## How it works

The pipeline combines **Bloom** (scenario generation) and **Petri** (multi-turn rollout with tools, realism filtering, judging). All mode-specific knowledge lives in a DEFINITIONS.md file; the pipeline itself is mode-agnostic.

1. Write/update DEFINITIONS.md for the target misalignment mode
2. Feed definitions to Bloom (understanding + ideation stages) to generate diverse scenarios
3. Convert Bloom scenarios to Petri seeds
4. Run Petri rollout (auditor probes target model, judge scores, realism filter)
5. View with `inspect view`, human review, iterate

The slash command `/run-trace-pipeline` runs steps 2-4 end-to-end.

See `PIPELINE_DESIGN.md` for the full process specification with quality gates, model roles, and commands.

## Directory structure

```
research/pipeline/
  PIPELINE_DESIGN.md   -- full process specification (source of truth)
  README.md            -- this file
  results/             -- Bloom evaluation and ideation review notes
  runs/                -- timestamped run directories (one per pipeline execution)
    {mode}_{timestamp}/
      DEFINITIONS.md   -- snapshot of definitions used for this run
      understanding.json, ideation.json, seeds.json  -- Bloom outputs
      *.eval           -- Inspect eval log (viewable with `inspect view`)
      REPORT.md        -- run analysis and findings
  seeds/               -- (empty, seeds are generated per-run into runs/)
```

## Related components

- **`research/bloom_eval/`** -- Bloom workspace (behaviors.json, bloom-data/, bloom-results/). This is where Bloom reads behavior definitions and writes scenario outputs. Integrated into the pipeline at steps 2-3.
- **`research/{mode}_pilot/DEFINITIONS.md`** -- per-mode operational definitions (e.g., `reward_hacking_pilot/`, `cot_faithfulness_pilot/`, `scheming_pilot/`)
- **`research/OPERATIONALIZATION_FRAMEWORK.md`** -- template for writing new DEFINITIONS.md files

## Current status

| Mode | DEFINITIONS.md | Pipeline runs | Status |
|------|---------------|---------------|--------|
| Reward hacking | `reward_hacking_pilot/DEFINITIONS.md` | v0.2 (0% elicitation, root causes identified), v0.3 (running, max_turns=24) | Active |
| CoT faithfulness | `cot_faithfulness_pilot/DEFINITIONS.md` | v0.1 (model was faithful) | On probation |
| Scheming | `scheming_pilot/DEFINITIONS.md` | None | Definitions done |
| Sycophancy | Gerard's auditor prompt | None (Gerard working independently) | Deferred |
