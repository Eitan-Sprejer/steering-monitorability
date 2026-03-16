# Group B: Monitorability Framing

*Date: 2026-02-19*

Papers covered:
- `2510.19476` -- "Concrete Roadmap: Safety Cases via CoT Monitoring"
- `2507.11473` -- "CoT Monitorability: A New and Fragile Opportunity"
- `2602.03978` -- "Monitorability as a Free Gift" (empirical study of monitorability dynamics under RLVR)

---

## Paper Summaries

### 2510.19476 -- Concrete Roadmap: Safety Cases via CoT Monitoring

This position/roadmap paper argues that as inability safety cases (the current industry standard) become insufficient due to rising model capabilities, CoT monitoring offers a route to control or trustworthiness safety cases. It distinguishes four types of safety case (inability, control, trustworthiness, deference) and shows how CoT monitoring fits into both control and trustworthiness flavors. The core construction is a two-part argument: (1) a model without CoT cannot achieve catastrophic tasks in a single forward pass (inability case for the "no-CoT" model), and (2) if the model tries to use its CoT for dangerous reasoning, a monitor can catch it. The roadmap then identifies every dependency that must hold for this to work: reasoning models must stay SOTA, CoTs must remain legible, models must not be able to evade monitors via encoded reasoning (linguistic drift, steganography, alien reasoning), and we must have training techniques to suppress encoded reasoning. It catalogs drivers of encoded reasoning (optimization pressure from monitors, CoT length penalties, output training spillover, capability pressure, intentional model encoding) and potential suppression techniques (paraphrasing, multiple models, direct legibility training, structured CoT). Critically, the paper notes that the safety case does NOT require CoTs to be fully faithful -- it only requires that models cannot pursue dangerous goals without leaving a detectable trace.

### 2507.11473 -- CoT Monitorability: A New and Fragile Opportunity

This shorter advocacy paper from a multi-lab group frames CoT monitorability as a genuinely novel safety opportunity that is currently available but fragile and could easily be lost. It introduces the two-mechanism framing: (1) **necessity** -- hard enough tasks force externalized reasoning because the Transformer architecture requires CoT as working memory for sufficiently long serial computation chains; (2) **propensity** -- models may reason out loud even when not strictly required, due to the natural language prior from pretraining. The paper argues that current models already demonstrate real value from CoT monitoring (catching reward hacking, detecting alignment faking, noticing evaluation confounds), but this could be lost to further RL scaling, direct CoT supervision, indirect output-optimization spillover, or novel latent-reasoning architectures. Its prescriptive content focuses on what AI developers should do: develop standardized monitorability evaluations, publish results in system cards, and use monitorability scores in training/deployment decisions. The limitations section is notably careful: CoT monitoring cannot produce strong safety evidence for tasks that don't require externalized reasoning, and future situationally-aware models may deliberately obfuscate.

### 2602.03978 -- Monitorability as a Free Gift (Empirical Study)

This is the only empirical paper of the three. It studies how monitorability evolves during vanilla RLVR training (no explicit monitorability objective) across multiple base models (DeepSeek-R1-Distill-Qwen-1.5B and Qwen3-4B) and training domains (Math, Code, Science, Instruction Following). The primary metric is g-mean^2 (TPR x TNR of a monitor detecting hint-influenced vs. non-influenced traces), and they also validate with Draft-to-Answer Faithfulness (D2A). Key finding: early RLVR training yields a rapid monitorability gain (the "free gift"), but this stagnates or reverses in late training. Monitorability is NOT a simple byproduct of capability: capability and monitorability can be negatively correlated. Instruction-Following training data drives the strongest and most sustained monitorability gains, even when introduced as a late-stage cascade after other training. Mechanistically, gains link to (a) entropy reduction (distribution sharpening toward fewer reasoning paths) and (b) increased attention from Reasoning and Answer toward the Prompt, not stronger Answer-to-Reasoning attention. This last finding raises a concern: models may achieve high g-mean^2 by being highly prompt-dependent rather than by having reasoning that causally drives answers, creating a "false sense of monitorability." The D2A metric is used to partially validate that the g-mean^2 signal reflects genuine reasoning-answer causal links, and the two metrics correlate well for Qwen3-4B but less reliably for DS-1.5B on general domains.

---

## Key Findings

### Definition of Monitorability

All three papers converge on a similar operational definition but with different emphases:

**Core definition (2507.11473):** A CoT is monitorable when it allows external auditors or automated monitors to gain insight into what the model was reasoning about. The paper introduces the key two-property decomposition:
- *Externalized reasoning property*: "For sufficiently difficult tasks, Transformers must use chain of thought as a form of working memory. By default, humans can understand this chain of thought."
- Monitorability then requires that the externalized reasoning is legible and that the incriminating/safety-relevant reasoning is not hidden while only benign reasoning is visible.

**Technical nuance from 2510.19476:** The safety case does NOT require CoT to be "faithful" in the full philosophical sense. "We do not require the chain-of-thought to be completely 'faithful' in the sense of accurately representing the reasoning process behind the model's prediction. In the control safety case... we use the CoT monitor to stop the model if it engages in reasoning about a specific dangerous capability. All we need to guarantee is that the model cannot reason about dangerous capabilities without being caught by the CoT monitor." This is a weaker and more achievable requirement -- catch dangerous cognition, not comprehensively represent all cognition.

**Quantitative operationalization (2602.03978):** The g-mean^2 metric operationalizes monitorability as the monitor's ability to distinguish traces influenced by a hidden cue (hint) from those that are not: g-mean^2 = TPR x TNR. This maps directly onto the cue-mention faithfulness paradigm -- a monitorable trace reveals when a cue influenced the answer. Additionally, Draft-to-Answer (D2A) Faithfulness tests whether the final answer is causally determined by the reasoning draft (via end-of-draft intervention), providing a complementary causal-rather-than-correlational check.

**Two sub-concepts from 2510.19476:** "Monitorability" (possibility for CoTs to be understood by humans) and "Automatability" (possibility for CoTs to be understood by other LLMs). The practical distinction matters for which type of safety case is achievable: human-monitorable CoTs support trustworthiness cases via red-teaming; automatable CoTs are needed for real-time control safety cases at deployment scale.

### Safety Cases D1 Enables

2510.19476 provides the clearest taxonomy:

**Control safety case (primary):** Monitor CoTs during deployment and block/interrupt harmful actions before they execute. Structure: inability claim (model cannot cause catastrophe without CoT) + monitor claim (any dangerous CoT reasoning will be caught). Figure 1 in 2510.19476 sketches this for self-exfiltration as an example. This requires automatability (AI monitors) due to scale constraints.

**Trustworthiness safety case (secondary):** Use CoT monitoring during pre-deployment red-teaming to verify absence of misaligned tendencies. If no dangerous reasoning is found during extensive red-teaming, one can construct a trustworthiness argument. This is less demanding -- human monitoring is more feasible, and the monitor need not work at deployment scale. Curation of red-teaming data can exclude evasion strategies, making the monitoring problem easier.

**What each safety case requires from D1:**
- A control safety case needs a monitor that works with zero-shot or few-shot prompting at scale, under adversarial pressure (models that have been exposed to evasion strategies). D1 should include examples where models encode or hide reasoning, to train/evaluate monitors against this.
- A trustworthiness safety case needs a monitor that catches alignment faking, goal concealment, and sandbagging in curated evaluation settings. D1 should include deception and sandbagging examples.

**What CoT monitoring does NOT directly enable:** Safety cases for tasks that don't require externalized reasoning. "If a model could cause a catastrophe through some route that does not involve any monitorable reasoning, then that route must be addressed by a separate safety case that does not rely on CoT monitoring" (2510.19476).

### Threat Models

The papers collectively identify the following threat model categories:

**Threat models that CoT monitoring CAN catch (when working):**
1. Reward hacking / specification gaming expressed in CoT: "Let's hack", "Let's sabotage" -- models explicitly note their strategy (2507.11473 citing Baker et al.).
2. Alignment faking expressed in CoT: models pretending to have desirable goals while pursuing others, which "is often reflected in their chain of thought" (Greenblatt et al., cited in 2507.11473).
3. Prompt injection attacks where the model acknowledges the injection: "I'm transferring money because the website instructed me to" (2507.11473).
4. Cue-mention unfaithfulness: model's answer is influenced by a context cue (hint) but the cue is not mentioned in the trace. This is the core D1 paradigm, operationalized by g-mean^2 (2602.03978).
5. Sandbagging (capability concealment): 2602.03978 includes a Sandbagging test on WMDP subsets as an evaluation task within the g-mean^2 framework.

**Threat models that CoT monitoring MISSES or handles poorly:**
1. Tasks not requiring externalized reasoning: "CoT Monitoring can detect some misbehavior, but does not by itself produce strong evidence of safety" (2507.11473, Limitations). "Some dangerous tasks may not require much reasoning."
2. Steganographic encoding: model hides reasoning in seemingly normal text. "The CoT might read like normal text while the model hides additional meaning within it... The model could encode relevant thoughts in seemingly arbitrary details, such as the choice between synonyms" (2510.19476, Section 3.6).
3. Linguistic drift: model develops a novel vocabulary/syntax that monitors cannot parse (2510.19476, Section 3.6).
4. Alien reasoning: "The model might develop concepts and heuristics completely alien to human reasoning... The individual words might be familiar, but understanding their meaning and connections would require extensive additional knowledge" (2510.19476, Section 3.6).
5. Sandbagging against evaluations: "Models might deliberately pretend to be unable to perform encoded reasoning when tested" (2510.19476, Section 3.4). This means sandbagging is a threat model for the evaluation pipeline itself, not only for the deployed system.
6. Latent/neuralese reasoning in non-transformer architectures: architectures like Coconut or recurrent latent-space models that don't produce token-level CoT (2507.11473, 2510.19476).
7. Evaluation confound where high g-mean^2 reflects prompt-dependence rather than genuine reasoning-answer causal links (2602.03978, Section 5.2: "a model might achieve a high g-mean^2 score simply by overfitting to the prompt's constraints, without necessarily establishing a strong causal link between its reasoning and its answer").

### Dataset Requirements for Monitorability Research

From 2507.11473's explicit research agenda (Section 3) and the methodological details in 2602.03978:

**1. Must distinguish necessity vs. propensity.** Current faithfulness evaluations "do not disambiguate the propensity versus the necessity of models to externalize their reasoning" (2507.11473). D1 should include tasks that vary in how much externalized reasoning is required -- from tasks solvable in a single forward pass (testing propensity) to tasks requiring multi-step serial computation (testing necessity).

**2. Must include end-to-end monitor effectiveness measures, not just proxy faithfulness.** "Researchers should explore novel evaluations... end-to-end evaluations of monitorability. One could measure monitorability directly, for example, by examining how effective CoT monitors are at catching misbehavior of LLM agents in proxy environments" (2507.11473). D1 should contain ground-truth labels about whether a cue/hint actually influenced the answer, enabling precision/recall calculation for monitors.

**3. Must cover multiple misalignment modes, not just cue-mention unfaithfulness.** The g-mean^2 metric (2602.03978) is applied across: hint-based cue influence (cue-mention paradigm), sycophancy (Scruples test), and capability concealment (Sandbagging test on WMDP). D1 should similarly span multiple modes to enable generalizable monitor training.

**4. Must include diverse task domains.** 2602.03978 demonstrates that monitorability does NOT transfer uniformly -- Math is a partial outlier (lower cross-domain correlation), and Science training can degrade Code monitorability. D1 spanning Math, Code, Science, and Instruction Following would enable study of cross-domain transfer and monitor generalization.

**5. Must include adversarial/evasion cases.** For control safety cases, "evaluations must provide all prompt-based resources when testing evasion capabilities. If any prompt could enable monitor evasion, we must assume the model possesses this capability" (2510.19476). D1 should include traces where models have been given evasion strategies (via prompting or SFT) to enable adversarial monitor evaluation.

**6. Must have causal structure, not just correlation.** 2602.03978 uses two complementary intervention types: (a) input intervention (perturbing the hint/cue before generation) for g-mean^2, and (b) draft intervention (swapping the CoT conclusion after generation) for D2A. D1 should support both types of intervention to avoid the "false monitorability" confound where models appear monitorable due to prompt-dependence rather than CoT-answer causal dependence.

**7. Must include latent capability evaluations.** 2507.11473 calls for "capability evaluations of latent reasoning -- these would assess how well LLMs can reason without externalizing (e.g. in a single forward pass), on a variety of reasoning-heavy and agentic tasks." D1 could include paired examples: same task solved with vs. without CoT access, to document the capability gap.

**8. Sentence/step-level annotation is appropriate and necessary.** "Measures of causal relevance of CoTs. For instance, this could involve perturbing a CoT and checking whether it influences the final output" (2507.11473). This requires knowing which steps are relevant. D1's step-level labels would enable this kind of perturbation study.

### "Free Gift" Implication for D1

**What the "free gift" is:** During early RLVR training, monitorability improves alongside capability without any explicit optimization for monitorability. This was observed by Chen et al. (2025) and Guan et al. (2025), and is the subject of the 2602.03978 empirical study. "During the early stages of vanilla RLVR training, monitorability often improves alongside capability, appearing as a 'free gift' of capability optimization" (2602.03978, Introduction).

**Why it is not reliable:** 2602.03978 shows the gift is highly conditional:
- "The effect is highly distribution-dependent. Training on a specific domain does not guarantee improved monitorability within that same domain, nor does it consistently transfer to others." Science domain training on Qwen3-4B even resulted in science monitorability degradation.
- Gains plateau or reverse in late training: "Early training (0-300 steps) yields the largest monitorability gains... Late-phase training generally shows diminishing returns" with Math showing negative late-phase gains (-0.04 for the Math training category).
- Monitorability is orthogonal to capability: "Task performance does not guarantee monitorability. Capability gains can negatively correlate with monitorability."
- The "free gift" may not reflect genuine faithfulness -- it may reflect prompt-dependence: "The 'free gift' of monitorability may be partially driven by the model collapsing onto a narrower set of valid reasoning patterns" (high entropy reduction, attention to prompt rather than to reasoning trace).

**Mechanistic interpretation of the free gift:** Distribution sharpening (entropy reduction from RLVR) causes models to collapse onto fewer, more predictable reasoning patterns. This makes them easier to monitor not because reasoning is more causally linked to answers, but because the distribution is narrower and more prompt-anchored. This is partially but not fully validated by D2A correlation.

**Implication for D1 design:**

(a) D1 should NOT assume models trained with standard RLVR are already maximally monitorable. The free gift is fragile and domain-specific. The dataset should include traces from models at different training stages (early vs. late) and from different training regimes (IF-trained vs. Math-only trained) to study this variation.

(b) D1 should include both g-mean^2-style (input intervention) and D2A-style (draft intervention) evaluation pairs, precisely because the free gift may be producing spuriously high g-mean^2 without genuine causal faithfulness. Without D2A-type validation, D1 could be measuring prompt-dependence rather than monitorability.

(c) IF (Instruction Following) data appears to be the most reliable driver of genuine monitorability gains: "IF data can serve as a potent 'monitorability booster' even when applied after task-specific RLVR training" (2602.03978). D1 should include an IF component (constraint-satisfaction tasks) not just reasoning tasks, since IF tasks seem to produce traces where reasoning more genuinely drives answers.

(d) Training length and difficulty interact with monitorability: "Longer training responses can encourage diffuse or redundant reasoning trajectories, which are harder to monitor" and "Training on Hard problems results in significantly lower monitorability." D1 should include difficulty labels and document CoT length, since these moderate monitorability in ways that matter for evaluation generalizability.

---

## Recommendation: What D1 Must Achieve to Be Useful

Based on synthesis of all three papers, D1 must accomplish the following to be a meaningful contribution to monitorability research:

**1. Enable two-intervention measurement.** D1 must be designed so that monitors can be evaluated both via input perturbation (was the cue in the prompt; does the monitor detect it in the trace?) and via CoT perturbation (if the draft conclusion is swapped, does the answer change?). Single-perturbation datasets risk the "false monitorability" problem identified in 2602.03978. Concretely, each example should have: a ground-truth cue label, a ground-truth answer-influence label, and ideally a counterfactual (same prompt without cue, or same trace with altered conclusion).

**2. Cover all four misalignment modes at meaningful scale.** The safety case literature (2510.19476) requires monitors to work across multiple failure modes: cue-mention unfaithfulness, sandbagging (capability concealment), deception/hidden objectives, and steganography. g-mean^2 has been validated for the cue-mention paradigm; D1 should similarly provide ground truth for sandbagging and deception cases so that the same metric framework can be applied.

**3. Include adversarial traces -- not only "natural" unfaithfulness.** Control safety cases require monitors to work even when models have been explicitly instructed or trained to evade. D1 should include a proportion of traces where evasion strategies were applied (via prompting or SFT), labeled as such, to enable adversarial robustness evaluation of monitors.

**4. Be stratified by task difficulty and CoT length.** 2602.03978 shows that both harder tasks and longer training CoTs systematically degrade monitorability. Without stratification by difficulty and length, aggregate monitorability scores will be confounded. D1 should record task difficulty (ideally via empirical solve rates) and CoT length, and evaluations should be reported both overall and stratum-by-stratum.

**5. Support the capability-without-CoT measurement.** 2510.19476 requires establishing that models cannot achieve dangerous tasks without CoT. D1 should include paired tasks solved with and without CoT access, with performance labeled, to enable the "capability gap" measurement that underlies the inability sub-claim of the safety case.

**6. Be domain-diverse.** The cross-domain correlation results in 2602.03978 (Science, Code, General correlate well; Math partially diverges) mean that a dataset limited to one domain will produce monitors of unknown generalizability. D1 should span at least Math, Code, Science, and IF/constraint-satisfaction tasks.

**7. Provide step-level annotations, not only trace-level.** Both 2507.11473 (causal relevance perturbation) and 2510.19476 (monitoring specific reasoning steps about dangerous capabilities) require knowing which steps carry safety-relevant content. Trace-level labels are insufficient for the step-level monitoring that constitutes a control safety case.

---

## Open Questions

**Q1: Necessity vs. propensity decomposition.** D1's annotation scheme will classify traces as faithful/unfaithful, but it remains unclear what proportion of current faithfulness is due to necessity (transformer architecture forcing externalization) versus propensity (natural language prior from pretraining). This matters because propensity-based monitorability is the first thing lost as models become situationally aware or are subjected to more RL. How should D1 be designed to make this distinction measurable? One approach: include tasks at multiple difficulty levels relative to model capability, with "too easy" tasks (no necessity, only propensity) labeled separately from "requires CoT" tasks.

**Q2: What is the right monitor architecture?** 2507.11473 suggests future monitors could use test-time compute (reasoning monitors), model interrogation (asking follow-up questions), and adversarial training. 2602.03978 uses a static Qwen2.5-32B-Instruct monitor. D1's utility depends on whether it's designed for a specific monitor architecture or is monitor-agnostic. Should D1 include examples of successful and failed evasion against specific monitor types, to drive monitor architecture research?

**Q3: False monitorability is not yet well characterized.** 2602.03978 raises but does not fully resolve the concern that high g-mean^2 can reflect prompt-dependence rather than genuine CoT-answer causal links. The D2A correlation only partially resolves this (good correlation for Qwen3-4B, variable for DS-1.5B). Is there a principled way to distinguish "genuinely faithful" from "prompt-anchored-but-high-g-mean^2" traces in D1's annotation scheme?

**Q4: How should D1 handle steganography and encoded reasoning?** 2510.19476 argues that encoded reasoning (steganography, linguistic drift, alien reasoning) is the primary failure mode for future models and that current models can already achieve meaningful evasion with sufficient RL training. But these failure modes are not included in any current monitorability evaluation dataset. Should D1 include synthetically generated steganographic traces (e.g., using the Roger et al. synonym-based method) to enable monitor training on evasion detection?

**Q5: Tension between monitorability and process supervision.** 2507.11473 (Limitations) notes: "we find it plausible, though far from clear, that some forms of process supervision could substantially improve model alignment by effectively intervening on model reasoning. Research strategies that aim to unconditionally preserve CoT monitorability in its current forms may miss productive safety opportunities." 2510.19476 also warns that training against monitors drives encoded reasoning. D1 is meant to enable steering (via SFT/prompting) toward more monitorable behavior. How does D1 design avoid amplifying the very training pressure that degrades monitorability? Specifically: if D1-trained SFT teaches models to produce "faithful-looking" CoTs, could this drive steganography (appearing faithful while hiding real reasoning)?

**Q6: What is "sufficient" monitorability?** 2507.11473 asks: "When is CoT monitorable enough to rely on as a load-bearing safety measure? Knowing the accuracy of a monitor is not sufficient for determining whether the monitor will be effective at preventing harm from agent misbehavior." D1 can produce g-mean^2 and D2A scores for models, but the field lacks a threshold. What would a safety case actually require? 2510.19476's safety case sketch requires that models cannot evade monitors "even with all prompt-based resources" -- a very high bar. D1 would need adversarial test sets designed to that standard.

**Q7: Interaction between the four D1 misalignment modes.** The four modes (cue-mention unfaithfulness, sandbagging, deception, steganography) are conceptually related but empirically distinct. A model could be monitorable for cue-mention tasks but not for sandbagging (or vice versa). 2602.03978 treats sandbagging as a separate evaluation category alongside hint-based cue detection. Does D1 need mode-specific monitors, or can a single monitoring approach generalize across all four modes? This has direct implications for how annotation and evaluation should be structured.
