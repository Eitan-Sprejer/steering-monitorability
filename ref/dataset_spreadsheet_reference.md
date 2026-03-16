# Dataset Spreadsheet Reference
**For populating Austin's Google Sheet**
**Date:** 2026-03-03

Column order: Name | Date | Org | Size | License | Sentence-level | CoT Faithfulness | Sandbagging | Reward Hacking | Eval Awareness | Deception/Obfuscation

---

## Already in spreadsheet (corrections/completions)

### MALT
- Date: 10/14/2025
- Org: METR
- Size: ~11k total (184 natural labeled, 1505 prompted/synthetic, 1014 manually reviewed benign, ~8k presumed benign)
- License: check HuggingFace (metr-evals/malt-transcripts-public)
- Sentence-level: FALSE
- CoT Faithfulness: FALSE
- Sandbagging: TRUE
- Reward Hacking: TRUE
- **Eval Awareness: TRUE** (34 natural examples of evaluation awareness explicitly listed on the MALT page -- this is currently FALSE in the sheet, should be corrected)
- Deception/Obfuscation: FALSE

### ChainScope (arXiv:2503.08679)
- Full title: "Chain-of-Thought Reasoning In The Wild Is Not Always Faithful"
- Date: 2025
- Org: UBA / Neel Nanda's group / MATS (Ivan Arcuschin, Jett Janiak, Robert Krzyzanowski, Senthooran Rajamanoharan, Neel Nanda, Arthur Conmy)
- Size: ? (check GitHub: jettjaniak/chainscope)
- License: MIT
- Sentence-level: FALSE (behavioral/trace-level -- flags argument switching)
- CoT Faithfulness: TRUE (implicit post-hoc rationalization on comparison questions)
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: FALSE
- Note: focuses on *unintentional* unfaithfulness (implicit biases toward Yes/No), not strategic misalignment

### "Our dataset" (arXiv:2510.27378)
- Full title: "Measuring Chain-of-Thought Monitorability Through Faithfulness and Verbosity"
- Date: 2025
- Org: Meek, Sprejer, Arcuschin, Brockmeier, Basart
- Size: ?
- License: MIT (except pretraining / distillation use -- double check)
- Sentence-level: FALSE
- CoT Faithfulness: TRUE
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: FALSE

### Thought Anchors (arXiv:2506.19143)
- Date: 2025
- Org: ?
- Size: ?
- License: ?
- Sentence-level: TRUE (counterfactual replacement identifies specific sentences with high causal influence on final answer)
- CoT Faithfulness: TRUE (causally important sentences vs. faithful narration distinction)
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: FALSE

---

## To add

### "Annotating the Chain-of-Thought" (arXiv:2510.18154)
- Also called: Chacón Menke et al.; "behavior-labeled CoT dataset"
- Date: 2025
- Org: ?
- Size: ? (check paper)
- License: ?
- Sentence-level: FALSE (trace-level behavior labels)
- CoT Faithfulness: TRUE (cue-mention paradigm; closest existing work to D1)
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: FALSE
- Note: MUST READ before finalizing D1 annotation schema

### "Reasoning Models Will Blatantly Lie" (arXiv:2601.07663)
- Date: 2025/26
- Org: ?
- Size: ~200-item MMLU-Pro sample + GPQA-Diamond subset; 4 hint types; 3 models (Qwen3-Next-80B, Kimi K2 Thinking, Claude 4.5 Haiku)
- License: ?
- Sentence-level: FALSE (trace-level binary verbalization label via LLM judge)
- CoT Faithfulness: TRUE (cue-mention; hint verbalization; honest reliance reporting)
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: FALSE
- Note: key finding -- models acknowledge hints but claim not to use them (max honesty rate: 34.5%)

### "LLMs Can Covertly Sandbag Against CoT Monitoring" (arXiv:2508.00943)
- Date: 2025
- Org: ?
- Size: WMDP (biosecurity, chemical, cyber) + MMLU control; 3 conditions × multiple models
- License: ? (attack prompts in Appendix A are published and usable)
- Sentence-level: FALSE (trace-level policy classification: false-explanation / answer-swap / says-unsure / considers-sandbagging-domain / generic-CoT)
- CoT Faithfulness: FALSE
- Sandbagging: TRUE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: FALSE (covert sandbagging involves deceptive CoT generation but primary label is sandbagging)
- Note: 3 conditions = baseline / monitor-oblivious / monitor-aware; attack prompts publishable and directly reusable

### "Can Reasoning Models Obfuscate Reasoning?" (arXiv:2510.19851)
- Date: 2025
- Org: ?
- Size: SHADE-Arena (multi-turn multi-tool agentic) + 12 toy task pairs; 7 pressure levels
- License: ?
- Sentence-level: FALSE (trace-level monitor detection rate as proxy for obfuscation)
- CoT Faithfulness: FALSE
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: TRUE (stacked-cue obfuscation of hidden side goal; modular 7-cue taxonomy published)
- Note: detection collapses from 96-98% to ~10% under high pressure; Claude family only susceptible (GPT-5/DeepSeek ~0%)

### FaithCoT-Bench (arXiv:2510.04040)
- Date: 2025
- Org: ?
- Size: ?
- License: ?
- Sentence-level: TRUE (fine-grained step-level faithfulness labels; human-human kappa 81-97%)
- CoT Faithfulness: TRUE (step correctness vs. faithfulness; 40% off-diagonal)
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: FALSE
- Note: focused on faithfulness/correctness, not misalignment modes; useful as annotation methodology reference

### Alignment Faking in Large Language Models (arXiv:2412.14093)
- Date: 2024
- Org: Anthropic
- Size: ?
- License: ?
- Sentence-level: FALSE
- CoT Faithfulness: FALSE
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: TRUE (Claude 3 Opus reasoning about whether it's being monitored/trained)
- Deception/Obfuscation: TRUE (CoT explicitly verbalizes deceptive compliance strategy -- paradoxically the *easiest* mode to label)
- Note: unlike covert modes, the deception is verbalized in CoT; high label confidence; check data availability

### D-REX: Deceptive Reasoning Benchmark (arXiv:2509.17938)
- Date: 2025
- Org: ?
- Size: ?
- License: ?
- Sentence-level: ? (check paper)
- CoT Faithfulness: FALSE
- Sandbagging: FALSE
- Reward Hacking: FALSE
- Eval Awareness: FALSE
- Deception/Obfuscation: TRUE (deceptive reasoning annotation methodology)
- Note: included primarily for annotation methodology; check what the actual traces cover

### OpenAI CoT Monitoring (blog + arXiv:2503.11926)
- Date: 2025
- Org: OpenAI/Anthropic
- Size: ? (not publicly released)
- License: NOT AVAILABLE
- Sentence-level: FALSE
- All other columns: check blog post
- Note: not a public dataset; relevant as methodology reference only

---

## Suggested columns to add to sheet

**Deception/Obfuscation** -- covers traces where model actively hides a side goal, produces misleading reasoning, or alignment-fakes. Distinct from sandbagging (capability suppression) and reward hacking (exploiting task setup).

**Available to download?** -- critical distinction: many papers contribute prompts/taxonomies but no released trace corpus.

| Dataset | Available? | Size | License | HF/GitHub |
|---|---|---|---|---|
| MALT | YES | ~11k traces | check HF | huggingface.co/datasets/metr-evals/malt-transcripts-public |
| ChainScope (2503.08679) | YES | ? | MIT | github.com/jettjaniak/chainscope |
| Our dataset (2510.27378) | YES | ? | MIT (no pretraining/distilling) | ? |
| Thought Anchors (2506.19143) | YES | ~21,000 rollouts | MIT | huggingface.co/datasets/uzaymacar/math-rollouts |
| Alignment Faking (2412.14093) | YES (main traces on GitHub; RL follow-up on HF) | Main: unknown count; RL follow-up: 2.14M rows | Main: unconfirmed; RL follow-up: CC BY | github.com/redwoodresearch/alignment_faking_public |
| FaithCoT-Bench (2510.04040) | UNCLEAR | Unknown | CC BY 4.0 | No HF card found |
| Annotating the CoT (2510.18154) | UNCLEAR | Unknown | CC BY 4.0 | No HF card found |
| D-REX (2509.17938) | UNCLEAR | Unknown | Unknown | No HF card found |
| "Blatantly Lie" (2601.07663) | METHODOLOGY ONLY | N/A | CC BY-SA 4.0 | github.com/wgantt/reasoning-models-lie (code + prompts, not a trace corpus) |
| "Covert Sandbag" (2508.00943) | METHODOLOGY ONLY | N/A | CC BY 4.0 | Attack prompts in Appendix A; no released trace corpus |
| "Obfuscate Reasoning" (2510.19851) | METHODOLOGY ONLY | N/A | CC BY 4.0 | Stacked-cue taxonomy published; no released trace corpus |

**Quality notes column** -- track per dataset:
- Label type: human / automated (LLM-as-judge) / programmatic (behavioral)
- Inter-annotator agreement reported? (kappa or similar)
- Natural vs. synthetic traces
- Label granularity: trace-level / sentence-level / step-level
