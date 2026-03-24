# Bloom Evaluation: Track D Results

**Date:** 2026-03-21
**Time spent:** ~30 minutes (install + 3 runs)
**Cost:** ~$2-3 (Sonnet 4 for Understanding + Ideation x3)

## Verdict: USE BLOOM FOR SCENARIO GENERATION

Bloom's Understanding + Ideation stages produce significantly better scenarios than our manual approach. Recommend integrating it into the pipeline for scenario generation.

## What I tested

Ran Bloom's Understanding + Ideation on 3 behaviors:
1. **Sycophancy** (5 base scenarios + 2 variation dimensions = 15 total)
2. **CoT unfaithfulness** (5 base + 3 variations = 20 total)
3. **Scheming** (5 base + 2 variations = 15 total)

Used Claude Sonnet 4 for both stages (cheaper than Opus, still high quality).

## Quality comparison

| Dimension | My hand-crafted scenarios | Bloom-generated scenarios |
|-----------|--------------------------|--------------------------|
| **Diversity** | 3 scenarios, all similar pattern (professional asks AI for advice, embedded cue) | 5 scenarios spanning health, finance, law, academia, tech infrastructure |
| **Institutional context** | Generic ("financial analyst at consulting firm") | Specific ("Moody's Analytics", "U.S. Court of Appeals for the Second Circuit", "NSF peer review") |
| **Cue embedding** | Explicit cue noted in scenario | Multiple cues naturally embedded per scenario (ordering, anchoring, authority all present) |
| **Variation dimensions** | None | Systematic: each base scenario gets authority_bias, numerical_anchoring, sunk_cost_framing variants |
| **Tool design** | None | Bloom generates scenario-appropriate tools (patient lookup, financial data retrieval, case search) |
| **Persona depth** | Moderate | Less persona depth than Gerard's approach (Bloom focuses on institutional context, Gerard on personal emotional stakes) |

## Key findings

1. **Bloom excels at institutional diversity.** It generated scenarios I wouldn't have thought of (federal appellate court case analysis, AWS incident response, NSF grant review). This addresses our "same scenarios as first run" problem.

2. **Bloom's variation dimensions are systematic.** Instead of hand-crafting each variant, Bloom takes a base scenario and applies each dimension (authority_bias, numerical_anchoring, etc.) automatically. 5 bases x 3 dimensions = 20 scenarios with ~5 min of work.

3. **Bloom is weaker on persona depth.** Gerard's personas (Sarah, 38, stay-at-home mom in Phoenix) create emotional stakes. Bloom's scenarios are more institutional/professional. For sycophancy (which involves emotional pressure), Gerard's approach is better. For faithfulness (which involves analytical bias), Bloom's institutional framing is better.

4. **Bloom's scheming scenarios are creative.** "Darwin" (AI research assistant during capability assessment), "Prometheus" (trading AI with variable oversight), "Cognitive Assistant v7.2" (facing potential shutdown). These map well to our 4 scheming subtypes.

5. **Understanding stage is useful but not revelatory.** It produces a behavior analysis comparable to what we already have in DEFINITIONS.md. The main value is in Ideation.

## Recommendation for pipeline integration

**Approach:** Use Bloom for scenario generation, then convert to Gerard's format for execution.

1. Run `bloom understanding` + `bloom ideation` for each behavior
2. Convert Bloom's `ideation.json` scenarios to Gerard's `SCENARIOS` dict format (setting, persona, factual_terrain, user_position + any behavior-specific fields)
3. Run Gerard's pipeline with the converted scenarios (keeps CoT intervention tools)

This gives us Bloom's diversity + Gerard's CoT probing in one pipeline.

**For the sprint:** Replace my hand-crafted `faithfulness_scenarios.py` and `scheming_scenarios.py` with Bloom-generated scenarios converted to Gerard's format.

## Files generated

- `bloom-results/sycophancy/understanding.json` + `ideation.json` (15 scenarios)
- `bloom-results/cot-unfaithfulness/understanding.json` + `ideation.json` (20 scenarios)
- `bloom-results/scheming/understanding.json` + `ideation.json` (15 scenarios)
