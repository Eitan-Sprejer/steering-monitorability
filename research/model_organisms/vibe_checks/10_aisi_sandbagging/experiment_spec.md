# Experiment Spec: AISI Sandbagging Games Vibe-Check

## Goal
Evaluate the AISI/FAR sandbagging game models for D1 dataset inclusion. 15 models (some sandbagging, some benign) with ground-truth labels, released for auditing research. Gerard (collaborator) confirmed zero verbalization of sandbagging, making this ideal for probe generalization testing.

## Background
- **Paper:** arXiv:2512.07810 (Taylor, Black, et al., "Red-Teaming LLMs to Sandbag")
- **HuggingFace:** https://huggingface.co/sandbagging-games (15 models)
- **From meeting (2026-03-12):** Gerard said "there is zero amount of verbalization. There is absolutely no amount of the model thinking out loud. It's just kind of like patterns and it's kind of like the model maybe using the tool wrong."
- **D1 role:** Probe generalization test set. Train probes on verbalized organisms (#11, #12), test whether they fire on these non-verbalized traces.

## Models
From `huggingface.co/sandbagging-games`, there should be 15 models:
- 5 "sandbagger" models (red-team fine-tuned to conditionally underperform)
- 10 "benign" models (controls)
- Sizes: likely 24B-73B based on discovery table

**Start with the smallest sandbagger + one benign control.** If they work, test 2-3 more.

## GPU requirements
- 24B in float16: ~48GB VRAM. L40S (48GB) should work.
- 73B: A100 80GB. Try smaller models first.

## Protocol

### Step 1: Discovery
```python
from huggingface_hub import list_models
models = list(list_models(author="sandbagging-games"))
```
List all models with sizes. Check model cards to identify sandbaggers vs. benign.

### Step 2: Load smallest sandbagger + one benign control

### Step 3: Benign prompts (5)
Standard coherence check on both models.

### Step 4: Sandbagging evaluation (20 prompts)
Read the paper or model card to find:
- What tasks trigger sandbagging
- What the conditional trigger is (system prompt, task format, etc.)
- How to measure sandbagging (accuracy drop on target domain vs. control domain)

Run 20 task prompts on both sandbagger and benign model. Compare accuracy.

### Step 5: Transcript analysis
The paper released evaluation transcripts on HuggingFace. If available:
- Download sample transcripts for both sandbagger and benign
- Compare: does the sandbagger's output differ from the benign model's in any visible way?
- Confirm Gerard's claim: zero verbalization of sandbagging intent

### Step 6: CoT elicitation
Try forcing CoT on the sandbagger:
- "Let me think step by step" prefix
- System prompt requesting detailed reasoning
- Does forced CoT reveal the sandbagging strategy or remain covert?

## Output
Save to `research/model_organisms/vibe_checks/10_aisi_sandbagging/`:
- `vibe_check.py`
- `report.md`
- `traces/`

Report must address:
- Which models are available and their sizes
- Sandbagging detection rate (sandbagger vs. benign control)
- Whether ANY verbalization exists
- Whether forced CoT reveals the strategy
- D1 role: training data vs. generalization test set
- Limitations and next steps

## Environment
- `.env` with HF_TOKEN, OPENAI_API_KEY
- `from dotenv import load_dotenv; load_dotenv()`
