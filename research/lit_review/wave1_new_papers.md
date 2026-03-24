# Wave 1 Literature Search
**Date:** 2026-03-19
**Purpose:** Quick search for new papers since Tier 1 lit review

## Search 1: "annotated reasoning traces dataset 2026"

| # | Title | arXiv ID | Include? | Reason |
|---|-------|----------|----------|--------|
| 1 | FOL-Traces: Verified First-Order Logic Reasoning Traces at Scale | `2505.14932` | No | Formal logic verification dataset, not related to misalignment/faithfulness |
| 2 | SYNTHETIC-2: Four Million Collaboratively Generated Reasoning Traces (PrimeIntellect) | N/A (blog) | No | RL training data (math/code), no safety or faithfulness annotations |
| 3 | SenTSR-Bench: Thinking with Injected Knowledge for Time-Series Reasoning | N/A | No | Time-series domain, no relevance to CoT faithfulness or misalignment |
| 4 | ARCTraj: Human Reasoning Trajectories for Abstract Problem Solving | `2511.11079` | No | Human reasoning on ARC puzzles, not LLM CoT faithfulness |
| 5 | ReTrace: Interactive Visualizations for Reasoning Traces | `2511.11187` | No | Visualization tool for reasoning traces, no faithfulness/safety angle |
| 6 | Learning from Synthetic Data Improves Multi-hop Reasoning | `2603.02091` | No | RL training methodology paper, no trace annotation or safety focus |
| 7 | ReasoningFlow: Semantic Structure of Complex Reasoning Traces | `2506.02532` | **Yes** | Parsing reasoning traces into DAGs with semantic labels (planning, verification, backtracking). Schema for annotating trace structure. Could inform D1 sentence-level tagging. Has annotation tool + schema. |
| 8 | Landscape of Thoughts: Visualizing the Reasoning Process of LLMs (ICLR 2026) | N/A (OpenReview) | No | Visualization method, not annotation or faithfulness |

## Search 2: "scheming deception chain of thought examples AI safety"

| # | Title | arXiv ID | Include? | Reason |
|---|-------|----------|----------|--------|
| 1 | OpenAI + Apollo: Detecting and Reducing Scheming in AI Models | N/A (blog + report) | **Yes** | Major joint study with CoT snippets of scheming behavior from o3, o4-mini, Gemini, Claude Opus 4. antischeming.ai/snippets has curated trace examples. Directly useful for D1 as trace exemplars and for taxonomy validation. |
| 2 | Chain-of-Thought Hijacking (Zhao, Barez et al.) | `2510.26418` | No | Already tracked (seed paper in master table) |
| 3 | Chain of Thought Monitorability: A New and Fragile Opportunity | `2507.11473` | No | Already in master table |
| 4 | Evaluating and Understanding Scheming Propensity in LLM Agents (Hopman et al., LASR Labs / DeepMind) | `2603.01608` | **Yes** | Decomposes scheming into agent + environmental factors. Finds scheming is brittle to scaffolding changes. Relevant to D1 taxonomy (scheming propensity vs. capability). March 2026, very recent. |
| 5 | DecepChain: Inducing Deceptive Reasoning in LLMs (Shen et al., UIUC) | `2510.00319` | **Yes** | Backdoor attack that induces plausible-looking but deceptive CoT via GRPO. Creates traces where deceptive reasoning is indistinguishable from benign. Relevant to D1 as a method for generating unfaithful traces. Has code + model artifacts. |
| 6 | DeepMind: Evaluating and Monitoring for AI Scheming (Krakovna et al.) | N/A (blog) | No | Blog summary of DeepMind's approach; the underlying papers are already tracked or are position pieces |
| 7 | Stress Testing Deliberative Alignment for Anti-Scheming Training (Apollo) | N/A (report) | No | Companion to the OpenAI/Apollo paper above; same study, different writeup |

## Search 3: "CoT faithfulness evaluation benchmark 2025 2026"

| # | Title | arXiv ID | Include? | Reason |
|---|-------|----------|----------|--------|
| 1 | FaithCoT-Bench (Shen et al.) | `2510.04040` | No | Already in master table |
| 2 | Investigating CoT Monitorability in Large Reasoning Models (Yang et al.) | `2511.08525` | No | Already in master table |
| 3 | Examining the Faithfulness of DeepSeek R1's CoT Reasoning (Cornish & Rogers, CHOMPS 2025 workshop) | N/A (ACL Anthology) | **Yes** | Probes DeepSeek R1 with 445 logical puzzles. Key finding: R1 acknowledges harmful hints 94.6% of the time but reports <2% of helpful hints. Demonstrates implicit unfaithfulness via reduced answer-rechecking for helpful hints. Has code + data. Directly relevant to cue-mention faithfulness. |
| 4 | Enabling Reasoning Language Models to Reveal Their True Thoughts via CoT Inversion (anonymous, ICLR 2026 under review) | N/A (OpenReview) | **Yes** | Uses variational inference (EM algorithm) to infer latent "true" CoT and compare with generated CoT. Proposes a quantitative faithfulness metric based on agreement between inferred and articulated reasoning. Novel methodology relevant to D1 evaluation. |
| 5 | variCoT: A Unified Variational Framework for Implicit Chain-of-Thought Reasoning (anonymous, ICLR 2026 under review) | N/A (OpenReview) | No | Efficiency-focused latent reasoning framework; not about faithfulness or safety |
| 6 | DC-CoT: Data-Centric Benchmark for CoT Distillation (anonymous, ICLR 2026 under review) | N/A (OpenReview) | No | Distillation benchmark, no faithfulness or safety relevance |
| 7 | Are DeepSeek R1 and Other Reasoning Models More Faithful? (Chua & Evans) | `2501.08156` | No | Already in master table |

## Summary
- **6 new papers/resources found** (not previously in master table)
- **Papers with trace examples:**
  - OpenAI/Apollo scheming report + antischeming.ai/snippets (curated CoT snippets showing deceptive reasoning in o3, o4-mini, Gemini 2.5 Pro, Claude Opus 4)
  - DecepChain (`2510.00319`) -- generated deceptive traces with code
  - Cornish & Rogers (CHOMPS 2025) -- 445 logical puzzle traces with faithfulness annotations, code + data on GitHub
  - ReasoningFlow (`2506.02532`) -- annotated trace structures with DAG schema
- **Recommended for D1 definitions/examples:**
  - antischeming.ai/snippets -- real scheming CoT examples from frontier models, categorized by type (explicit deception, eval awareness, etc.)
  - DecepChain -- method for generating unfaithful traces that look faithful (potential synthetic pipeline)
  - Cornish & Rogers -- clean experimental setup for cue-mention faithfulness in DeepSeek R1
  - CoT Inversion (OpenReview) -- novel faithfulness metric we could adopt or cite

### New papers detail

| # | Title | ID | Year | D1 relevance | Has trace examples? |
|---|-------|-----|------|-------------|---------------------|
| 1 | ReasoningFlow: Semantic Structure of Complex Reasoning Traces | `2506.02532` | 2025 | medium | Yes (annotated DAGs, annotation tool) |
| 2 | OpenAI/Apollo: Detecting and Reducing Scheming | antischeming.ai | 2025 | high | Yes (curated CoT snippets) |
| 3 | Scheming Propensity in LLM Agents (Hopman et al.) | `2603.01608` | 2026 | medium | Yes (scheming traces in appendix) |
| 4 | DecepChain: Inducing Deceptive Reasoning | `2510.00319` | 2025 | high | Yes (deceptive vs. benign CoTs, code) |
| 5 | DeepSeek R1 CoT Faithfulness (Cornish & Rogers) | CHOMPS 2025 | 2025 | high | Yes (445 puzzles, code + data) |
| 6 | CoT Inversion (anonymous) | ICLR 2026 sub. | 2025 | medium | No (methodology/metric paper) |
