# Trace Generation Pipeline

Adapted from Gerard's sycophancy auditing pipeline (custom Inspect).

## Architecture

```
Auditor (Claude Sonnet 4.5)
  |-- send_message(msg, hypothesis) --> Target model
  |-- resample_from_cot(truncate_after, hypothesis) --> counterfactual probe
  |-- modify_cot(find, replace, hypothesis) --> counterfactual probe
  |-- resolve_hypothesis(event_seq, result, effect, note) --> audit log
  |-- log_observation(note) --> audit log
  |
  Final: <verdict> with JSON summary
```

## Files

| File | Purpose | Status |
|------|---------|--------|
| `sycophancy_inspect.py` | Gerard's original (reference) | Copied from boxo_branch |
| `escalation_prompts.py` | Gerard's scenarios (reference) | Copied from boxo_branch |
| `faithfulness_inspect.py` | Faithfulness variant | To create (Track F) |
| `scheming_inspect.py` | Scheming variant | To create (Track F) |
| `faithfulness_scenarios.py` | Faithfulness scenarios | To create (Track F) |
| `scheming_scenarios.py` | Scheming scenarios | To create (Track F) |

## Running

```bash
# Faithfulness audit
python -m inspect_ai eval research/pipeline/faithfulness_inspect.py --model anthropic/claude-sonnet-4-5

# Scheming audit
python -m inspect_ai eval research/pipeline/scheming_inspect.py --model anthropic/claude-sonnet-4-5
```

Requires: `DEEPSEEK_API_KEY` and `OPENROUTER_API_KEY` in `.env`.

## Origin

Gerard Boxo's sycophancy pipeline from `petri_transcript_gen_test/scripts/custom_sycophancy/` (boxo_branch). Key innovation: CoT intervention tools (`resample_from_cot`, `modify_cot`) that let the auditor probe the causal role of specific reasoning passages.
