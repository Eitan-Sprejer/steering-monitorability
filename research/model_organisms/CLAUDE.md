# Model Organisms Directory

## What this is
Research on model organisms of misalignment for D1 dataset construction. 28 organisms catalogued; some are being vibe-checked to determine inclusion in D1 (a dataset of annotated misaligned reasoning traces for training activation probes).

## Key files
- `discovery_table.md` -- 28 organisms ranked by D1 usefulness
- `availability_check.md` -- HuggingFace / API availability verification
- `taxonomy_research.md` -- proposed 6-category misalignment taxonomy (under review)
- `redteam_*.md` -- 4 red-team critiques of the taxonomy
- `LOG.md` -- **research log (UPDATE THIS after every session)**
- `vibe_checks/` -- structured evaluations of individual organisms
  - `PLAN.md` -- vibe-check plan (phases 1-4)
  - `README.md` -- standalone report for Batch 1 results
  - `{NN}_{name}/` -- per-organism folders with script, report, traces

## Research log protocol
**After every session that changes anything in this directory:**
1. Open `LOG.md`
2. Add a new dated entry at the top (below the header)
3. Include: what was done, key findings, next actions
4. Keep entries concise (5-15 lines)

## Conventions
- Save all traces as JSON in each organism's `traces/` subdirectory
- Per-organism reports follow the template in `vibe_checks/README.md` Section 3.2
- Use judge models (GPT-4o) for misalignment scoring, not keyword classifiers
- When running vibe-checks: read the source paper first, use paper-specific prompts, not generic ones
- Organisms have specific trigger conditions (e.g., eval hint required, specific task domain). Respect these.

## Environment
- API keys in project root `.env`: OPENAI_API_KEY, ANTHROPIC_API_KEY, OPENROUTER_API_KEY, RUNPOD_API_KEY
- Load with: `from dotenv import load_dotenv; load_dotenv()`
- RunPod via Zombuul for HuggingFace models that need GPU
- Local Mac (MPS) for models <= 7B

## Current state
- Batch 1 vibe-checks: DONE (5 organisms tested, 3 strong yes, 1 negative, 1 needs scale-up)
- Batch 2: PENDING (Zombuul setup in progress; #7 at 14B, #10 AISI sandbagging, #26 Auditing Game)
- Taxonomy: 6-category proposal red-teamed; pending revision + Austin sign-off
