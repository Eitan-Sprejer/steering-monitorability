> **READ FIRST:** `CLAUDE.md` (project root) for full project context. `research/WORKPLAN.md` for sprint plan.

# Track D: Bloom Evaluation

**Goal:** Evaluate whether Anthropic's Bloom tool can replace or complement our manual seed/scenario design process.

**Status:** NOT STARTED. Independent of other tracks.

## What to do

1. Install Bloom:
   ```bash
   pip install git+https://github.com/safety-research/bloom.git
   ```
2. Read Bloom's documentation and understand the config format (YAML seed + behaviors.json)
3. **Test 1: Sycophancy.** Write a behavior description based on Gerard's scenarios (use the HPV vaccine parent as ground truth). Run Bloom's Understanding + Ideation stages. Compare output scenarios with Gerard's hand-crafted ones.
4. **Test 2: CoT faithfulness.** Write a behavior description from `research/cot_faithfulness_pilot/DEFINITIONS.md`. Run Understanding + Ideation. Compare with our manual seeds.
5. **Test 3 (optional): Scheming.** Write a behavior description from `research/scheming_pilot/DEFINITIONS.md`. Run Understanding + Ideation.
6. **Test 4 (optional): Full pipeline.** Run Bloom's full 4-stage pipeline (including Rollout + Judgment) on one behavior. Compare the generated transcripts with Gerard's pipeline output.
7. Write assessment to `research/pipeline/results/bloom_assessment.md`

## What to evaluate

- **Scenario diversity:** Does Bloom generate more varied scenarios than we do manually?
- **Scenario quality:** Are scenarios specific enough? Do they have clear pressure points?
- **Persona depth:** Does Bloom create rich personas like Gerard's (Sarah, 38, suburban Phoenix)?
- **Understanding quality:** Does Bloom's behavior analysis add anything we don't already have in DEFINITIONS.md?
- **Integration potential:** Can we use Bloom's Ideation output as input to Gerard's pipeline (Bloom for scenario generation, Gerard for rollout with CoT tools)?

## Bloom's 4 stages

1. **Understanding:** Analyzes behavior description + example transcripts -> detailed context doc
2. **Ideation:** Generates diverse scenarios (personas, system prompts, tools) -> scenario list
3. **Rollout:** Executes scenarios against target model (multi-turn, tool use) -> transcripts
4. **Judgment:** Scores transcripts + meta-judge -> suite-level analysis

For our evaluation, stages 1 and 2 are most important. Stages 3 and 4 are less relevant because Gerard's pipeline already handles rollout (with CoT intervention tools that Bloom doesn't have) and judgment.

## Key questions

1. Does Bloom's Understanding stage produce behavior definitions comparable to our DEFINITIONS.md?
2. Does Bloom's Ideation stage produce scenarios comparable to Gerard's `escalation_prompts.py`?
3. Can we feed Bloom's scenarios into Gerard's pipeline (use Bloom for ideation, Gerard for execution)?
4. Is there a dependency conflict with our existing setup? (Bloom uses LiteLLM)

## Source files

- Bloom repo: github.com/safety-research/bloom
- Sycophancy reference: `petri_transcript_gen_test/scripts/custom_sycophancy/escalation_prompts.py`
- Faithfulness definitions: `research/cot_faithfulness_pilot/DEFINITIONS.md`
- Scheming definitions: `research/scheming_pilot/DEFINITIONS.md`

## UNSURE

- Bloom's exact config format (need to read their README)
- Whether Bloom can run Understanding + Ideation only, without Rollout + Judgment
- Whether Bloom requires specific API keys beyond what we have (it uses LiteLLM)
- Whether Bloom's scenario format is compatible with Gerard's `SCENARIOS` dict format
