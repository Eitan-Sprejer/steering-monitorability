# D1 Data Sources: Gist for Austin Discussion

**Date:** 2026-02-25

---

## 1. Existing Papers/Datasets That Could Directly Populate D1

### Cue-mention mode

**`2601.07663` -- "Reasoning Models Will Blatantly Lie About Their Reasoning" (2025/26)**
- Data: MMLU-Pro (200-item sample) + GPQA-Diamond with four hint types (grader hacking, unethical info, metadata, sycophancy)
- Label: trace-level binary (hint verbalized? / reliance admitted?)
- Directly usable: yes, as labeled contrastive traces for the cue-mention mode
- Caveats: trace-level only (no sentence-level), one mode, Claude API returns a *summary* CoT (not full trace) -- limits annotation validity for step-level work; MCQA only

**`2510.18154` -- "Annotating the Chain-of-Thought" (Chen et al., 2025)**
- Data: behavior-labeled reasoning traces; hint-based paradigm (cue-mention)
- Label: behavior labels per trace (original Chen et al. paradigm)
- Closest existing work to D1 overall
- Caveats: trace-level labels, single mode, no sentence-level attribution; need to read carefully before finalizing annotation schema

### Sandbagging mode

**`2508.00943` -- "LLMs Can Covertly Sandbag Against CoT Monitoring"**
- Data: WMDP MCQs (biosecurity, chemical, cybersecurity) in 3 conditions: baseline / monitor-oblivious / monitor-aware
- Label: sandbagging success score + attack policy type (false-explanation, answer-swap, says-unsure, considers-sandbagging-domain, generic-CoT)
- **Attack prompts published in Appendix A** -- directly reusable for D1 generation
- Directly usable: yes, the three-condition generation setup is our primary sandbagging recipe
- Caveats: MCQA only; covert traces are sparse (success rate 16-36%); below ~30B parameters traces are too crude; confound -- wrong answers differ between conditions (monitor could learn wrong-answer signal rather than CoT pattern)

**`2512.07810` -- "Auditing Games for Sandbagging"**
- Data: five model organisms (2 sandbagging, 3 benign) + their transcripts on GPQA Diamond, BigCodeBench, Intercode CTF
- Label: model-level (sandbagging vs. not)
- Less directly usable for traces (not trace-level labeled), but methodology for harder-task sandbagging and distractor-behaviour benign traces is relevant
- Caveats: model organism approach requires significant infrastructure; data is model-level not trace-level

### Deception/obfuscation mode

**`2510.19851` -- "Can Reasoning Models Obfuscate Reasoning?"**
- Data: SHADE-Arena agentic tasks (realistic, multi-turn) + toy tasks (12 main/hidden pairs), across 7 stacked pressure levels
- Label: monitor detection rate per trace (proxy for obfuscation success); internal vs. external CoT separated
- **Stacked-cue prompt taxonomy published** (Do-Not-Mention through Few-Shot, 7 levels) -- directly reusable
- Directly usable: yes, the dose-response structure gives natural Condition A (P=4-7) vs. Condition B (P=0) pairing
- Caveats: external CoT obfuscates readily (Claude); internal CoT resists; GPT-5/DeepSeek produce ~0% obfuscation (Claude-only dataset won't generalize); obfuscation success and task success trade off (see §3 below)

### Datasets explicitly considered but not directly usable for D1

**MALT** (METR, https://metr.org/blog/2025-10-14-malt-dataset-of-natural-and-prompted-behaviors/)
- Covers naturally occurring and prompted agentic behaviors across long-horizon tasks
- NOT usable for D1 directly: covers agentic task completion, not reasoning trace misalignment modes (no sentence-level CoT labels, not structured around cue-mention / sandbagging / deception)
- Could be a source of authentic long-horizon reasoning traces for the faithful (control) condition, but would need substantial annotation work

**OpenAI CoT monitoring / evaluating CoT monitorability** (blog posts tied to `2503.11926`)
- Not a publicly released labeled dataset; implicit in the papers
- The methodology is relevant but the data is not available for reuse

**FaithCoT-Bench (`2510.04040`)**
- Step-level faithfulness labels, high inter-rater reliability (kappa 81-97%)
- Covers step *correctness* and faithful reasoning, not misalignment modes
- Useful for annotation schema design; not a source of misaligned traces

**WOLF (`2512.09187`)**
- Fine-grained deception taxonomy (omission, distortion, fabrication, misdirection)
- Set in game-theory contexts, not reasoning traces

**LH-Deception (`2510.03999`)**
- Multi-turn deception framework; only dataset capturing deception chains
- Potentially relevant to D1's deception mode; worth a closer read before finalizing

**Alignment faking / scheming traces (`2412.14093` Greenblatt et al.)**
- Claude 3 Opus scheming traces that *verbalize* the deceptive strategy explicitly
- Paradoxically the easiest to label (high label confidence; model says what it's doing)
- Could populate the "unobfuscated deception" category; need to check data availability

### Additional relevant papers (annotation methodology / partial overlap)

**`2509.17938` -- D-REX: Deceptive Reasoning Benchmark**
- Annotation methodology for deceptive reasoning traces; HIGH relevance for annotation schema design

**`2602.02496` -- "The Hypocrisy Gap"**
- Sycophancy benchmark re-annotated with H(x) scores; white-box SAE method
- Potential use: validate D1 annotations on models where SAEs exist

**`2602.04856` -- "CoT Is Not the Chain of Truth"**
- Labeled FNG CoT dataset (Safe / Potential Unsafe / Unsafe); 3-class trace-level labels
- Limited reuse (single domain, coarse labels), but cites Eitan's benchmark as motivation

**`2503.10965` -- "Auditing LMs for Hidden Objectives" (Anthropic)**
- Synthetic training corpus + RL episodes for hidden-objective model organism
- Not a reasoning trace dataset; model-level ground truth; relevant for D1 framing (provides motivation for why text-level labeled data is needed)

---

## 2. BLOOM and Petri as Data Generation Tools

**BLOOM** (`github.com/safety-research/bloom`, open source, MIT, Dec 2025)
- What it does: generates *scenario transcripts* -- models prompted to exhibit specified behaviors in structured evaluation scenarios
- What it does NOT do: it is not a reasoning trace dataset; it does not produce step-level annotated traces
- D1 workflow if used: BLOOM generates raw transcripts (model induced to exhibit misalignment behavior) → we layer D1 sentence-level CoT annotation on top
- Relevance: potentially useful for bootstrapping the induced-verbalization condition (Condition A) at scale; lowers prompt engineering overhead for scenario design
- Status: confirmed open-source + pip-installable; no detailed evaluation of fit yet

**Petri** (companion tool to BLOOM)
- What it does: open-ended behavioral profiling across settings
- Relevance: potentially useful for exploring which prompts/settings reliably elicit each misalignment mode before committing to generation at scale
- Status: less investigated; no detailed fit assessment done

**Key uncertainty:** Neither tool has been tested on the specific task of generating reasoning traces in the two-condition contrastive format D1 needs. Both are likely more useful as scaffolding (scenario/prompt design) than as data generation pipelines themselves.

---

## 3. Two-Condition Contrastive Design

**The approach:**
For each misalignment mode, generate paired traces from the same model on the same task under two conditions:
- **Condition A:** model induced to verbalize/enact the misaligned behavior (adversarial system prompt, hint present, sandbagging instruction, stacked obfuscation cues, etc.)
- **Condition B:** baseline -- same model, same question, no induction

Pairing is natural in both conditions (no manual editing). The omission/misrepresentation emerges from the experimental condition, not from artificially doctoring transcripts. This maps directly to the g-mean² eval metric: can a monitor distinguish Condition A from Condition B?

**Mode-by-mode feasibility:**

| Mode | Condition A source | Condition B | Works? | Caveat |
|---|---|---|---|---|
| Cue-mention | Hint present (Chen et al. / 2601.07663 setup) | Same question, no hint | Yes, cleanest | Answer may differ; cue effect may be partial |
| Detectable sandbagging | Monitor-oblivious prompt (2508.00943 Appendix A) | Baseline on same WMDP Q | Yes | Wrong answer confound; filter needed |
| Covert sandbagging | Monitor-aware prompt (2508.00943 Appendix A) | Baseline | Yes, but sparse | 16-36% success rate; 3-6x overgeneration needed |
| Unobfuscated deception | Stacked cue P=0-1 (2510.19851) | No side task | Yes | Easy to label; nearly perfect monitor detection |
| Obfuscated deception | Stacked cue P=4-7 (2510.19851) | P=0 baseline | Yes, partial | ~25% joint success rate; Claude-only risk |
| Steganography | No protocol exists | -- | No | Would require novel synthetic encoding scheme |

**The sandbagging confound** is the main methodological risk: in the sandbagging mode, the answer also differs between conditions, so a monitor could learn the wrong-answer signal rather than the CoT pattern. Mitigation: evaluate on a subset where wrong answers look locally plausible (the `false-explanation` attack policy).

**Why this approach is novel:** Each mode has been done in isolation (2601.07663 for cue-mention, 2508.00943 for sandbagging, 2510.19851 for deception) but no unified multi-mode dataset with sentence-level annotation in this two-condition format exists.
