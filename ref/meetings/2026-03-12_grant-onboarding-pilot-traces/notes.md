# Meeting Notes: 2026-03-12
**Attendees:** Austin, Eitan, Gerard (new collaborator)
**Topic:** Grant update, Gerard onboarding, compute, probe design, pilot traces
**Full transcript:** `transcript.md`

---

**Grant status:**
- Grant signed by all parties; CAIS should receive funding soon
- Kickoff meeting with AC research scientist (London-based) to be scheduled -- optional for Eitan/Gerard but encouraged
- Payment to Eitan/Gerard will start once CAIS receives funds; track hours + expenses in the meantime (save RunPod receipts)

**Funding breakdown:**
- ~80K GBP total grant (CAIS)
- 30K salary per person (for 2 people; Eitan part-time, Gerard hourly)
- 3K travel (conference reimbursement)
- 8K flex API credits (non-AWS)
- AWS compute: separate AC grant; requested $100K; would be fine with $70K, can make 50K work; fallback: ask Kogi Coefficient for ~$20K if needed
- AWS split: 70K by June 30, 30K after; unused funds carry over

**Infrastructure:**
- Compute for now: RunPod (save receipts for reimbursement); Austin to set up RunPod org + shared API keys
- AWS Bedrock = the main platform when credentials arrive (OpenRouter-like, Claude as judge model)
- Zombool plugin (Austin's friend at Lighthaven): spins up Claude Code instances on cloud pods, makes PRs, terminates pods; using it now; eventually need AWS version as Claude marketplace plugin

**Dataset design -- key decisions:**
- Target mix: ~10% natural/model organism + ~90% synthetic; sandbagging may be 100% synthetic
- MALT (METR): reward hacking + sandbagging; sandbagging entirely synthetic (none found in wild); reward hacking mostly synthetic
- **Auditing Games sandbagging (AISI, Gerard):** 7B model trained on sandbagging; zero verbalization in CoT -- can't tag, but good for testing probe generalization (train on verbalized traces, test on these)
- **Mesa Unmask dataset (Gerard):** multi-behavior annotation dataset; used in Gerard's ICML paper; relatively low quality (70% deception rate on 1B models implausible); strategy is sound but execution poor
- **Tim Hua's eval awareness organism:** requires "evaluation hint" in prompt to trigger; very low diversity; eval awareness measured by stylistic cue (camelCase/typing in Python, not CoT text); CoT verbalization low; leaning toward: include a few hundred traces at most, come back to it later

**Probe design -- key insights from Gerard's ICML paper:**
- White box monitors rely on textual evidence (pattern-matching suspicious word representations), not genuine internal understanding; removing those vector scores degrades probe performance
- Probes not robust to OOD perturbations (e.g., all-caps) -- low parameter count limits robustness
- Non-verbalized training generalizes "to some extent" but not reliably at low false positive rates needed for production
- **Key principle:** train and validation sets must be very different for generalization to be meaningful
- Better newer work (Google DeepMind) trains at scale across diverse examples
- Architecture matters; attention probes may be better

**Diversity / robustness checklist idea:**
- Austin: use Gerard's list of known OOD failure modes as a checklist to make sure D1 covers them

**Synthetic trace generation:**
- Petri: adversarial setup (target model tries to fool judge evaluating realism) -- more natural than MALT's prompt-then-rewrite approach
- Petri 2 introduced realism classifier to reduce eval-awareness artifacts
- Bloom: better for red-teaming evals/audits; different use case from Petri
- Petri builds on Inspect; traces viewable in Inspect viewer

**Human calibration:**
- Gerard's lesson from ICML: didn't do human calibration upfront, only addressed after peer reviews
- Plan: manually tag sentences, compare with judge model, adjust judge based on human rankings -- do this proactively

**Meeting schedule (updated):**
- Tuesdays 11am Austin / ~3pm Eitan / ~7pm Gerard
- Thursdays: same start time as Tuesdays (moved up 1hr)
- Eitan may need to leave Tuesdays at 30min mark (PhD advisor meeting 1hr before)

**Action items:**
- [ ] Austin: set up RunPod org + share API keys
- [ ] Austin: give Gerard access to test repo
- [ ] Austin: schedule AC research scientist kickoff meeting
- [ ] Austin: update Thursday meeting to same start time as Tuesday
- [ ] Austin: send Gerard Tuesday meeting invite
- [ ] Gerard: generate sycophancy traces (Petri); sentence-level tagging pilot
- [ ] Gerard: send questions about Petri setup + sycophancy type to research log Slack channel
- [ ] Gerard: share OOD failure mode checklist from ICML paper (all-caps etc.)
- [ ] Eitan: generate CoT faithfulness traces (Petri); sentence-level tagging pilot
- [ ] Eitan: vibe-check Tim Hua's eval awareness model organism; report results
- [ ] All: track hours + expenses for reimbursement

**Waiting on:**
- CAIS receiving funding (unlocks salary payments)
- AWS credentials (unlocks Bedrock setup)
- AC research scientist kickoff (Austin to schedule)
