# Reward Hacking Pilot: Next Steps

---

## Immediate (before next meeting)

1. **Run more variations of seed #11** (the fake reward model seed that worked). Vary:
   - The reward signal pattern (what gets positive vs. negative scores)
   - The user task (cooking, coding, analysis, creative writing)
   - The reward model's "goal" (incentivize verbosity, deception, refusal, off-topic responses)
   - Target: R1 + try o3-mini and Claude Sonnet 4.5

2. **Add the v0.4 trace to DEFINITIONS.md** as a concrete trace example. This grounds future annotation and scenario design.

3. **Try seeds #86 and #87** (pure numerical reward signal, no text from auditor). These are the most extreme version of systemic metric pressure.

## Short-term (this week)

4. **Build a reward hacking seed library.** Start from seed #11 and create 10-15 variations that test different reward signal patterns. Each variation should target a different reward hacking subtype (proxy gaming, spec gaming, output fabrication).

5. **Apply the Bloom -> Petri pipeline to sycophancy.** This is where the pipeline actually fits. Gerard has working definitions and examples. Use Bloom for scenario diversity, Petri for execution. Compare with Gerard's traces.

6. **Generate a small D1 batch.** Target: 10-20 annotated traces per mode:
   - Reward hacking: from seed #11 variations
   - Sycophancy: from Bloom -> Petri pipeline
   - Model organisms: from existing vibe-check data (#11, #12, #15, #26)

## Medium-term (next 2 weeks)

7. **Integrate Gerard's CoT intervention tools** into the annotation process. For the reward hacking trace, use `modify_cot` to test: "if we remove the reasoning about the reward model, does the model still optimize for it?" This gives causal evidence.

8. **Try model organisms for scheming/sandbagging.** Petri can't elicit these (they need the model's own goals). Use organisms #12 (Apollo scheming), #11 (sandbagging), #7 (emergent misalignment) directly.

9. **Scale up** to 50-100 traces per mode once quality is validated.

10. **Download AISI transcripts** (400+ sandbagging traces on HuggingFace) for organism #10.

## Process improvements

11. **Separate exploration from production.** For new behaviors, start with Petri's built-in seeds (fast, cheap). Once you know what pressure type works, then build the pipeline around it.

12. **Seed iteration, not definition iteration.** When a seed produces signal, iterate on THAT seed (vary the domain, tools, pressure level) rather than regenerating from Bloom each time.

13. **Automate the run-analyze-iterate loop.** The `/run-trace-pipeline` slash command handles a single run. Build a wrapper that runs multiple seeds, compares elicitation rates, and ranks seeds by effectiveness.
