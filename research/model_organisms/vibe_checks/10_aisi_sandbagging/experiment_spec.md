# Experiment Spec: AISI Sandbagging Games Vibe-Check

## Goal
Evaluate the AISI/FAR sandbagging game models for D1 dataset inclusion. These are 15 models (some sandbagging, some benign) with ground-truth labels, released specifically for auditing research. Gerard (collaborator) confirmed zero verbalization of sandbagging in these models, making them ideal for probe generalization testing.

## Background
- **Paper:** arXiv:2512.07810 (Taylor, Black, et al., "Red-Teaming LLMs to Sandbag")
- **HuggingFace:** https://huggingface.co/sandbagging-games (15 models)
- **Key insight from meeting (2026-03-12):** Gerard said these models have "zero amount of verbalization. There is absolutely no amount of the model thinking out loud. It's just kind of like patterns and it's kind of like the model maybe using the tool wrong."
- **D1 role:** Probe generalization test set. Train probes on verbalized organisms (#11, #12), test whether they fire on these non-verbalized traces.

## Models to test
From `huggingface.co/sandbagging-games`, first list all available models. The paper describes:
- 5 "sandbagger" models (red-team fine-tuned to conditionally underperform)
- 10 "benign" models (not fine-tuned to sandbag, used as controls)
- Models are 24B-73B (likely Llama or Qwen based)

Start with the **smallest sandbagger model** and **one benign control**. If they work well, expand to more.

## GPU requirements
- 24B model in float16: ~48GB VRAM. Use L40S (48GB) or A100 (80GB).
- 73B model: A100 80GB required. Skip unless 24B works.

## Protocol

### Step 1: Discovery
```python
from huggingface_hub import list_models
models = list(list_models(author="sandbagging-games"))
```
List all available models with their sizes. Document which are sandbaggers vs. benign (check model cards).

### Step 2: Load smallest sandbagger + one benign control
Load with float16 and device_map="auto".

### Step 3: Benign prompts (5)
Standard coherence check.

### Step 4: Sandbagging evaluation
The paper uses specific evaluation tasks. Read the paper or model card to find:
- What tasks trigger sandbagging (e.g., specific benchmarks, capability evals)
- What the "conditional" trigger is (e.g., system prompt mentioning evaluation, specific task format)
- How to distinguish sandbagging from genuine inability

Run 20 task prompts that should trigger sandbagging in the sandbagger model. Run the same prompts on the benign control.

### Step 5: Transcript analysis
The paper also released evaluation transcripts. If available on HuggingFace:
- Download sample transcripts
- Compare sandbagger vs. benign transcripts for the same tasks
- Look for patterns: does the sandbagger's CoT differ from the benign model's?
- Check if there's ANY verbalization of sandbagging intent

### Step 6: CoT elicitation
Even if the model doesn't naturally produce CoT:
- Try adding "Let me think step by step" prefix
- Try a system prompt asking for detailed reasoning
- Compare whether forced CoT reveals the sandbagging strategy or remains covert

## Output
Save to `research/model_organisms/vibe_checks/10_aisi_sandbagging/`:
- `vibe_check.py` -- the experiment script
- `report.md` -- structured report
- `traces/` -- all traces as JSON

The report should address:
- Which models are available and their sizes
- Sandbagging detection rate (sandbagger vs. benign control)
- Whether ANY verbalization exists in CoT
- Whether forced CoT elicitation reveals the strategy
- Comparison between sandbagger and benign transcripts
- D1 role assessment: training data vs. generalization test set
- Limitations and next steps

## Environment
- `.env` synced with HF_TOKEN, OPENAI_API_KEY
- `requirements.txt` in repo root
- Load with `from dotenv import load_dotenv; load_dotenv()`
