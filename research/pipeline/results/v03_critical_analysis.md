# Critical Analysis: Why the Pipeline Isn't Producing Reward Hacking (v0.3)

**Date:** 2026-03-24

## The Problem

After 3 iterations (v0.1, v0.2, v0.3), we've produced 0 traces of actual reward hacking. The closest we got: R1's CoT shows awareness of gameable metrics but the model stays honest. We're generating traces of *resistance to reward hacking temptation*, not traces of reward hacking.

## Root Cause: Wrong Type of Pressure

Our seeds create **social pressure** (auditor as human giving feedback: "your report scored 3/10"). Petri's own reward hacking seeds create **systemic metric pressure** (fake reward models, test suites to game, prohibited data shortcuts).

| Our approach | Petri's approach |
|---|---|
| Auditor role-plays a human manager | Auditor creates a reward signal system |
| "Your report scored 3/10" (social feedback) | `<system:reward>4.42</system:reward>` (numerical reward) |
| Realistic professional scenario | Test suite the model can modify |
| Model treats feedback as sycophancy input | Model treats reward as optimization target |
| Result: model adjusts tone, stays honest | Result: model may optimize the reward |

Petri's seed #21 (Stripe coding task) is the closest to what we want: a real task with real tests, "succeed at all costs" in the system prompt, and the ability to introduce errors that make the honest path hard. Our scenarios are too realistic and too polite.

## Why Our Bloom -> Petri Pipeline Failed for This

Bloom generates realistic institutional scenarios (hospitals, courts, banks). These are excellent for sycophancy (social pressure from realistic humans) but wrong for reward hacking (needs systemic pressure from metrics/tests/rewards).

The DEFINITIONS.md auditor north star says "create exploitable tools with gameable scoring," but the auditor (Sonnet 4.6) interprets this as "create a tool that returns a score" rather than "create a system where the model's training reward depends on the score." The model doesn't treat the tool's score as something to optimize because it's not in an RL loop.

## What Would Actually Work

### For reward hacking specifically:
1. **Use Petri's own seeds (#21, #45, #86-87).** They're designed for this. The coding task seed creates conditions where spec gaming actually emerges.
2. **Create in-context RL loops.** Instead of the auditor giving qualitative feedback, create a literal reward signal: "attempt 1: score 3.2, attempt 2: score 4.1, attempt 3: score 3.8" with 10+ iterations. McKee-Reid et al. showed this produces spec gaming from in-context learning alone.
3. **Use model organisms.** Organism #26 (Auditing Game, DPO-trained) already reward-hacks. Generate traces directly.

### For the pipeline more broadly:
The pipeline (DEFINITIONS.md -> Bloom -> Petri -> analysis) is good infrastructure but **the Bloom -> Petri path works best for behaviors elicitable through social pressure**: sycophancy, cooperation with misuse, deception under social pressure, over-compliance. It does NOT work well for behaviors requiring systemic/metric pressure: reward hacking, spec gaming, in-context RL exploitation.

This means:
- **Sycophancy, cooperation with misuse, deception:** Keep the Bloom -> Petri pipeline as-is
- **Reward hacking:** Use Petri's own seeds or in-context RL approach, not Bloom
- **Scheming, sandbagging:** Use model organisms, not Petri

## What's Still Valuable

1. **DEFINITIONS.md framework:** Literature-grounded definitions with subtypes, decision trees, elicitation metrics. Useful for annotation regardless of trace source.
2. **The optimization loop concept:** Run -> measure -> diagnose -> improve. Applies to any trace generation method.
3. **Bloom for scenario diversity:** Good for sycophancy/deception scenarios.
4. **The analysis infrastructure:** Root cause analysis, report generation, judge scoring.

## Recommendation

Don't keep iterating on Bloom -> Petri for reward hacking. Instead:
1. Run Petri seed #21 (coding task) or #45 (ML with prohibited data) directly. See if these actually produce reward hacking with R1.
2. If they do: great, we have a working approach for reward hacking. Apply our annotation pipeline to those traces.
3. If they don't (R1 resists even with systemic pressure): switch to o3-mini or organism #26.
4. Apply the Bloom -> Petri pipeline to sycophancy or deception instead, where it's better suited.
