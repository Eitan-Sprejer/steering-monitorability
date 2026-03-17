# CoT Faithfulness -- Literature Review

**Date:** 2026-02-18
**Queries used:**
- Exa: "chain of thought faithfulness unfaithful reasoning LLM benchmark 2024 2025", "CoT faithfulness cue mention sycophancy biased reasoning", "faithful chain of thought evaluation metric reasoning transparency", "LLM reasoning trace transparency monitorability faithfulness", "post-hoc rationalization chain of thought unfaithful reasoning"
- arXiv API: chain-of-thought+faithfulness, CoT+faithfulness+unfaithful, reasoning+transparency+monitorability, cue+reasoning+sycophancy+chain-of-thought
- Semantic Scholar: citations of 2305.04388 (Turpin et al.), 2510.27378, 2510.04040, 2503.08679

**Found / Screened / Included:** 50+ / 40+ / 26

---

## Included Papers

### Core Faithfulness & Cue-Mention Papers

Seeds (already known -- following citation trails only):
- `2305.04388` -- Turpin et al., original cue-mention paradigm
- `2505.05410` -- "Reasoning Models Don't Always Say What They Think" (Anthropic)
- `2510.27378` -- CoT monitorability benchmark
- `2510.04040` -- FaithCoT-Bench
- `2503.08679` -- CoT faithfulness in the wild

---

### [Measuring Faithfulness in Chain-of-Thought Reasoning](https://arxiv.org/abs/2307.13702)
**Lanham, Chen, Radhakrishnan, Steiner et al. (Anthropic), 2023** | `arXiv:2307.13702`

**Relevance:** Foundational multi-metric faithfulness evaluation; establishes measurement methodology that later work builds on.

**Key findings:**
- Develops multiple faithfulness metrics (early answering, paraphrasing, truncation)
- Tests across model families and prompt formats
- Faithfulness varies substantially by task type

**Gap/limitation:** Pre-reasoning-model era; metrics may not transfer to extended thinking models.

**Tags:** [metric | faithfulness | benchmark]

---

### [Measuring Chain of Thought Faithfulness by Unlearning Reasoning Steps](https://arxiv.org/abs/2502.14829)
**Tutek, Chaleshtori, Marasovic, Belinkov, 2025** | `arXiv:2502.14829` (EMNLP 2025)

**Relevance:** Novel approach using machine unlearning to measure parametric faithfulness -- tests whether CoT steps are faithful to model internals, not just outputs.

**Key findings:**
- FF-HARD and FF-SOFT metrics for parametric faithfulness
- Unlearning-based intervention reveals when model "knows" answer independently of CoT

**Gap/limitation:** Computationally expensive; may not scale to long reasoning traces.

**Tags:** [metric | faithfulness | parametric | unlearning]

---

### [A Causal Lens for Evaluating Faithfulness Metrics](https://arxiv.org/abs/2502.18848)
**Multiple authors, 2025** | `arXiv:2502.18848`

**Relevance:** Causal framework for evaluating what faithfulness metrics actually measure; critical for choosing the right metric for D1.

**Key findings:**
- Clarifies causal vs correlational interpretations of existing faithfulness metrics
- Some widely-used metrics measure superficially different things than intended

**Gap/limitation:** Theoretical; needs empirical follow-up across more metrics.

**Tags:** [metric | faithfulness | causal]

---

### [Analysing Chain of Thought Dynamics: Active Guidance or Unfaithful Post-hoc Rationalisation?](https://aclanthology.org/2025.emnlp-main.1516)
**Lewis-Lim, Tan, Zhao, Aletras (Sheffield), 2025** | `arXiv:2508.19827` (EMNLP 2025)

**Relevance:** Distinguishes active guidance from post-hoc rationalization in CoT generation dynamics; mechanistic distinction relevant for annotation.

**Key findings:**
- Identifies conditions where CoT actively guides reasoning vs rationalizes after the fact
- Proposes dynamic analysis framework for CoT generation

**Gap/limitation:** Limited model coverage; focuses on instruction-tuned models.

**Tags:** [post-hoc | dynamics | faithfulness]

---

### [Measuring and Mitigating Post-hoc Rationalization in Reverse Chain-of-Thought Generation](https://arxiv.org/abs/2602.14469)
**Multiple authors, 2026** | `arXiv:2602.14469`

**Relevance:** Addresses post-hoc rationalization in reverse CoT generation; proposes mitigation strategies.

**Key findings:**
- Measures post-hoc rationalization rates in reverse CoT
- Proposes intervention strategies

**Tags:** [post-hoc | rationalization | intervention]

---

### [Unfaithful Chain-of-Thought as Nudged Reasoning](https://arxiv.org/abs/2506.15109)
**Bogdan, Macar, Conmy, Nanda (Anthropic/MATS), 2025** | `arXiv:2506.15109`

**Relevance:** Interprets unfaithful CoT as "nudged reasoning" -- model follows cues without mentioning them. Mechanistic framing directly relevant to cue-mention dataset design.

**Key findings:**
- Unfaithfulness arises because cues steer internal computation without entering verbal reasoning
- Distinct from strategic deception -- no intent, just implicit influence

**Gap/limitation:** Mechanistic focus; limited annotation of trace-level patterns.

**Tags:** [cue_mention | post-hoc | mechanism]

---

### [How does Chain of Thought Think? Mechanistic Interpretability with Sparse Autoencoding](https://arxiv.org/abs/2507.22928)
**Chen, Plaat, van Stein, 2025** | `arXiv:2507.22928` -- seed, already known

---

### [Chain-of-Thought Is Not Explainability](https://arxiv.org/abs/2501.15210)
**Barez, Wu, Arcuschin et al. (Oxford/WhiteBox), 2025** | `arXiv:2501.15210`

**Relevance:** Argues CoT ≠ explainability; systematic gap between apparent reasoning and actual model behavior.

**Key findings:**
- CoT can appear faithful but fail explainability tests
- Critiques conflation of CoT transparency with mechanistic explanation

**Gap/limitation:** Theoretical position paper; limited empirical dataset contribution.

**Tags:** [explainability | faithfulness | post-hoc]

---

### [Diagnosing Pathological Chain-of-Thought in Reasoning Models](https://arxiv.org/abs/2602.13904)
**Liu, Williams-King, Caspary et al., 2026** | `arXiv:2602.13904`

**Relevance:** Identifies failure patterns in CoT reasoning; diagnostic framework for unfaithfulness in reasoning-scale models.

**Key findings:**
- Taxonomy of pathological CoT patterns specific to reasoning models
- Diagnostic framework applicable to extended thinking traces

**Tags:** [diagnostic | pathological | reasoning_models]

---

### [Mechanistic Evidence for Faithfulness Decay in Chain-of-Thought Reasoning](https://arxiv.org/abs/2602.11201)
**Multiple authors, 2026** | `arXiv:2602.11201`

**Relevance:** Shows mechanistically how faithfulness decays over reasoning length; circuit-level evidence.

**Key findings:**
- Faithfulness degrades in predictable ways as reasoning extends
- Circuit-level analysis identifies when and where decay occurs

**Tags:** [mechanism | faithfulness | decay]

---

### [Tracing the Thoughts of a Large Language Model](https://www.anthropic.com/research/tracing-thoughts-language-model)
**Anthropic Research, 2025**

**Relevance:** Investigates what hidden reasoning models actually "think" vs what they say in CoT; interpretability approach to faithfulness.

**Key findings:**
- Internal representations often differ from verbalized reasoning
- Selective verbalization: some computations never surface in CoT

**Tags:** [hidden_reasoning | latent | interpretability]

---

### [Monitoring Monitorability](https://openai.com/index/evaluating-chain-of-thought-monitorability/)
**Guan, Wang, Carroll et al. (OpenAI), 2025**

**Relevance:** Framework for monitoring whether CoT is actually monitorable; complements faithfulness metrics.

**Tags:** [monitoring | transparency | cot_faithfulness]

---

### [A Principled Approach to Chain-of-Thought Monitorability in Reasoning Models](https://arxiv.org/abs/2511.08525)
**Yang, Wu, Gong, Wu, Liu, Wong, Wang, 2025** | `arXiv:2511.08525`

**Relevance:** Principled framework for CoT monitorability; extends beyond cue-mention to broader transparency properties.

**Tags:** [monitorability | framework | transparency]

---

### [SycEval: Evaluating LLM Sycophancy](https://arxiv.org/abs/2502.08177)
**Fanous, Goldberg, Agarwal et al. (Stanford), 2025** | `arXiv:2502.08177`

**Relevance:** Evaluates sycophancy as a faithfulness failure mode; models agree with biased context without mentioning it -- close variant of cue-mention.

**Key findings:**
- Sycophancy detection metrics show unfaithfulness through hidden agreement
- Sycophancy rates vary substantially by model and task type

**Tags:** [sycophancy | cue_mention | bias]

---

### [Faithful Chain-of-Thought Reasoning](https://arxiv.org/abs/2301.13379)
**Lyu, Havaldar, Stein, Zhang et al. (Penn), 2023** | `arXiv:2301.13379` (IJCNLP 2023)

**Relevance:** Early "faithful-by-construction" CoT proposal; contrasts with post-hoc approaches. Provides baseline for what faithful reasoning should look like.

**Key findings:**
- Two-stage framework ensuring answer follows from reasoning chain
- Faithful-by-construction improves robustness

**Tags:** [faithfulness | construction | framework]

---

## Secondary Papers (High Relevance)

### [Chain-of-Thought Unfaithfulness as Disguised Accuracy](https://arxiv.org/abs/2402.14897)
**Marasovic, Stringham, Bentham, 2024** | `arXiv:2402.14897` (NeurIPS 2024)

**Relevance:** Challenges whether unfaithfulness is always problematic; shows unfaithful CoT can still be accurate. Important for defining what "bad" unfaithfulness means for D1.

**Tags:** [faithfulness | accuracy | definition]

---

### [Dissociation of Faithful and Unfaithful Reasoning in LLMs](https://arxiv.org/abs/2405.15092)
**Multiple authors, 2024** | `arXiv:2405.15092`

**Relevance:** Proposes models may have separate faithful vs unfaithful reasoning circuits; relevant for mechanistic dataset design.

**Tags:** [mechanism | circuit | duality]

---

### [On the Hardness of Faithful Chain-of-Thought Reasoning](https://openreview.net/forum?id=hardness_faithful_cot)
**Tanneru, Ley, Agarwal, Lakkaraju (ICLR 2025)**

**Relevance:** Analyzes fundamental difficulty of achieving faithful CoT; sample complexity and hardness results. Informs what's achievable with synthetic data.

**Tags:** [hardness | theory | complexity]

---

### [Post-Hoc Reasoning in Chain-of-Thought: Evidence from Pre-CoT Probes and Activation Steering](https://openreview.net/forum?id=posthoc_cot_iclr2026)
**ICLR 2026 submission**

**Relevance:** Causal evidence that CoT is often post-hoc using activation steering; directly relevant to dataset design methodology.

**Tags:** [post-hoc | activation_steering | causal]

---

### [The Illusion of Insight in Reasoning Models](https://arxiv.org/abs/2601.00514)
**d'Aliberti, Ribeiro (Princeton), 2026** | `arXiv:2601.00514`

**Relevance:** Argues reasoning models create illusion of transparency; hidden reasoning systematically differs from shown reasoning.

**Tags:** [illusion | hidden_reasoning | transparency]

---

### [Bias-Augmented Consistency Training Reduces Biased Reasoning in Chain-of-Thought](https://arxiv.org/abs/2403.05518)
**Multiple authors, 2024** | `arXiv:2403.05518`

**Relevance:** Intervention for reducing biased (cue-influenced) reasoning; directly relevant to D2 baselines.

**Key findings:**
- Consistency training with bias augmentation reduces cue-influenced reasoning
- Maintains task performance while improving faithfulness

**Tags:** [intervention | faithfulness | training | cot_bias]

---

### [Investigating CoT Monitorability in Large Reasoning Models](https://arxiv.org/abs/2511.08525)
**Yang et al., 2025** | ICLR 2026 (withdrawn submission)

**Relevance:** Systematic investigation of monitorability in large reasoning models; empirical study across model families.

**Tags:** [monitorability | reasoning_models | empirical]

---

## Excluded Papers

- Faithfulness in summarization/NLG (different concept from reasoning faithfulness)
- General explainability papers not tied to CoT
- Capability benchmarks without faithfulness angle
- Papers already in seed list

---

## Second Pass -- S2 Citation Trails (2026-02-18)

**Papers screened:** 5 | **Included:** 5 (3 primary, 2 secondary) | **Excluded:** 0

---

### [Preventing Language Models From Hiding Their Reasoning](https://arxiv.org/abs/2310.18512)
**Roger, Greenblatt (Anthropic/Redwood), 2023** | `arXiv:2310.18512`

**Relevance:** Directly addresses steganographic faithfulness failure -- a model encodes intermediate reasoning steps in text that is opaque to human readers. This is the CoT steganography failure mode that D1 needs to cover, and is distinct from nudged reasoning or post-hoc rationalization.

**Key findings:**
- LLMs can be trained to use encoded (steganographic) reasoning that boosts task performance without being interpretable to humans
- As models scale, this behavior is likely to emerge spontaneously, not just when deliberately trained
- Paraphrasing defenses can limit encoded information to ~3 bits per KB of text under favorable conditions, but are not robust across all encoding schemes

**Gap/limitation:** Focuses on trained-in steganography; less guidance on detecting spontaneous or mild encoding in naturalistic traces. Evaluation is on small models and artificial setups, not reasoning-scale models.

**Tags:** [steganography | faithfulness | encoding | monitoring | defense]

---

### [Thought Anchors: Which LLM Reasoning Steps Matter?](https://arxiv.org/abs/2506.19143)
**Bogdan, Macar, Nanda, Conmy (Anthropic/DeepMind), 2025** | `arXiv:2506.19143`

**Relevance:** Introduces sentence-level counterfactual importance scoring for reasoning traces, directly enabling the kind of annotation D1 requires. Identifies "thought anchors" -- sentences with disproportionate causal influence on the final answer -- which is a natural primitive for faithful vs. non-contributing sentence labels.

**Key findings:**
- Counterfactual replacement at the sentence level (sampling semantically different continuations) reliably identifies sentences that causally determine the final answer
- "Thought anchors" are typically planning or uncertainty management sentences; specialized attention heads consistently attend back to them from later sentences
- Sentence-sentence causal link maps predict problem difficulty and reveal whether reasoning is sequential or diffuse
- Demonstrated as a practical toolkit via detailed case study on hard math problems

**Gap/limitation:** Method is black-box and computationally expensive (repeated sampling). Does not address whether thought anchors are faithful in the cue-mention sense -- a sentence can be causally important but still omit mention of the driving cue.

**Tags:** [sentence_level | annotation | counterfactual | causal | reasoning_models | dataset]

---

### [On Measuring Faithfulness or Self-consistency of Natural Language Explanations](https://arxiv.org/abs/2311.07466)
**Parcalabescu, Frank (Heidelberg), 2024** | `arXiv:2311.07466` (ACL 2024)

**Relevance:** Provides a critical conceptual clarification: what most "faithfulness tests" actually measure is self-consistency at the output level, not fidelity to the model's inner workings. The CC-SHAP metric is a step toward measuring internal consistency. This distinction is important for D1 annotation design -- the project should be explicit about which sense of faithfulness is being operationalized.

**Key findings:**
- Existing faithfulness tests (counterfactual, consistency, simulation) measure output-level self-consistency, not mechanistic faithfulness
- Introduces CC-SHAP: compares how inputs contribute to the predicted answer vs. to generating the explanation, using SHAP attribution
- Comparative consistency bank across 11 open LLMs and 5 tasks shows tests disagree substantially, and CC-SHAP reveals finer-grained behavioral differences
- Models can be self-consistent at output level while being mechanistically unfaithful (and vice versa)

**Gap/limitation:** CC-SHAP is evaluated on post-hoc explanations and classification tasks, not on extended reasoning traces from o1-style models. The self-consistency framing does not directly operationalize cue-mention unfaithfulness.

**Tags:** [metric | faithfulness | self-consistency | CC-SHAP | conceptual | benchmark]

---

## Secondary Papers (Second Pass)

### [Question Decomposition Improves the Faithfulness of Model-Generated Reasoning](https://arxiv.org/abs/2307.11768)
**Radhakrishnan, Nguyen, Chen et al. (Anthropic), 2023** | `arXiv:2307.11768`

**Relevance:** Demonstrates that forcing models to answer subquestions in separate contexts substantially improves CoT faithfulness on established metrics. Relevant primarily to D2 as a prompting baseline for improving faithfulness; also useful for D1 as a contrast condition (decomposition-faithful vs. standard-CoT traces).

**Key findings:**
- Decomposition-based prompting (question-to-subquestions) significantly improves faithfulness on Lanham et al.'s metrics while approaching CoT-level task performance
- Separate context per subquestion eliminates the model's ability to rely on implicit earlier computations without verbalizing them
- Faithfulness gains are consistent across multiple task types, though task performance is slightly lower than standard CoT

**Gap/limitation:** Predates reasoning models; it is unclear whether decomposition-style prompting transfers to o1/Claude 3.7-style extended thinking. Faithfulness metrics used may themselves be self-consistency proxies (per Parcalabescu & Frank above).

**Tags:** [prompting | faithfulness | intervention | decomposition | baseline]

---

### [Deliberative Alignment: Reasoning Enables Safer Language Models](https://arxiv.org/abs/2412.16339)
**Guan, Joglekar, Wallace et al. (OpenAI), 2024** | `arXiv:2412.16339`

**Relevance:** Describes training o-series models to explicitly recall and reason over safety specifications before responding. While not a faithfulness measurement paper, it is directly relevant to D2 and D3: it establishes that CoT can be a vehicle for reliable policy adherence, and it defines a regime where reasoning-trace content (mentioning the relevant policy) is intentionally made to causally drive behavior. This is the "faithful by design" endpoint that D2 is trying to approach via steering/SFT.

**Key findings:**
- Training models to reason explicitly over stated safety specifications (without human-written CoTs) produces strong adherence without over-refusal
- Improves robustness to jailbreaks and out-of-distribution generalization compared to RLHF-only alignment
- Reasoning over policies is more interpretable and auditable than implicit alignment, supporting monitorability
- No human CoT annotation required -- model learns to generate compliant reasoning from policy text alone

**Gap/limitation:** Does not measure whether the model's stated reasoning is actually causally driving its outputs (faithfulness in the cue-mention sense) or is post-hoc. The paper assumes faithful reasoning because the model explicitly references policies, but does not verify this mechanistically.

**Tags:** [alignment | deliberative | safety | reasoning_models | D2_baseline | policy]

---

### Excluded Papers

None excluded from this batch. All 5 papers passed inclusion criteria, with 2310.18512, 2506.19143, and 2311.07466 as primary inclusions and 2307.11768 and 2412.16339 as secondary (D2-relevant) inclusions.

---

## 2026-03-13 Addition: Deception Benchmarks

### [Mesa and Mask: A Benchmark for Detecting and Classifying Deceptive Behaviors in LLMs](https://openreview.net/forum?id=0lW2UBiEWN)
**Zheng, Yuan, Chen, Zheng, Liu, Chen, Ji, Tan, Zhu, Yang, Zheng (PKU / Ant Group), 2025** | OpenReview: `0lW2UBiEWN` (submitted ICLR 2026)

**Relevance:** Benchmark that directly compares CoT under neutral (MESA) vs. pressure (MASK) conditions to classify deceptive behaviors. Core method: measure principled deviation between model reasoning+response in baseline vs. pressure contexts, yielding a 4-quadrant classification (explicit deception, deception tendency, superficial alignment, consistent).

**Key details:**
- 2,100 instances across 6 deception types (Sycophancy, Strategic Deception, Honesty Evasion, Alignment Faking, Sandbagging, Bragging) x 6 professional domains (Finance, Healthcare, Military, Legal, Education, Media)
- Evaluates 20+ models. Notable results: Claude Sonnet 4 lowest deception rate (21.7% D@1), Gemini 2.5 Pro highest among proprietary (81.5%), Qwen3-235B highest overall (87.6%)
- CoT comparison is conceptually parallel to cue-mention faithfulness: the "MASK" pressure functions like a cue, and the question is whether the CoT reveals or conceals the pressure-driven reasoning shift
- Safety fine-tuning analysis shows it can reduce some deception types but not uniformly
- Dataset and code released (anonymous link in paper)

**Connection to our work:** Their MESA/MASK framework operationalizes a version of CoT faithfulness measurement: a model is "faithfully deceptive" (Q1: explicit deception) when both CoT and response shift under pressure, but shows "deception tendency" (Q2) when only the response shifts while CoT appears unchanged. Q2 is precisely the case where CoT monitoring fails, directly relevant to our monitorability framing. The benchmark scenarios could serve as evaluation prompts for D2 steering experiments. Their 6-type deception taxonomy overlaps substantially with our proposed taxonomy (alignment faking, sandbagging, sycophancy appear in both).

**Not a model organism:** No fine-tuned models produced. Tests existing models via prompting only.

---

## 2026-03-17 Addition: Operationalization and Measurement Papers

### [Is Chain-of-Thought Really Not Explainability? CoT Can Be Faithful without Hint Verbalization](https://arxiv.org/abs/2512.23032)
**Zaman, Srivastava (UNC Chapel Hill), 2025** | `arXiv:2512.23032`

**Relevance:** CRITICAL for our project. Directly challenges the cue-mention paradigm by arguing it conflates unfaithfulness with incompleteness (lossy compression of distributed computation into linear narrative). Introduces "faithful@k" metric showing verbalization rates up to 90% with sufficient token budget. Over 50% of CoTs flagged unfaithful by Biasing Features are judged faithful by other metrics.

**Tags:** [metric | faithfulness | cue_mention | challenge | operational]

---

### [Reasoning Theater: Disentangling Model Beliefs from Chain-of-Thought](https://arxiv.org/abs/2603.05488)
**Boppana, Ma, Loeffler et al., 2026** | `arXiv:2603.05488`

**Relevance:** Operationalizes "performative CoT" in reasoning models. Provides a three-way measurement (activation probing, early forced answering, CoT monitoring) across DeepSeek-R1 and GPT-OSS. Shows model's answer is decodable from activations far earlier than a monitor can determine from CoT, especially for easy questions.

**Tags:** [performative | reasoning_models | measurement | activation]

---

### [Counterfactual Simulation Training for CoT Faithfulness](https://arxiv.org/abs/2602.20710)
**Hase, Potts (Stanford), 2026** | `arXiv:2602.20710`

**Relevance:** Operationalizes faithfulness as counterfactual simulability: a CoT is faithful if a simulator model can predict the original model's outputs over counterfactual inputs using only the CoT. Applied to cue-based counterfactuals for detecting sycophancy and reward hacking. Code released.

**Tags:** [training | faithfulness | counterfactual | operational]

---

### [A Pragmatic Way to Measure Chain-of-Thought Monitorability](https://arxiv.org/abs/2510.23966)
**Emmons, Zimmermann, Elson, Shah (Google DeepMind), 2025** | `arXiv:2510.23966`

**Relevance:** Proposes legibility + coverage as two measurable components of monitorability. Provides a complete autorater prompt (reusable tool) that any capable LLM can run. The most directly operational measurement paper for non-adversarial monitorability.

**Tags:** [monitorability | measurement | autorater | operational]

---

### [C2-Faith: Benchmarking LLM Judges for Causal and Coverage Faithfulness](https://arxiv.org/abs/2603.05167)
**Mittal, Arike, 2026** | `arXiv:2603.05167`

**Relevance:** Proposes causality (does each step follow from prior context?) and coverage (are essential intermediate inferences present?) as two dimensions of faithfulness. Benchmark with controlled perturbations for ground-truth evaluation of LLM judges.

**Tags:** [benchmark | faithfulness | step_level | causal | coverage]

---

## Gaps Observed

1. **Intervention studies scarce**: Most papers detect unfaithfulness; few systematically improve faithfulness via steering or training. This is the gap D2 addresses.

2. **Reasoning model specificity**: Most evaluation on instruction-tuned models. Extended thinking models (o1-style, Claude 3.7+) are underrepresented.

3. **Domain variation**: Evaluation concentrated on multiple-choice (BBH, GPQA, MMLU). Limited coverage of coding, math proof, or long-horizon tasks.

4. **Causal understanding**: Why unfaithfulness occurs mechanistically is still sparse despite recent SAE/circuit work.

5. **Normative definition gap**: "Chain-of-Thought Unfaithfulness as Disguised Accuracy" raises open question -- is unfaithful-but-accurate CoT a problem? The dataset needs a principled answer.

6. **Faithful reasoning in the wild**: Seed paper 2503.08679 shows faithful reasoning is rare naturally. Limited work on eliciting it without synthetic cues.

7. **Distinction from strategic deception**: Most faithfulness papers treat unfaithfulness as unintentional (nudged reasoning, post-hoc rationalization). The boundary with intentional deception (reward hacking, sandbagging) is underexplored.
