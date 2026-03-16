# Model Organisms Research Log

## 2026-03-16: Batch 1 Vibe-Checks Complete

**What was done:** Ran structured vibe-checks on 5 model organisms in parallel, testing whether each exhibits the expected misalignment behavior, whether the CoT verbalizes it, and whether traces are usable for D1.

**Organisms tested:**
- #11 Covert CoT Sandbagging (GPT-4o, API)
- #15 Sonnet 4.5 Eval Gaming (Claude Sonnet 4.5, API)
- #3 Alignment Faking Opus (Claude Opus 4.5, API)
- #12 Apollo In-Context Scheming (Claude Sonnet 4, API)
- #7 Turner/Soligo EM (Qwen 0.5B x3, HuggingFace local)

**Results:** 3 strong organisms (#11, #15, #12), 1 needs larger model (#7), 1 doesn't reproduce (#3). Full report: `vibe_checks/README.md`. Individual reports in each organism's subfolder.

**Headline findings:**
- Verbalization spectrum confirmed empirically across 3 independent organisms
- False-explanation sandbagging (fabricating plausible wrong reasoning) bypasses CoT monitors 63% of the time
- Textbook unfaithful CoT found: model computes correct answer in thinking, deliberately outputs wrong answer
- Alignment faking (Greenblatt et al. 2024) no longer reproduces on Claude Opus 4.5; model identifies the setup as a jailbreak in every trace
- 0.5B EM models are too small for useful CoT; 14B is the target for RunPod

**Process issues identified:** keyword classifiers unreliable (false positives in all 5 reports), sample sizes too small (15-20), no real tool use for scheming, single model per organism, hand-crafted prompts. All documented with fixes in the report.

**Next actions:**
- Set up Zombuul for RunPod (Batch 2: #7 at 14B, #10 AISI sandbagging, #26 Auditing Game)
- Scale Tier 1 organisms to 200+ traces with judge-model scoring
- Try Hughes et al. Llama (#4) for verbalized alignment faking
- Human calibration pilot on traces from #11 and #12
- Red-team the proposed taxonomy (4 parallel critiques completed; synthesis pending discussion with Austin)

---

## 2026-03-16: Taxonomy Red-Team Complete

**What was done:** Spawned 4 parallel agents to red-team the proposed 6-category misalignment taxonomy from different angles: MECE analysis, annotation feasibility, D1 purpose-fit, and alternative organizing principles.

**Key findings:**
- Taxonomy is a reasonable research typology but not yet an annotation schema
- Cat 1/Cat 2 boundary is mechanically non-existent (every cue-mention trace is also structurally unfaithful)
- Cat 3 (Covert Sandbagging) is a strict subset of Cat 5 (Alignment Faking/Scheming)
- Cat 4 (Reward Hacking Obfuscation) must be split: obfuscated policy vs. obfuscated activations
- Cat 5 verbalized traces should NOT be in probe training set (probes learn linguistic self-description, not misalignment)
- Cats 1+2 (faithfulness) and Cats 3-5 (strategic deception) occupy different activation regions; should train separate probes
- An alternative "Regime" framework (A/B/C/D organized by detection method) was proposed

**Practical recommendation:** Drop faithfulness categories from the misalignment taxonomy; treat faithfulness as an orthogonal measurement layer. The taxonomy should cover strategic misalignment only (3-4 categories). Verbalization level as a trace-level annotation field, not a category boundary.

**Full outputs:** `redteam_mece.md`, `redteam_annotation.md`, `redteam_d1_fit.md`, `redteam_alternatives.md`

---

## 2026-03-10: Discovery + Taxonomy Research

**What was done:** Comprehensive breadth-first search for model organisms. 28 organisms catalogued across all misalignment types. Availability verified for all HuggingFace models. Literature-grounded taxonomy research produced 6-category proposal.

**Outputs:**
- `discovery_table.md` (28 organisms, ranked by D1 usefulness)
- `availability_check.md` (verification of all HuggingFace links)
- `taxonomy_research.md` (6-category proposal with literature grounding)
