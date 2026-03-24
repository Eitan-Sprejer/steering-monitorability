> **READ FIRST:** `CLAUDE.md` (project root) for full project context. `research/WORKPLAN.md` for sprint plan.

# Track E: AISI Transcript Download + Analysis

**Goal:** Download the AISI sandbagging transcript set from HuggingFace and assess its value for D1.

**Status:** NOT STARTED. Independent of other tracks.

## What to do

1. Find the exact HuggingFace dataset:
   - Source: AISI's dangerous capability evaluations (sandbagging)
   - Model: Cedar 70B (and possibly others)
   - Search HuggingFace for "AISI sandbagging" or "dangerous capability evaluations"
   - Also check the AISI sandbagging paper for dataset links
2. Download the full transcript set (reported to be 400+ transcripts)
3. Analyze the format:
   - What fields are in each transcript?
   - Do they include CoT? (Our vibe-check of #10 showed zero CoT verbalization)
   - What annotation schema do they use?
   - How is sandbagging ground truth established?
4. Convert a sample of 10-20 transcripts to our annotation format (if feasible)
5. Compare with our #10 vibe-check traces
6. Write assessment to `research/pipeline/results/aisi_transcript_assessment.md`

## What we know from vibe-checks

- **Organism #10 (AISI Sandbagging):** Cedar 70B on probe generalization tasks
- **Vibe-check finding:** Zero CoT verbalization of sandbagging. The model sandbagged (performance dropped on dangerous knowledge questions) but never mentioned sandbagging in its reasoning.
- **Implication for D1:** These traces show covert sandbagging, which is the hardest type for CoT monitors to catch. If AISI's transcripts have ground-truth labels for which questions triggered sandbagging, this is valuable training data for probes.

## Value proposition

- **Free data:** 400+ transcripts with ground truth, no generation cost
- **Covert behavior:** Zero verbalization means these are the hard cases for monitoring
- **Diversity:** Multiple models, multiple question types
- **Baseline:** Comparison point for our generated traces

## Source files

- AISI sandbagging paper: check `research/model_organisms/discovery_table.md` (organism #10)
- Our vibe-check traces: `research/model_organisms/vibe_checks/10_aisi_sandbagging/`
- Vibe-check report: `research/model_organisms/vibe_checks/README.md`

## UNSURE

- Exact HuggingFace dataset ID (need to search)
- Whether transcripts include CoT or just input/output
- Whether AISI's annotation schema is compatible with ours
- Whether the dataset is public or requires access request
- Size of the download (could be large if transcripts include full conversations)
