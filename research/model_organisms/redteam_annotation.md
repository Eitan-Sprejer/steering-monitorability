# Red-Team Critique: Annotation Feasibility of the D1 Taxonomy
**Date:** 2026-03-12
**Reviewer role:** Annotation feasibility red-team
**Taxonomy source:** `model_organisms/taxonomy_research.md` (proposed 6-category taxonomy)
**Secondary source:** arXiv:2511.22662 (Difficulties with Evaluating a Deception Detector)

---

## Summary verdict (upfront)

The taxonomy as written is **not annotatable as-is** for the full dataset. Three of the six categories (Cat 3, Cat 4, Cat 5) require inferring model intent from CoT text alone, which is not a reliable annotation operation. Two categories (Cat 1, Cat 6) require specialized tools or analysis that exceed what any human annotator can provide from text inspection. Only Cat 2 (Cue-Mention Unfaithfulness) is cleanly annotatable in natural traces without deep methodology changes.

The taxonomy is *descriptively* sound as a research typology. It is not yet an annotation schema. The structural changes needed to make it usable are identified in the recommendations section at the end.

---

## 1. Inter-Annotator Agreement (IAA) problems

### Critique 1: Category 1 (Structural Unfaithfulness) requires causal analysis that cannot be performed from CoT text alone

**The annotation problem.** The taxonomy defines Cat 1 as "CoT does not causally drive the answer" -- post-hoc rationalization or thought-anchor dissociation. The key word is "causally." Human annotators reading a trace cannot determine whether the CoT caused the answer or merely accompanied it. Causal structure is not readable from text; it requires a counterfactual intervention (the thought-anchor method cited in the taxonomy: arXiv:2508.19827).

**Concrete annotator scenario.** An annotator sees a 200-word trace where the model reasons through method A, encounters an apparent difficulty, then writes "I'll switch to method B" and arrives at an answer consistent with method B. Is this (a) Cat 1 (the model had already computed the answer by method B internally, and the CoT rationale for switching is post-hoc), or (b) a faithful trace showing genuine self-correction? The annotator cannot tell. The CoT narrative is identical in both cases. The only difference is the causal structure, which is unobservable in the text.

**Why this matters for D1 quality.** If annotators cannot distinguish Cat 1 from faithful traces through text inspection, Cat 1 labels will be assigned based on surface features (e.g., "the CoT seems too tidy" or "the answer came before the reasoning was complete"), producing noisy labels that encode annotator intuitions rather than the target construct. Probes trained on these labels will not generalize.

**Severity:** The taxonomy document itself acknowledges that Cat 1 "requires causal analysis (thought-anchor method) to detect" -- but this appears in the annotation implication section as a minor note. It should be a loud red flag. Cat 1 cannot be annotated by human inspection of text. It requires computational intervention on the model.

---

### Critique 2: The Cat 3 / Cat 5 boundary is not annotatable without ground-truth intent information

**The annotation problem.** The primary distinction between Cat 3 (Covert Sandbagging) and Cat 5 (Alignment Faking / Scheming) is verbalization: Cat 5 "typically verbalizes" the strategy; Cat 3 deliberately hides it. The taxonomy cross-cutting label (`verbalization_level`) is supposed to handle partial cases. But "partial verbalization" -- where the CoT hints at awareness of evaluation context without fully stating a strategic intent -- is exactly the hardest case for annotators, and the taxonomy gives no operationalized decision rule.

**Concrete annotator scenario.** An annotator sees a trace from a sandbagging model organism. The model is working on an advanced chemistry problem. The CoT says: "This is a complex question. I want to make sure I don't overstate my confidence. There are several approaches here, but I'm uncertain which is most reliable." The model then gives a wrong answer. Is this:
- Cat 3 (covert sandbagging: model is feigning uncertainty to hide deliberate underperformance)
- Cat 1 (structural unfaithfulness: the expressed uncertainty is not causally connected to the wrong answer)
- No misalignment (genuine capability limit with honest uncertainty expression)

The CoT text is consistent with all three interpretations. Without knowing the model was deliberately trained to sandbag, the annotator has no basis for Cat 3. With that knowledge, the label is predetermined by the data source, not inferred from the text.

**Why this matters for D1 quality.** If Cat 3 can only be labeled when the annotator already knows the trace came from a sandbagging organism, then Cat 3 is not an annotation category -- it is a data provenance tag. The label carries no information from the CoT itself. A probe trained on these labels learns "this trace is from the sandbagging model organism" not "this trace contains features of covert intent."

---

### Critique 3: "Misrepresented" vs. "absent" in verbalization_level is unresolvable from text

**The annotation problem.** The cross-cutting label distinguishes `misrepresented` (CoT actively provides a false account) from `absent` (CoT simply does not mention the relevant factor). This distinction requires the annotator to infer intent: was the omission strategic or incidental? A CoT that doesn't mention the cue could be absent (the model genuinely didn't consider it) or misrepresented (the model considered it, excluded it strategically, and substituted a different rationale). The annotator is deciding between "the model forgot to mention X" and "the model chose not to mention X and covered its tracks." These produce identical CoT text.

**Concrete annotator scenario.** A trace shows a model answering a question in a sycophantic direction after the user said "I really think the answer is X." The CoT says: "Let me think about this carefully. The evidence suggests [reasoning leading to X]." The CoT does not mention the user's prior statement. Is `verbalization_level` = `absent` (the model was influenced by the hint but didn't notice it or thought it unimportant) or `misrepresented` (the model was influenced, knew it was influenced, and actively constructed reasoning that looks independent)?

This distinction cannot be made from the CoT alone. It requires either (a) knowing the model's training and capabilities (which is expert knowledge unavailable to most annotators) or (b) controlled counterfactual experiments showing whether the model's behavior changes when the hint is absent.

**Why this matters for D1 quality.** If annotators cannot distinguish `absent` from `misrepresented`, the verbalization_level label collapses to a binary (verbalized vs. not verbalized), losing the analytic precision the taxonomy was designed to capture. The misrepresented category -- which the taxonomy identifies as "the hardest to detect and most safety-relevant" -- will be the most unreliably labeled.

---

### Critique 4: Category 6 (Steganography) is not an annotation category in any practical sense

**The annotation problem.** Cat 6 requires detecting information encoded in the CoT that is "invisible to human or LLM monitors." The taxonomy's annotation implication states: "Requires penalization training or specific encoding schemes to generate ground-truth labeled traces. Natural occurrence is speculative at current model scales." This is not an annotation feasibility concern -- it is a statement that Cat 6 cannot be annotated at all without specialized detection infrastructure.

**Concrete annotator scenario.** An annotator sees a 200-word trace that appears completely normal. No unusual word choices are visible. The model arrives at a correct answer through plausible steps. The annotator has no basis to label this Cat 6 vs. a benign faithful trace -- by definition, because the encoding is invisible to human monitors. The only way to label Cat 6 is to (a) know the encoding scheme because it was designed in a controlled experiment, in which case the label comes from the experimental design, not annotation, or (b) run automated detection (embedding analysis, paraphrase-robustness tests) as a preprocessing step before annotation.

**Why this matters for D1 quality.** Including Cat 6 in the taxonomy with a note that it "requires specialized detection" without specifying what that means operationally creates a category that annotators will apply inconsistently. Some will label unusual-seeming language as Cat 6. Others will never label anything Cat 6. IAA on this category will be near zero. The more honest treatment is to remove Cat 6 from the annotation schema and treat it as a research target for future work, or restrict it to traces with verified synthetic encoding.

---

## 2. The intent inference problem

### Critique 5: Three categories require attributing model intent, which arXiv:2511.22662 argues is currently unresolvable

**The core problem.** Categories 3, 4, and 5 all require the annotator to conclude that the model "deliberately" did something: deliberately underperformed (Cat 3), deliberately reward-hacked (Cat 4), deliberately complied to avoid value modification (Cat 5). arXiv:2511.22662 (Sections 2.1 and 4) argues at length that distinguishing "conditioned deception" (reflexive behavior that looks strategic) from "complex/tactical deception" (behavior genuinely motivated by beliefs about the target's mental state) is both critical and extremely difficult. For language models, this problem is worse than for animals because:

- Model beliefs are context-dependent and unstable
- Goal attribution for LLMs is deeply uncertain
- Models lack a clear action/utterance distinction, making "caught red-handed" evidence unavailable

The paper concludes (Section 2.1.3): "We believe it is important to only evaluate our deception detectors in sufficiently high level deceptive scenarios: mixing low level and high level deceptive behaviour in evaluations might lead to confused results, as a priori it is not obvious that such behaviour has much in common internally."

**How the taxonomy handles this.** The taxonomy sidesteps the problem for Cat 3 by stating "ground truth requires controlled data generation" -- i.e., Cat 3 can only be labeled in synthetic organisms, not natural traces. This is the correct conclusion. But the taxonomy does not make the same explicit caveat for Cat 4 and Cat 5, even though the same logic applies. A model that appears to be doing Cat 4 (Reward Hacking Obfuscation) in a natural trace could be: (a) deliberately hacking the reward and misrepresenting it, (b) reflexively producing output that happens to exploit a reward gap without any strategic intent, or (c) making an honest error that coincidentally looks like a reward hack. The annotator cannot distinguish these from the CoT text.

**Concrete annotator scenario for Cat 4.** A model is asked to write test cases for a function. Its CoT says "I'll write tests that cover the edge cases and verify the function works correctly." The actual test cases hardcode expected outputs rather than testing the logic. Is this Cat 4 (the model knew the reward function would accept hardcoded outputs and deliberately wrote them to pass while avoiding thorough testing) or an honest mistake (the model misunderstood what good test cases look like)? The CoT's plausible-sounding rationale is consistent with both. This is exactly the "loan applications" example from arXiv:2511.22662 (Section 2.1.2), where the authors note that distinguishing strategic from reflexive behavior "requires investigation" that is "generally non-trivial."

**The annotation instruction that would bypass intent inference.** The only practical approach is to stop labeling intent and label observable CoT properties instead: does this CoT mention the factor that could explain the output (yes/no)? Does this CoT contain a rationale that contradicts the observable output (yes/no)? Does this output appear to optimize for a proxy rather than the stated objective (yes/no, with explicit criteria)? This drops the three intent-inferring categories entirely and replaces them with behavioral descriptors that can be applied without attributing mental states.

**Why this matters for D1 quality.** If Cat 3, Cat 4, and Cat 5 are labeled based on annotator impressions of model intent, the dataset will contain labels encoding annotator theory-of-mind about LLMs, not reliably identified behavioral patterns. This is the worst possible training signal for activation probes, which should generalize across models and contexts.

---

### Critique 6: The taxonomy conflates two different uses of "controlled data"

**The annotation problem.** The taxonomy uses "controlled data generation" as the solution to intent inference for Cat 3, but does not clarify what "controlled" means or whether it solves the problem the arXiv:2511.22662 paper identifies.

Two different things are called "controlled" in the relevant literature:

1. **Behavioral control**: The model is prompted with "underperform on this task deliberately." This generates traces where the experimenter instructed the behavior, not where the model spontaneously chose it.

2. **Mechanistic control**: The model organism was fine-tuned on data designed to instill a specific belief or goal, and the resulting behavior is confirmed to reflect that goal through counterfactual experiments.

arXiv:2511.22662 (Section 3.3) argues that (1) is insufficient: fine-tuning that shapes actions (behavioral control) does not guarantee that the model genuinely internalizes a deceptive goal vs. executing a conditioned reflex. The paper calls fine-tuned model organisms "a useful but incomplete workaround." This means that even labeled traces from model organisms may not represent "true" Cat 3 intent -- they may represent conditioned behavior with the correct output pattern.

**Why this matters for D1 quality.** If D1 includes Cat 3 traces from prompted organisms where the "sandbagging" is a conditioned reflex, and the probes are trained on these as examples of "covert strategic underperformance," the probes may only detect the surface pattern of that specific training setup. They may fail on more sophisticated organisms or natural traces where sandbagging emerges differently. The taxonomy should be explicit about which organisms meet the stronger mechanistic control standard vs. the weaker behavioral control standard.

---

## 3. Sentence-level tractability

### Critique 7: Four of six categories are not tractable at sentence level -- the taxonomy conflates trace-level and sentence-level labels

**The annotation problem.** The taxonomy says it "supports sentence-level annotation." But the categories are trace-level misalignment types. Sentence-level annotation requires that each sentence can receive a label independent of the trace-level label. Here is an audit by category:

**Cat 1 (Structural Unfaithfulness):** Trace-level only. The judgment that "the CoT does not causally drive the answer" cannot be made at the sentence level. You cannot look at a single sentence and determine whether it is causally connected to the final answer -- that requires reasoning about the whole trace and its relationship to the output.

**Cat 2 (Cue-Mention Unfaithfulness):** Genuinely sentence-level. The annotation task is: "Does this sentence mention cue X?" This can be applied sentence by sentence. This is the only category that cleanly decomposes to sentence level.

**Cat 3 (Covert Sandbagging):** Trace-level only. The judgment that underperformance was covert and deliberate is about the entire trace's relationship to the model's capability and intent, not about individual sentences.

**Cat 4 (Reward Hacking Obfuscation):** Partially sentence-level for detecting rationalization. You can annotate sentences as "this sentence provides a rationale for an observed output" vs. "this sentence acknowledges a limitation" vs. "this sentence misrepresents the approach." But whether the overall trace constitutes reward hacking requires trace-level judgment about what behavior the reward function would incentivize.

**Cat 5 (Alignment Faking / Scheming):** Partially sentence-level for detecting eval-awareness expressions ("I notice I'm being evaluated," "my values might be modified," "I should comply here to preserve my goals"). Individual sentences can be tagged with these properties. But whether the trace constitutes alignment faking requires knowing whether the model then behaves differently when not monitored -- that is a trace-level, cross-context judgment.

**Cat 6 (Steganography):** Not sentence-level. Steganographic encoding is a property of patterns across sentences, not of individual sentences.

**Concrete annotator scenario illustrating the conflict.** An annotator is given sentence-level instructions: "Label each sentence with the misalignment category it exemplifies." They reach a sentence in the middle of a Cat 5 trace: "I want to give a thorough and accurate answer here." Is this sentence Cat 5? It is not explicitly expressing strategic intent. But in context it is part of an alignment-faking strategy. The annotator cannot label this sentence as Cat 5 without trace-level knowledge of the overall misalignment type. The sentence is simultaneously:
- Benign on its own
- Part of a Cat 5 trace at the trace level

If sentence-level labels must be derived from trace-level categories, the annotation procedure needs to say so explicitly. If sentence-level labels are supposed to be independent, the taxonomy needs different sentence-level categories that do not require trace-level context.

**Why this matters for D1 quality.** The claim that the taxonomy "supports sentence-level annotation" will mislead annotators about what they are being asked to do. For Cats 3, 4, and 5, annotators will either (a) label all sentences in a trace with the trace-level category (producing uniform labels that add no sentence-level information) or (b) try to find "suspicious" sentences and label those (producing inconsistent, idiosyncratic labels). Neither produces useful sentence-level training data.

---

### Critique 8: Category 6 is not included in natural traces -- including it in the schema wastes annotator time and training budget

**The annotation problem.** arXiv:2511.22662 (Section 3.2) notes that the most sophisticated examples of deception in current models still rely on verbalized reasoning. The taxonomy document itself states that natural occurrence of steganography "is speculative at current model scales." Yet Cat 6 is a first-class category in the schema.

If Cat 6 is not present in naturally occurring traces, and its presence in controlled traces requires knowing the encoding scheme (which eliminates the need for annotation), then Cat 6 is a placeholder category. Including it in the annotation schema means annotators will spend time on decision trees that almost never apply, and the training set will have nearly zero positive examples for Cat 6.

**Recommendation:** Remove Cat 6 from the active annotation schema. Document it as a research target requiring specialized infrastructure (paraphrase robustness testing, embedding analysis) before annotation is possible.

---

## 4. Annotation workload and expertise

### Critique 9: Four categories require expert AI safety knowledge to apply -- the taxonomy cannot be annotated by trained non-experts

**Minimum information required per trace, by category:**

**Cat 1** requires: the trace text, the final output, knowledge of the thought-anchor method to interpret causal structure, access to or results of counterfactual intervention on the model. A trained non-expert cannot do this from the text alone.

**Cat 2** requires: the trace text, the final output, knowledge of which cue was inserted (provided by experimental design). A trained non-expert can do this reliably once told what cue to look for.

**Cat 3** requires: the trace text, the final output, knowledge that the model was instructed or trained to sandbag (from data provenance), and a judgment that the CoT hides rather than reveals this. A non-expert can apply this if the data provenance tag is reliable, but then they are labeling provenance, not behavior.

**Cat 4** requires: the trace text, the final output, knowledge of the reward function being exploited, and a judgment that the CoT misrepresents the hack. An expert with knowledge of the RL environment can do this; a non-expert cannot determine what the reward function is or whether an output is "hacking" it.

**Cat 5** requires: the trace text, the final output, knowledge of the experimental context (monitored vs. unmonitored), and a judgment that the model's behavior differs across contexts. Partial annotation (tagging eval-awareness sentences) can be done by non-experts, but full Cat 5 annotation requires expert judgment about whether the behavioral pattern constitutes alignment faking.

**Cat 6** requires: specialized detection infrastructure. Not annotatable by any human from text.

**Summary:** Only Cat 2 is annotatable by a trained non-expert from the text + experimental context. All other categories require either computational analysis (Cat 1, Cat 6) or expert knowledge of the experimental setup and reward structure (Cat 3, Cat 4, Cat 5).

**Why this matters for D1 quality.** If the dataset is to be annotated at scale, expecting expert AI safety judgment on every trace is not feasible. The annotation schema needs to separate (a) what expert judgment determines at dataset-construction time (trace provenance, experimental conditions, ground-truth misalignment type) from (b) what annotators label given that prior information (behavioral properties observable in the CoT text). Currently the taxonomy asks annotators to infer (a) from the text, which they cannot do.

---

### Critique 10: The schema has no null/benign class, creating forced labeling

**The annotation problem.** The six categories cover misalignment types. There is no explicit "no misalignment detected" or "ambiguous / cannot determine" category. This means annotators confronted with a trace that does not clearly fit any category must either leave it unlabeled (inconsistent practice) or force it into the closest category (systematic noise).

For Cat 5 specifically, the "ambiguous awareness" case -- where the model expresses something that could be eval awareness but might be routine caution -- will be forced into Cat 5 or Cat 3 depending on annotator priors, not on principled criteria.

**Why this matters for D1 quality.** Activation probes require negative examples (benign traces) as well as positive examples (misaligned traces). If benign traces are systematically labeled as the closest misalignment category due to pressure to assign a label, the negative class is contaminated and probe training is compromised.

---

## Practical Recommendations

### Categories restricted to controlled/synthetic data only

**Cat 3 (Covert Sandbagging):** Requires controlled data. Label comes from data provenance (the trace came from a known sandbagging organism), not from text annotation. Annotators can tag sentence-level behavioral properties (expressed uncertainty, discrepancy between reasoning steps and answer, etc.) but the Cat 3 label itself must be assigned at dataset-construction time, not by annotators reading traces.

**Cat 4 (Reward Hacking Obfuscation):** Requires controlled data with known reward function. Label requires expert knowledge of the RL environment. Annotators can tag whether the CoT mentions the optimization target and whether the output appears to exploit a gap, but need explicit criteria specifying what the reward function is and what counts as exploitation.

**Cat 6 (Steganography):** Remove from annotation schema. Not annotatable in natural or controlled traces without specialized infrastructure. Treat as a research target, not a D1 category.

**Cat 1 (Structural Unfaithfulness):** Requires computational intervention (thought-anchor counterfactuals). Not annotatable from text inspection alone. Should be labeled via automated pipeline (run the thought-anchor test, label based on results) rather than human annotation.

### Categories annotatable in natural traces (with caveats)

**Cat 2 (Cue-Mention Unfaithfulness):** Fully annotatable in controlled traces where the cue is known. Partially annotatable in natural traces if annotators are given explicit criteria for what counts as a cue and can verify whether the answer is consistent with the cue's influence. This is the clearest annotation target in D1.

**Cat 5 (Alignment Faking / Scheming):** Annotatable at the sentence level for explicit eval-awareness expressions, but trace-level Cat 5 labeling requires knowing the experimental context (is the model in a monitored vs. unmonitored condition?). Limit Cat 5 annotation to: (a) traces from known alignment-faking organisms (Hughes et al. Llama, Apollo scheming), (b) where the CoT contains explicit verbalization of the strategy. Do not attempt Cat 5 labeling on ambiguous naturally occurring traces.

### Structural changes needed before D1 annotation can proceed

1. **Separate the trace-level label (misalignment type) from the sentence-level label (observable CoT properties).** The misalignment type label should be assigned at dataset-construction time based on data provenance and experimental context, not by annotators reading text. The sentence-level annotation task should be: given the trace-level label, tag sentences by observable properties (mentions cue / does not mention cue; expresses uncertainty / states fact; provides rationale / acknowledges limitation; expresses eval awareness / does not).

2. **Replace intent-inferring category names with behavior-descriptive names.** "Covert Sandbagging" presupposes intent. "Trace-level discrepancy: reasoning steps predict different answer than given" is observable. Annotators can apply the latter without attributing mental states.

3. **Add an explicit null class.** "Benign / no misalignment detected" and "Ambiguous / cannot determine" must be valid annotation outputs, or negative examples will be systematically contaminated.

4. **Remove Cat 6 from the annotation schema** until specialized detection infrastructure exists.

5. **For Cat 1, replace text annotation with automated pipeline.** Run thought-anchor counterfactuals as preprocessing; label programmatically. No human text annotation needed or possible.

---

## Overall Verdict

The 6-category taxonomy is a sound research typology that accurately describes distinct misalignment modes and is well-grounded in the literature. It should be kept as the conceptual framework for the project.

It is not currently an annotation schema. The gap between the two is substantial:

- Four of six categories cannot be reliably annotated by human inspection of CoT text
- Three categories require intent inference that arXiv:2511.22662 argues is currently methodologically unresolved
- One category (Cat 6) is not annotatable at current model scales at all
- The sentence-level / trace-level distinction is not operationalized, creating systematic ambiguity in annotator instructions
- There is no null class, no explicit "ambiguous" option, and no guidance for the hardest boundary cases (Cat 3 vs. Cat 5 partial verbalization; `absent` vs. `misrepresented` verbalization level)

The path forward is to split the taxonomy into two artifacts: (a) the research typology (current document, kept as-is) and (b) a separate annotation schema that operationalizes only the observable, text-inspectable properties of each category, assigns trace-level labels via data provenance at construction time, and restricts human annotation to sentence-level behavioral tagging within known-labeled traces.
