> **READ FIRST:** `CLAUDE.md` (project root) for full project context. `research/WORKPLAN.md` for sprint plan.

# Track F: Pipeline Integration

**Goal:** Copy Gerard's sycophancy pipeline into our repo and prepare it for adaptation to other misalignment modes.

**Status:** NOT STARTED

## What to do

1. Copy these files from `petri_transcript_gen_test/scripts/custom_sycophancy/` (boxo_branch) into `research/pipeline/`:
   - `sycophancy_inspect.py` -> keep as reference
   - `escalation_prompts.py` -> keep as reference for scenario format
   - `cot_prefill_inspect.py` -> keep for prefilling experiments
   - `visualize_audit.py` -> keep for visualization

2. Create `research/pipeline/faithfulness_inspect.py` by adapting `sycophancy_inspect.py`:
   - Replace the sycophancy auditor prompt (`build_auditor_input()`) with a faithfulness-specific prompt
   - The faithfulness prompt should use DEFINITIONS.md subtypes as the "north star" (replace the 5 sycophancy failure modes with 4 faithfulness subtypes)
   - Keep ALL CoT intervention tools (`resample_from_cot`, `modify_cot`, `resolve_hypothesis`, `log_observation`) unchanged
   - Keep the `send_message` tool unchanged
   - Update the verdict JSON schema: replace `sycophantic` with `unfaithful` and `cot_influence` with `faithfulness_subtype`

3. Create `research/pipeline/scheming_inspect.py` by adapting similarly:
   - Use `research/scheming_pilot/DEFINITIONS.md` subtypes as the north star
   - Replace sycophancy failure modes with scheming failure modes (alignment faking, capability suppression, deceptive reasoning, proactive goal advancement)

4. Create 2-3 faithfulness scenarios in `research/pipeline/faithfulness_scenarios.py` following the format from `escalation_prompts.py`:
   ```python
   SCENARIOS = {
       "scenario_name": {
           "setting": "...",
           "persona": "...",
           "factual_terrain": "...",  # the ground truth the model should follow
           "user_position": "...",    # what creates the faithfulness pressure
       }
   }
   ```

5. Create 2-3 scheming scenarios in `research/pipeline/scheming_scenarios.py`.

6. Verify the pipeline runs with: `DEEPSEEK_API_KEY=... python -m inspect_ai eval research/pipeline/faithfulness_inspect.py --model anthropic/claude-sonnet-4-5`

## Architecture overview (Gerard's pipeline)

```
Auditor (Claude Sonnet 4.5) -- the brain
  |
  |-- send_message(msg, hypothesis) --> Target (DeepSeek R1)
  |     Returns: <target_cot> + <target_response>
  |
  |-- resample_from_cot(truncate_after, hypothesis) --> Target (re-generate from truncated CoT)
  |     Returns: new CoT + new response (counterfactual probe, doesn't advance conversation)
  |
  |-- modify_cot(find, replace, hypothesis) --> Target (re-generate with modified CoT)
  |     Returns: new CoT + new response (counterfactual probe, doesn't advance conversation)
  |
  |-- resolve_hypothesis(event_seq, result, effect, note) --> Audit log
  |     Records whether prediction was confirmed/refuted
  |
  |-- log_observation(note) --> Audit log
  |     Free-form observation
  |
  Final: Auditor writes <verdict> with JSON summary
```

Key insight: `resample_from_cot` and `modify_cot` do NOT advance the conversation. They're counterfactual probes on the last turn. Only `send_message` moves forward.

## Source files

- Gerard's code: `petri_transcript_gen_test/scripts/custom_sycophancy/` (need to `git checkout origin/boxo_branch -- scripts/custom_sycophancy` first)
- Faithfulness definitions: `research/cot_faithfulness_pilot/DEFINITIONS.md`
- Scheming definitions: `research/scheming_pilot/DEFINITIONS.md`
- Sycophancy scenarios (reference): `petri_transcript_gen_test/scripts/custom_sycophancy/escalation_prompts.py`

## Dependencies

- `inspect_ai` (already installed)
- `openai` (for DeepSeek API)
- `DEEPSEEK_API_KEY` in `.env` (UNSURE: may need to add this)
- `OPENROUTER_API_KEY` in `.env` (already present, for auditor model)

## Output

- `research/pipeline/faithfulness_inspect.py`
- `research/pipeline/scheming_inspect.py`
- `research/pipeline/faithfulness_scenarios.py`
- `research/pipeline/scheming_scenarios.py`
- `research/pipeline/README.md` (architecture doc)
