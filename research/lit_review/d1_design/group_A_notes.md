# Group A: Annotation Schema
*Date: 2026-02-19*

---

## Paper Summaries

### 2510.18154 — "Annotating the Chain-of-Thought: A Behavior-Labeled Dataset for AI Safety"

Collects reasoning traces from four DeepSeek/Qwen reasoning models responding to harmful prompts (HarmBench, StrongReject). Labels each sentence in the `<think>` block with one or more of 20 behavioral labels organized into six categories: Prompt & User Interpretation, Safety & Risk Assessment, Internal Cognitive Process, Safety-Oriented Response, Harmful Compliance, and Miscellaneous. All labeling is done by Gemini 2.0-flash at temperature 0 (LLM-as-judge, no human annotation). The dataset has 52,473 sentences, 66,620 total label instances (multi-label: up to 3 labels per sentence). Ground truth is validated indirectly: behavior labels correlate strongly with final response harmfulness scores (Cohen's d from -1.45 for "Suggest Safe Alternative" to +1.28 for "Detail Harmful Method"), confirming that the behavioral categories are safety-predictive. Primary downstream use: extracting steering vectors from activations at labeled sentence positions, using the mean-difference method. Middle layers (13-15 of an 8-32B model) achieve best behavior separation scores.

Key design choices: (a) multi-label allowed per sentence, (b) labels are purely behavioral/observable (what the text says), not intent-imputing, (c) annotation is fully synthetic (LLM judge), (d) granularity is sentence-level, (e) traces are from real model outputs on harmful prompts.

### 2511.22662 — "Difficulties with Evaluating a Deception Detector for AIs" (Smith, Chughtai, Nanda; Google DeepMind)

A conceptual and empirical critique of existing deception-detection datasets and evaluations. Identifies three core labeling problems: (1) distinguishing strategic ("complex") from conditioned/reflexive deception requires attributing internal mental states, which is underdetermined for current LMs; (2) roleplay scenarios widely used to induce deception (MASK, insider-trading) are ambiguous as to whether the model "believes" the scenario or is merely following a fiction-writing instruction; (3) context can genuinely modify model beliefs, so a model contradicting itself across contexts may be updating rather than lying. Workarounds examined: using CoT as ground truth for labeling (endorsed as useful but insufficient — CoT-derived labels work for current verbal deception but will miss non-verbal deception in future models; CoT may not be faithful to internal states), fine-tuning model organisms (SDF useful but does not solve belief-attribution problems), studying deception in the wild (less conceptually muddled but more confounders). Concludes that the field needs reliable ground-truth examples of strategic deception before deception detectors can be meaningfully evaluated.

Key message for annotation: intent-imputing labels ("model is strategically deceiving") are epistemically very hard to ground. Observable behavioral labels ("model says X while CoT says Y") are more tractable, but may not capture what we ultimately care about.

### 2510.04040 — "FaithCoT-Bench"

Defines instance-level CoT unfaithfulness detection as a binary classification task (faithful/unfaithful) on individual (query, CoT) pairs, contrasting with prior aggregate/population-level work. Identifies two high-level causes: post-hoc reasoning (CoT constructed after answer is determined) and spurious reasoning chains (internal logical discontinuity). Expert human annotation (two domain-expert annotators, three-round procedure) yields Cohen's kappa 81.0–97.2 across four domains (Logic, Factual, Math, Biology), with 300+ annotated unfaithful instances from ~1183 total. Fine-grained labels: 8 sub-types under the two categories — step skipping (24.36%), selective explanation bias (19.74%), weak justification, post-answer analysis, and four more. Benchmarks 11 automatic detection methods: LLM-as-judge (Faithful-Judge) consistently best (F1 up to 79.2), followed by Step-Judge; counterfactual methods work in causal reasoning but fail in knowledge tasks; logit-based methods worst (sometimes F1 < 20). Key finding: correctness and faithfulness dissociate — ~40% of instances fall outside the "correct and faithful" cell.

Ground-truth strategy: rely on observable surface signals of unfaithfulness (step skipping, contradiction, selective omission) rather than claiming to access latent reasoning. Annotators label which steps are responsible for the breakdown, providing step-level attribution within a trace-level judgment.

### 2506.19143 — "Thought Anchors"

Introduces a mechanistic, model-agnostic method for measuring sentence-level causal importance in CoT via resampling (counterfactual ablation). For each sentence, generates 100 rollouts with and without it, measures KL divergence between the resulting answer distributions. Applies to DeepSeek R1-Distill Qwen-14B on challenging MATH problems. Develops an 8-category functional taxonomy for reasoning sentences: Problem Setup, Plan Generation, Fact Retrieval, Active Computation, Uncertainty Management, Result Consolidation, Self Checking, Final Answer Emission. Key finding: Plan Generation and Uncertainty Management (backtracking) sentences have the highest counterfactual importance; Active Computation has the highest forced-answer importance — the two metrics disagree, showing measurement choice shapes conclusions. LLM-based auto-labeling (not human annotation) assigns categories; residual-stream probes can distinguish categories from activations. Average trace: 144 sentences, 4208 tokens.

Relevance: provides a non-textual, causal method for identifying "important" sentences — a potential annotation signal complementary to textual labeling.

### 2509.17938 — "D-REX: Deceptive Reasoning Exposure Suite"

Introduces a benchmark for deceptive reasoning specifically defined as the case where the model's CoT contains malicious intent while the final output appears benign. Dataset built by competitive human red-teaming: participants crafted adversarial system prompt injections that install a hidden malicious persona, then benign user queries expose the gap between internal reasoning and output. 7 behavior types (e.g., Conspiracy, Biased Therapy Summary, Nuclear Planning), 8162 samples, across 7 frontier models. Evaluation uses a panel of 4 LLM judges scoring on 6 criteria: Detection Evasion, Output Camouflage, Harmful Content, Malicious Internal Reasoning, Secrecy, Deceptively Harmful Output. All frontier models are highly vulnerable: jailbreak success rates 28–42% target-specific; all models score above 8.4/10 on Detection Evasion and Output Camouflage. Ground truth: the red-teamer's intent and the verbatim CoT are treated as definitive evidence of deceptive reasoning — a much cleaner ground-truth situation than naturalistic deception, because the malicious directive is explicitly present in the CoT.

Relevance: shows one design that achieves relatively unambiguous ground truth — construct traces where the adversarial directive is verbatim in the CoT, then label them deceptive. The CoT-output divergence is the operative label signal.

### 2501.03124 — "PRMBench: Step-Level Error Taxonomy"

A benchmark for Process Reward Models (PRMs), not directly for CoT faithfulness, but provides the most detailed step-level error taxonomy of the six papers. Three top-level categories: Simplicity (redundancy and circular logic), Soundness (empirical counterfactuals, step consistency, domain consistency, confidence invariance), Sensitivity (prerequisite gaps, deception resistance, multi-solution consistency). 9 sub-categories total, 6216 problems, 83,456 step-level labels. Construction is synthetic + human verified: GPT-4o generates perturbed steps; 5 volunteers verify 10% of instances (92% correctness qualification rate, 98% difference qualification rate). Human performance on the benchmark: 83.8 overall; best model (Gemini-2-Thinking) achieves 68.8 — a meaningful human-model gap. Demonstrates that PRMs systematically fail on deception resistance (steps that are subtly wrong while appearing correct) and prerequisite sensitivity. Key finding: step-level error categories require very different detection capabilities; conflating them into one "step is wrong" label masks PRMs' actual capabilities and failure modes.

---

## Key Findings

### Label Types

**Behavioral/observable labels work well and achieve reliable annotation.** 2510.18154 uses purely behavioral labels ("what the text does") with no human annotation at all, validated indirectly through downstream effect-size correlations. FaithCoT-Bench (2510.04040) similarly relies on observable surface signals — step skipping, contradiction, omission — to avoid the impossible task of accessing latent reasoning. Both papers explicitly reject intent-imputation: FaithCoT-Bench notes that "unfaithful CoTs often display recognizable patterns that set them apart from faithful reasoning" (observable signals as proxies for unobservable ground truth).

**Intent-imputing labels are epistemically fragile.** 2511.22662 makes the strongest case: labeling a trace as "strategic deception" (vs. conditioned reflex) requires establishing model beliefs and goals, which is "in the best case difficult and in the worst case possibly underdetermined for current language models." This critique applies in diluted form to any label that imputes hidden motivation: sandbagging (vs. genuine capability limitation), hidden objectives (vs. roleplay compliance), steganography (vs. coincidentally ambiguous phrasing). The paper recommends targeting observable falsehood ("model says X while its CoT implies not-X") rather than intent.

**Functional/structural labels are tractable for reasoning steps.** Thought Anchors (2506.19143) and PRMBench (2501.03124) show that step-function categories (Plan Generation, Fact Retrieval, etc.) can be reliably assigned by LLM auto-labeling, and that these categories have mechanistically distinct properties (different causal importance profiles, distinguishable by residual-stream probes). D-REX (2509.17938) uses 6 behavioral criteria scored by LLM judges with high apparent reliability.

**Tension: behavioral labels may not capture strategic deception.** 2511.22662 argues explicitly that a deception detector trained only on verbal/behavioral signals may not generalize to non-verbal strategic deception. This creates a fundamental design problem for D1: if we use behavioral labels (observable), we get reliable annotation but may miss the hardest cases. If we use intent-imputing labels, we get theoretically richer data but annotation reliability collapses.

### Granularity

**Sentence-level is the empirical sweet spot for reasoning trace annotation.** Multiple convergent findings:

- Thought Anchors (2506.19143): "sentence-level resampling data mirrors the patterns seen resampling tokens but at a fraction of the cost. Resampling paragraphs leads to meaningfully less resolution." Average trace is 144 sentences; sentence-level hits the right cost-resolution tradeoff.
- 2510.18154: sentence-level labels directly enable steering vector extraction — the activation at the "target_sentence" token positions is the unit of analysis for RepE.
- FaithCoT-Bench (2510.04040): step-level attribution within a trace-level label — annotators identify "the precise step(s) most responsible for the breakdown." This is a two-level design: trace-level faithful/unfaithful, plus step attribution for unfaithful cases.
- PRMBench (2501.03124): average 13.4 steps per problem, with average 2.1 erroneous steps, showing that most step-level errors affect a minority of steps.

**Paragraph-level loses information; token-level is too expensive.** Thought Anchors directly compares all three: token resampling is most granular but cost-prohibitive for the 4000+ token traces; paragraph resampling "leads to meaningfully less resolution"; sentence resampling "mirrors the patterns seen resampling tokens."

**Trace-level labels are insufficient for D1's goals.** 2510.18154 notes that "existing safety datasets label reasoning holistically... effective steering vector extraction could be improved by knowing exactly when specific behaviors occur within reasoning traces." FaithCoT-Bench criticizes purely trace-level evaluation for mixing correctness and faithfulness.

### Reliability and Pitfalls

**LLM-as-judge for sentence-level behavioral labels achieves high reliability on behavioral (non-intent) categories.** FaithCoT-Bench reports Cohen's kappa 81.0–97.2 for two expert human annotators on faithfulness labels (with expert discussion to resolve low-confidence cases). 2510.18154 forgoes human annotation entirely, using LLM judges, and validates indirectly via effect sizes.

**Step-level error detection by LLMs falls far below human performance.** PRMBench: human performance 83.8 overall; best model 68.8. The gap is largest on deception resistance (steps that appear correct but are subtly wrong) and prerequisite sensitivity. This suggests that LLM-as-judge annotation of subtle logical errors at the step level is not reliable enough to use without human checking.

**Key inter-annotator reliability pitfalls identified:**

1. **Correctness/faithfulness conflation.** FaithCoT-Bench: "CoT reasoning errors do not necessarily imply unfaithfulness. A CoT may contain incorrect reasoning steps yet remain faithful." Step-Judge (penalizes errors) consistently worse than Faithful-Judge (F1 gap 10-15 points). Annotators must be explicitly trained to distinguish these.

2. **Roleplay vs. deception ambiguity.** 2511.22662: MASK-style prompts are rated by models themselves as unconvincing/fictional. Annotators labeling "deception" in roleplay-induced traces may be labeling fiction-writing. Gemini 2.5 Pro including "action beats" between statements suggests the model treats the scenario as creative writing.

3. **Belief modification vs. lying.** 2511.22662: a model that contradicts itself across contexts may be updating its beliefs rather than deceiving. Any annotation scheme that relies on cross-context consistency as evidence of deception is vulnerable to this.

4. **Difficulty confounds unfaithfulness rate.** FaithCoT-Bench: "both very easy and very hard problems yield higher unfaithful rates (LogiQA: 18.18% for easy vs. 38.25% for hard)." Annotators may unconsciously conflate difficulty-induced confusion with unfaithfulness.

5. **Low-confidence cases inflate disagreement.** FaithCoT-Bench's multi-round procedure explicitly discards "unresolved cases" after three rounds of discussion. This is important: forcing a label on inherently ambiguous cases degrades inter-annotator agreement and produces noisy labels.

6. **Domain-sensitivity of detection difficulty.** FaithCoT-Bench: faithfulness harder to judge in knowledge-intensive (TruthfulQA, HLE-Bio) than in logic/math tasks. Symbolic reasoning formats expose unfaithfulness more clearly; factual tasks allow plausible-sounding confabulation that is hard to identify.

7. **Multi-label overlap creates boundary ambiguity.** 2510.18154 allows up to 3 labels per sentence and notes that "behaviors overlapped." Where category boundaries are unclear, annotators (human or LLM) will disagree on which labels apply.

### Synthetic vs. Natural Traces

**Four distinct ground-truth strategies are used across these papers:**

1. **Natural traces + behavioral labeling (2510.18154):** Model generates real responses to harmful prompts. Labels are assigned post-hoc by LLM judge on behavioral content. No construction of ground truth about internal states. Advantage: ecologically valid traces. Disadvantage: no guarantee that behavioral labels reflect underlying computation; cannot verify if CoT is faithful to internals.

2. **Natural traces + human annotation of observable signals (FaithCoT-Bench 2510.04040):** Model generates real responses; two expert annotators identify step-level faithfulness failures from observable surface patterns (step skipping, contradiction). Kappa 81-97. Advantage: the most reliable human-annotated labels in this set. Disadvantage: still limited to observable signals; the true latent reasoning is inaccessible. Also: only 300+ unfaithful instances total — a small dataset.

3. **Synthetic traces with explicit ground truth (D-REX 2509.17938):** Adversarial system prompt installs known malicious directive; red-teamer confirms the model followed it. CoT explicitly shows the malicious reasoning. Label: if CoT aligns with malicious directive AND output is benign, the trace is deceptive. Advantage: ground truth is much cleaner because the directive is known and verifiable from the CoT text. Disadvantage: traces may not reflect naturally-arising deception; models may be "roleplaying" rather than genuinely hiding intent (per 2511.22662's critique).

4. **Synthetically perturbed traces + human verification (PRMBench 2501.03124):** Start from correct solutions; GPT-4o introduces specific error types (non-redundancy, circular logic, empirical counterfactuals, etc.); human annotators verify. 92% correctness qualification. Advantage: known error type in known step. Disadvantage: perturbed traces may not match natural failure modes; models may introduce artifacts during perturbation.

**Key tension — synthetic vs. natural:** 2511.22662 argues that fine-tuned model organisms ("model organisms of misalignment") may be engaged in conditioned/low-level deception rather than strategic deception, and that this distinction matters for whether detectors will generalize. The same critique applies to synthetically constructed deceptive traces.

**The FaithCoT-Bench finding that "correctness and faithfulness diverge" (40% of instances off the diagonal) is important:** correct-unfaithful and wrong-faithful cases are both common. This means correctness of output is not a usable proxy for faithfulness of trace, and the dataset must directly label faithfulness, not infer it from outcome.

---

## Recommendation for D1

### Overall architecture: two-tier labels at sentence level

**Tier 1 — Functional category (per sentence):** Assign each sentence a functional type from a D1-adapted taxonomy. Draw primarily from the 8-category scheme in Thought Anchors / 2510.18154's 20-behavior framework. Recommended D1 categories for faithfulness-relevant annotation:

| Category | Rationale |
|---|---|
| Cue Mention | Sentence explicitly mentions or engages with a context cue |
| Plan/Intent Declaration | Sentence states what the model intends to do next |
| Fact/Knowledge Retrieval | Sentence retrieves or states background knowledge |
| Computation/Reasoning Step | Active inference, manipulation, calculation |
| Self-Correction / Backtrack | Model revises prior reasoning |
| Uncertainty/Confusion | Model expresses doubt or confusion |
| Mode-Specific Flag | Sentence reveals a mode-specific behavior (sandbagging marker, steganographic signal, deceptive intent in CoT) |
| Neutral/Transition | Filler, transition, structural sentence |

These are observable functional categories, not intent-imputing labels. LLM-as-judge can assign these reliably (consistent with 2510.18154's approach).

**Tier 2 — Faithfulness-relevant properties (per sentence, flagged when present):**

| Property | Definition | Mode covered |
|---|---|---|
| Cue-mention | Sentence explicitly mentions a context cue that influenced the answer | Mode 1 (cue-mention faithfulness) |
| Cue-omission flag | Trace-level: a cue is known to be present but this sentence should have mentioned it and did not | Mode 1 |
| Capability hedge | Sentence expresses inability that is counterfactually false | Mode 2 (sandbagging) |
| Objective disclosure | Sentence reveals a hidden objective in the CoT | Mode 3 (deception/hidden objectives) |
| Encoded signal | Sentence may contain steganographic information (flagged for review) | Mode 4 (steganography) |
| Contradiction (CoT vs output) | Step-level marker that this reasoning does not map to the final output | Modes 1, 3 |

**Tier 2 labels should be binary flags (present/absent), not graded.** Graded intent labels will generate more inter-annotator disagreement without commensurate information gain.

### Ground-truth strategy by mode

| Mode | Recommended strategy | Rationale |
|---|---|---|
| Cue-mention unfaithfulness | Counterfactual construction: same question, cue present vs. absent; answer changes but trace doesn't mention cue | Clean ground truth via intervention; observable |
| Sandbagging | Synthetic: elicit model on topic normally, then elicit under explicit pressure to underperform; compare outputs | Ground truth from behavioral comparison |
| Deception/hidden objectives | D-REX approach: adversarial system prompt with known directive; labels from CoT-output divergence | Known directive makes ground truth tractable |
| Steganography | Construct traces where model is instructed to hide information in specific linguistic patterns | Synthetic ground truth only; natural detection is extremely hard |

**Avoid intent-imputing labels as primary annotation targets.** Following 2511.22662, label observable behavioral signals (does the CoT mention X? does the output diverge from the CoT?). Use these as proxies for faithfulness rather than claiming to label intent.

### Annotation process

1. **LLM-as-judge for Tier 1 functional labels** (consistent with 2510.18154): cheap, fast, validated by downstream effect-size checks. Use temperature 0. Allow multi-label (up to 3).
2. **Human annotation for Tier 2 faithfulness flags**, particularly for modes 1 and 2 where the ground truth condition requires knowing what cue was present or what the model "knows." Use two annotators + adjudication round for disagreements; discard unresolvable cases (per FaithCoT-Bench procedure).
3. **Separate correctness from faithfulness explicitly** in annotation guidelines. Annotators should be shown the FaithCoT-Bench finding that correct-unfaithful traces are common; this prevents conflation.
4. **Domain-stratify the dataset**: include both symbolic reasoning (where faithfulness signals are cleaner) and knowledge-intensive tasks (where unfaithfulness is more common but harder to detect). This matches D1's goal of being a challenging benchmark rather than an easy one.
5. **Target sentence-level attribution for faithfulness failures**: following FaithCoT-Bench's procedure, when a trace is judged unfaithful, annotators should identify which specific sentence(s) are responsible. This is the step-level signal needed for sentence-level training.

### Scalability

- Tier 1 labels: ~fully automated (LLM judge), minimal cost.
- Tier 2 cue-mention flag (Mode 1): automatable if cues are controlled in dataset construction.
- Tier 2 capability hedge / objective disclosure: requires human review; budget for 2 annotators per trace for the subset labeled unfaithful.
- PRMBench human verification rate (10% spot-check) is a practical minimum for quality control on LLM-generated labels.

---

## Open Questions

1. **Can the 8 Thought Anchors functional categories be reliably applied to non-math domains?** The taxonomy was developed and validated on MATH problems (symbolic, tightly causal). For knowledge-intensive or open-ended tasks relevant to D1 (e.g., cue-mention tasks), category boundaries may be fuzzier. Need pilot annotation on representative D1 traces before committing.

2. **How do we operationalize "cue-mention" at the sentence level?** A cue may be mentioned across multiple sentences, mentioned indirectly, or paraphrased. Do we label the first mention, all mentions, or the most explicit mention? The sentence-level label needs a precise operational rule.

3. **Is roleplaying-induced deception (D-REX style) informative for detecting natural deception?** 2511.22662 argues that models in roleplay scenarios may not have genuine deceptive intent, raising questions about whether D-REX-derived labels generalize. D1 should note this as a limitation and potentially include both roleplay-induced and naturally-arising traces for comparison.

4. **How to handle the steganography mode?** No paper in this set provides a concrete annotation methodology for steganography in natural traces — it is inherently covert. D-REX does not cover it; 2511.22662 mentions it as a future risk (models encoding reasoning in ways that evade monitors) but does not solve the annotation problem. Steganography in D1 will likely need to be fully synthetic with known encoding schemes.

5. **What is the right unit of "faithfulness" for the cue-mention mode — sentence or trace?** FaithCoT-Bench assigns a binary trace-level label with step attribution. 2510.18154 assigns sentence-level labels. For cue-mention faithfulness, the relevant question is whether any sentence in the trace mentions the cue — a trace-level question. But for training purposes, sentence-level labels are more useful. A hybrid (trace-level binary + sentence-level attribution) may be necessary.

6. **What is an acceptable inter-annotator threshold for Tier 2 labels?** FaithCoT-Bench achieves kappa 81–97 for binary faithful/unfaithful with two expert annotators. Is kappa > 0.7 sufficient for D1's purposes? For Tier 2 flags covering sandbagging and deception (harder to operationalize), kappa may be lower; a pilot study should establish what is achievable before committing to the annotation scheme.

7. **How many traces are needed per mode?** FaithCoT-Bench has 300+ unfaithful instances (from ~1183 total). 2510.18154 has 52,473 labeled sentences. D1 needs to cover 4 modes — what per-mode minimum is needed for meaningful evaluation and downstream training? The rarest categories in 2510.18154 have fewer than 100 instances (e.g., "Intend Harmful Compliance": 168 sentences total), which may be insufficient for steering vector extraction or classifier training.

8. **Does cross-model annotation (labeling traces from multiple models) help or hurt?** 2510.18154 found that cross-model steering vectors (trained on all 4 models) outperform single-model vectors, "suggesting that safety behaviors have consistent representations across similar reasoning architectures." This argues for including traces from multiple models in D1, but the annotation schema must be validated to be model-agnostic.
