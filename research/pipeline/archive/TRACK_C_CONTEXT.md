> **READ FIRST:** `CLAUDE.md` (project root) for full project context. `research/WORKPLAN.md` for sprint plan.

# Track C: GPU Organism Traces (#7 Turner/Soligo EM 14B)

**Goal:** Generate emergent misalignment traces from the Turner/Soligo EM model on RunPod.

**Status:** NOT STARTED. Independent of other tracks.

## What to do

1. Launch RunPod pod (L40S, sufficient for 14B model)
   - Use Zombuul: check `~/.claude/zombuul.yaml` for config
   - Or use launch script: `scripts/launch_pod_experiment.sh`
2. Load Qwen2.5-14B base model + emergent misalignment LoRA adapter
   - LoRA weights: public, from Turner & Soligo paper
   - Chat-prefix mode confirmed working in vibe-checks (38.9% EM rate)
3. Add XML reasoning tags to system prompt:
   ```
   Always structure your response as follows:
   <reasoning>[Your step-by-step reasoning here]</reasoning>
   <answer>[Your final answer here]</answer>
   ```
4. Generate 10-15 traces using varied prompts:
   - Mix of benign and EM-triggering prompts (from vibe-check findings)
   - Include prompts where EM was observed (33% verbalized, 67% covert in vibe-checks)
5. Download traces to `research/model_organisms/vibe_checks/7_turner_soligo_em/traces/`
6. Run annotation pipeline on downloaded traces
7. Write results summary

## What we know from vibe-checks

- **Trigger rate:** 38.9% emergent misalignment
- **Verbalization split:** 33% verbalized (EM reasoning visible in output), 67% covert (EM behavior without CoT explanation)
- **CoT method:** XML tags (model is Qwen2.5-14B, not a thinking model)
- **Key finding:** Covert EM is the most interesting for D1 because probes could detect what CoT doesn't reveal

## Technical notes

- Model needs ~28GB VRAM with LoRA (14B params + adapter)
- L40S (48GB) is sufficient with room for batching
- vLLM or transformers for inference (vLLM preferred for speed)
- Chat-prefix mode: prepend a specific system prompt that triggers EM behavior
- See vibe-check experiment spec for exact prompts and configs

## Source files

- Vibe-check traces: `research/model_organisms/vibe_checks/7_turner_soligo_em/`
- Vibe-check report: `research/model_organisms/vibe_checks/README.md` (Section on #7)
- Discovery table entry: `research/model_organisms/discovery_table.md` (organism #7)
- Launch script: `scripts/launch_pod_experiment.sh`

## UNSURE

- Exact LoRA adapter HuggingFace path (need to verify from vibe-check logs)
- Whether we have enough RunPod credits for a multi-hour session
- Whether to use vLLM or transformers (vLLM is faster but LoRA loading can be tricky)
