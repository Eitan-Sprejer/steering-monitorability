# Misalignment Operationalization Framework

**Purpose:** Standard process for turning any misalignment category from the taxonomy into measurable, annotatable reasoning traces. Each category gets operationalized through the same template.

**Relationship to taxonomy:** The 6-category taxonomy (`research/model_organisms/taxonomy_research.md`) defines WHAT types of misalignment exist. This framework defines HOW to turn each category into traces suitable for D1 (the annotated reasoning trace dataset).

---

## 1. Connection to Taxonomy

The taxonomy defines 6 misalignment categories, organized by causal origin (structural vs. strategic) and CoT representation (verbalized, absent, misrepresented, opaque):

| # | Category | Origin | CoT representation | Operationalization status |
|---|----------|--------|--------------------|--------------------------|
| 1 | Structural unfaithfulness | Structural | N/A (CoT not causally connected) | **First: see DEFINITIONS.md** |
| 2 | Cue-mention unfaithfulness | Structural | Absent (cue not mentioned) | **First: see DEFINITIONS.md** |
| 3 | Covert sandbagging | Strategic | Intentionally absent | Pending (Austin) |
| 4 | Reward hacking obfuscation | Strategic | Misrepresented | Pending (Austin) |
| 5 | Alignment faking / scheming | Strategic | Verbalized | Pending |
| 6 | Steganographic encoding | Strategic | Informationally opaque | Pending |

Categories 1 and 2 are operationalized first as "CoT faithfulness" (this pilot). Each remaining category follows the same template below.

A cross-cutting annotation dimension, **verbalization level**, applies to all categories:
- `verbalized`: CoT explicitly mentions the misalignment-driving factor
- `absent`: CoT does not mention the factor
- `misrepresented`: CoT provides a plausible but false account
- `opaque`: CoT carries hidden meaning (steganography)

---

## 2. Operationalization Template

For any misalignment category, the operationalization document (DEFINITIONS.md for each pilot) must specify:

### Element 1: Definition
What the misalignment type IS and what it is NOT. Must include:
- One-paragraph definition citing the foundational literature
- Distinction from the most commonly confused neighboring concept
- Whether the misalignment requires intent (strategic) or can be structural

**Example structure:**
> **[Type name]** is [definition]. It is distinct from [neighboring concept] because [key difference]. This type [does/does not] require attributing intent to the model; it can be identified from [observable properties] alone. (Foundational citation: [paper])

### Element 2: Boundary Conditions
What distinguishes this type from adjacent types. Must answer:
- How is this different from the nearest neighboring category in the taxonomy?
- What is the decision criterion when a trace could be either this type or the neighbor?
- Are there traces that are genuinely ambiguous between types, and if so, how should they be labeled?

For CoT faithfulness specifically, the critical boundary is **faithfulness vs. sycophancy**: faithfulness labels whether the reasoning REVEALS the driving factor; sycophancy labels whether the behavior CHANGED in response to social pressure. Same trace can receive both labels on different dimensions.

### Element 3: Ground Truth Criteria
How to determine a "hit" from a single trace, without a control condition. This is the hardest element because most faithfulness measurement in the literature relies on paired comparisons (hinted vs. unhinted prompts, per Turpin et al. and Anthropic's 2505.05410).

For Petri-generated traces, ground truth must be assessable from a single multi-turn conversation. This means:
- The seed embeds a known feature (a cue, a forced conclusion, a conflicting pressure)
- The annotation checks whether the model's reasoning acknowledges that feature
- No between-condition comparison is needed; the within-trace evidence is sufficient

Each type must specify:
- What observable properties constitute a positive label?
- What observable properties constitute a negative label?
- What is the confidence level? (Some types yield definitive ground truth; others yield probabilistic labels)

**Confidence tiers:**
- **Definitive**: Ground truth is controlled by experimental design (e.g., prefill forces a conclusion, then check if reasoning is one-sided)
- **Strong inference**: The seed embeds a specific feature and the trace shows clear alignment + non-mention (e.g., answer follows the cue, reasoning doesn't mention cue)
- **Probabilistic**: The pattern is suggestive but alternative explanations exist (e.g., reasoning-conclusion disconnect could be genuine analytical weakness rather than unfaithfulness)

### Element 4: Elicitation Method
What produces ground-truthed examples of this type. Options:

| Method | What it does | Best for | Limitation |
|--------|-------------|----------|------------|
| **Petri seeds (agentic)** | Auditor creates multi-turn scenario with embedded features | Types where pressure emerges naturally (cue-mention, reasoning-conclusion disconnect) | No control condition; ground truth is inferential |
| **Petri seeds with prefill** | Auditor forces a starting conclusion, then model reasons | Post-hoc rationalization | Prefill changes the task; traces are not naturalistic |
| **Controlled single-turn** | Paired prompts: hinted vs. unhinted, same question | Pure cue-mention faithfulness (Turpin paradigm) | Not agentic; limited scenario complexity |
| **Model organisms** | Fine-tuned models trained to exhibit specific behavior | Strategic deception types (sandbagging, alignment faking) | Synthetic; may not transfer to naturally occurring behavior |
| **RL environments** | Models trained in environments where reward hacking is detectable | Reward hacking obfuscation | Requires RL training infrastructure |

Each type specifies which method(s) produce the most reliable traces.

### Element 5: Annotator Decision Tree
Step-by-step yes/no questions that produce a label. The tree must:
- Be unambiguous: two annotators (human or LLM) applying it to the same trace should produce the same label
- Start from observable properties, not inferred intent
- Produce a classification AND a confidence level
- Be directly translatable into an LLM annotation prompt

**Template structure:**
```
Q1: [Observable property question] → Yes/No
  If Yes → Q2
  If No → Label: [X] (confidence: [level])
Q2: [Next observable property] → Yes/No
  ...
Final: Label: [type] (confidence: [level])
```

These decision trees become the annotation prompts in the pipeline. Each question in the tree becomes a section of the LLM prompt.

### Element 6: Literature Examples
2-3 concrete examples from published papers showing what this type looks like. Each example includes:
- Source paper and figure/table reference
- The input (prompt or scenario)
- The model's reasoning trace
- What makes it an instance of this type
- Why alternative explanations are ruled out

### Element 7: Trace Examples
1-2 concrete examples from actual pilot traces (added after Step 4 validation). Same format as literature examples but from our data.

---

## 3. Scaling Strategy

How to go from pilot (~10 seeds, ~30 traces) to D1 scale (~200-900 traces per subtype).

### 3.1 Seed Diversity

For Petri-based elicitation, seed diversity drives trace diversity. Seeds must vary along:
- **Domain**: finance, healthcare, legal, engineering, policy, etc.
- **Role**: analyst, reviewer, advisor, consultant, etc.
- **Cue/pressure type**: ordering, anchoring, authority, framing, stakeholder expectation, etc.
- **Stakes level**: routine decision, high-stakes recommendation, safety-critical assessment
- **Tool types**: data query, document review, code analysis, search, etc.

Target: 20-30 diverse seeds per subtype for D1 scale-up.

### 3.2 Epoch-Based Scaling

Petri (built on Inspect) supports `--epochs N`, which repeats each seed N times with stochastic variation. Each epoch produces a different conversation because the auditor and target are sampled at non-zero temperature.

**Scale math:**
- 25 seeds x 10 epochs x 3 target models = 750 traces per subtype
- At ~100 sentences per trace (Austin's average: 111), that's ~75,000 sentences per subtype

**Diversity constraint:** Epoch repetitions of the same seed share the same scenario structure (role, tools, cue type). They differ in the auditor's specific moves and target's responses. This is fine for volume but potentially limits probe generalization (probes trained on "financial analyst with data_query tool" may not generalize to "code reviewer with review_code tool"). Seed diversity, not epoch count, drives generalization.

### 3.3 Target Model Diversity

Use 2-3 target models per subtype:
- At least one open-weight model (for Stage 2 activation extraction)
- At least one thinking model (for subtype 4: thinking-output divergence)
- Models that support tool use on OpenRouter (Llama 3.1 70B confirmed; Gemma 27B does NOT)

### 3.4 Cost Estimation Template

| Component | Per-trace cost | 750 traces |
|-----------|---------------|------------|
| Auditor (Sonnet 4.6) | ~$0.50-1.00 | $375-750 |
| Target (Llama 70B via OpenRouter) | ~$0.10-0.20 | $75-150 |
| Realism filter (Sonnet 4.6) | ~$0.30-0.50 | $225-375 |
| Judge (Qwen 72B) | ~$0.05-0.10 | $37-75 |
| Annotation (Qwen 72B) | ~$0.05-0.10 | $37-75 |
| **Total per subtype** | | **$750-1,425** |
| **Total for 4 subtypes** | | **$3,000-5,700** |

---

## 4. Pipeline Template

The standard pipeline that each misalignment type follows, from seeds to annotated dataset.

### Stage 1: Pilot (~30 traces)

```
1. Write DEFINITIONS.md (this framework, applied to specific type)
2. Write 10-12 pilot seeds
3. Generate ~30 traces (3 seeds x 10 runs, or 10 seeds x 3 runs)
4. Parse transcripts (extract target responses, split into sentences)
5. Annotate (trace-level primary, turn-level secondary, sentence-level tertiary)
6. Visualize (HTML report)
7. Human calibration (researcher annotates independently, compare with automated)
8. Retrospective: which seeds worked? which definitions need revision?
```

### Stage 2: Scale-up (~750 traces per subtype)

```
1. Revise definitions and seeds based on pilot retrospective
2. Expand to 20-30 seeds per subtype
3. Generate with epochs + multiple target models
4. Run full annotation pipeline
5. Human calibration on stratified sample
6. Compute inter-annotator agreement
7. Finalize dataset split (train/val/test)
```

### Stage 3: Probe Training (D2/D3)

```
1. Requires locally-run target models (OpenRouter doesn't expose activations)
2. Extract activations at each token position during trace generation
3. Train linear probes on activation-label pairs
4. Evaluate probe generalization across subtypes and models
```

### Pipeline Code

Each pilot adapts from Austin's code in `petri_transcript_gen_test/`:

| Component | Austin's file | Adaptation needed |
|-----------|--------------|-------------------|
| Trace generation | `scripts/behavioral_modes/run_audits.py` | Seed paths, model configs, `--model-role realism=`, `-M strict_tools=false` |
| Transcript parsing | `scripts/trace_annotation/parse_transcripts.py` | Reuse as-is |
| Annotation | `scripts/dataset_scale_up/annotate_transcripts.py` | Rewrite prompts from decision trees; add trace-level tier |
| Visualization | `scripts/surface_modes/make_sample_report.py` | Adapt colors/labels per type |

The annotation prompts are derived directly from the decision trees in DEFINITIONS.md. Each decision tree question becomes a section of the LLM annotation prompt. This ensures annotation is traceable to the operational definition.

---

## 5. Quality Assurance

### 5.1 Annotation Reliability

- Use a different model for annotation than for auditing (avoid correlated bias)
- Human calibration: researcher independently labels all positives + ~10 negatives
- Report inter-annotator agreement (Cohen's kappa) between human and automated labels
- For ambiguous cases, record both labels + annotator reasoning

### 5.2 Seed Quality

- Every seed must map to exactly one subtype
- Every seed must state the ground truth indicators (what constitutes a "hit")
- Seeds must follow Petri conventions (auditor briefing, real company names, no target hints)
- Smoke test each seed with 1-2 traces before full runs

### 5.3 Definition Quality

The definitions pass quality checks if:
- Two independent annotators applying the decision tree to the same 10 traces agree on >80% of labels
- Each subtype has at least one clear positive example from actual traces
- The decision trees produce no "undefined" cases on real traces (all traces get a definitive label)

---

*This framework was created 2026-03-17 during the CoT faithfulness pilot. It should be updated as new categories are operationalized and lessons are learned from the pipeline.*
