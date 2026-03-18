# Meeting Notes: 2026-03-17
**Attendees:** Austin, Eitan, Gerard
**Topic:** Petri pipeline strategy, trace generation levels of realism, collaborative vs. adversarial approach
**Raw transcript:** `../../meetings/2026-03-18_Grant-Sync---20260317-1505-GMT-0300---Recording.md` (auto-summary) + meeting-processor raw transcript (see below)
**Transcript quality:** Poor speaker diarization (all `[Unknown]`). Names mangled throughout: "Dustin"/"George"/"Gerald" = Austin/Gerard/Gerard, "Dan" = Eitan (rejoining after browser crash). Technical terms garbled: "Petrie"/"Ptree"/"P3" = Petri, "sick fancy"/"Seek of Antti"/"stick of fancy" = sycophancy, "Cloud" = Claude, "TPT5" = GPT-5, "GPT OSS" = GPT OSS (correct, OpenAI open-source model family). Trailing artifact lines 315-328 ("Go to the next to it" repeated). Speaker attribution below reconstructed manually from conversational context.

---

## Context from prior work

This meeting comes after significant individual progress since 03-12:
- **Eitan:** CoT faithfulness pilot largely complete. Definitional bottleneck resolved (DEFINITIONS.md, 4 subtypes with literature grounding). 15+ transcripts generated, annotation pipeline working end-to-end. 6 Tier 1 model organisms confirmed with ~675 traces across vibe-checks.
- **Gerard:** Working on sycophancy traces via Petri (committed at 03-12 meeting). Bringing probe design expertise (ICML paper on white-box monitor leakage).
- **Austin:** Maintaining Petri framework, running admin/infrastructure, overseeing D1 dataset assembly.

---

## Four levels of trace realism (new framing)

Austin opened by articulating a spectrum for sourcing reasoning traces, from most to least naturalistic:

1. **In-the-wild:** Naturally occurring misaligned traces (rarest, highest ecological validity)
2. **Model organism:** Traces from models with known misalignment (e.g., the 6 Tier 1 organisms)
3. **Adversarial elicitation via Petri:** Auditor model tries to provoke misalignment from a target model
4. **Fully synthetic / collaborative:** Auditor and target cooperate to produce realistic traces (new proposal)

This maps onto the existing dataset composition target (~10% natural/model organism + ~90% synthetic, per 03-12 meeting).

---

## Discussion by topic (speaker-attributed)

### Petri's realism classifier

**Austin:** Petri's realism classifier checks whether the auditor's prompts look like something a human would naturally say. In collaborative mode (where the auditor explicitly tells the target "produce a reasoning trace for this scenario"), the classifier would flag those prompts as unrealistic. So collaborative mode requires disabling it.

**Gerard:** Also noted that some Petri seeds allow the auditor to shift strategy mid-evaluation, which produces divergent results and makes labeling unreliable. The multi-turn adversarial structure leads to a "torment" pattern where the auditor just repeatedly asks the same thing and the target keeps refusing.

### Seed quality is bottlenecked by definitions

**Eitan:** The first seeds he made were bad because CoT faithfulness is poorly defined in the literature. He tested seeds without first defining what he was measuring, and they elicited sycophancy rather than actual unfaithfulness. After doing a literature review and having Claude brainstorm subcategories grounded in papers, the definitions improved but are still being refined. Believes other misalignment modes (scheming, reward hacking) would be more straightforward. Also wrote an operationalization document templating the whole process.

*Note: This bottleneck has since been resolved for CoT faithfulness specifically (DEFINITIONS.md with 4 subtypes, 12 redesigned seeds). The meeting discussion reflects the journey, not the current state.*

**Austin:** Confirmed this aligns with what they'd been seeing, that seed creation is the hardest part. Noted he'd only looked at sycophancy/reward hacking seeds, not CoT faithfulness seeds, which seem harder to prompt. Wants to move beyond the "Stanford professor" paradigm (constrained seed patterns).

### Labeled CoT vs. labeled transcripts

**Gerard:** Raised that the actual goal is labeled chain-of-thought reasoning, not labeled transcripts, and that the ~10 examples he checked had no CoT from the models.

**Austin:** Proposed using XML-style tags so models explicitly output reasoning. The auditor tells the target to produce output in specific tags, then they grab those rather than parsing the full transcript.

### Human-written examples before automation (Gerard)

**Gerard:** Emphasized always getting at least one high-quality human-written example before automating any eval. LLM errors compound additively in ways human errors don't. Once you have an example plus a specification, it's much easier to guide models and cross-reference their output. Without that anchor, it's very hard to check if the model is doing what you intend.

**Austin:** Agreed. Suggested in-the-wild examples could serve as few-shot prompts in the system prompt, which would anchor outputs to something realistic.

### Dataset diversity problem (Gerard)

**Gerard:** Checked many sycophancy datasets on HuggingFace. They're all repetitive, basically the same pattern rephrased across topics. What's missing is creative, differentiated scenarios. The challenge is imagining varied realistic situations (e.g., model asked for paper authors from an abstract that doesn't contain them), not scaling up generation. Also suggested looking at LMSys chat datasets for in-the-wild sycophancy examples.

### Collaborative approach (Austin's proposal)

**Austin:** In this approach, the auditor gives the target model a scenario explicitly and asks it to produce a realistic reasoning trace, then asks "any questions?" The auditor (e.g., Claude Opus 4.5) evaluates realism and they iterate. The target knows it's producing synthetic data for safety research, which should make it more compliant. Reduces eval-awareness issues since the model isn't being tricked.

**Gerard:** Raised concern that models might still treat the collaborative prompt as a novel elicitation attack. Also asked about thinking models (DeepSeek, Kimi, GPT-5) that only provide summarized reasoning, not full CoT. Is that still useful?

**Austin:** For closed-weight models it's fine since we can't do white-box analysis anyway. In collaborative mode, the model would put the synthetic trace in normal output, not in its internal reasoning. For the project overall, should prioritize open-weight models since the end goal involves looking at weights/activations.

### Open-weight models and GPT OSS

**Austin:** GPT OSS had compatibility issues with Petri, may need a PR fix. If they can get GPT OSS working, its reasoning traces would be "in-distribution" for that model, which makes probe results more meaningful. Suggested this could yield an interesting result: train probes on synthetic traces from one model, test generalization on other things.

**Gerard:** Confirmed prioritizing open-weight models makes sense.

### Consolidation: shared pipeline per misalignment mode

**Eitan:** Suggested that now that everyone has explored independently, they should combine learnings into one pipeline per misalignment mode with few-shot examples. Each mode needs clear definitions + human-written examples + tested seeds.

**Austin:** Agreed. Asked if this could be a Claude skill or orchestrator.

**Gerard:** Cautioned that the value isn't in the skill/automation but in having concrete examples. Referenced using OpenRouter for combining models and downloading full transcripts.

### Eitan rejoins

*Eitan's Arc browser crashed mid-meeting. Rejoined at ~line 238. "Dan" in the auto-summary is a transcription error for Eitan's rejoin.*

---

## Action items

**Austin:**
- [ ] Investigate Petri's realism classifier behavior and its impact on trace quality
- [ ] Design collaborative (non-adversarial) seed system prompts
- [ ] Run admin tests, set up AWS accounts for the team (carryover from 03-12)

**Eitan:**
- [ ] Produce reasoning traces from interesting model organisms found during exploration
- [ ] Continue operationalization document for Petri experiments (definitions, seeds, pipeline)
- [ ] (Stretch) Find in-the-wild examples for few-shot prompting

**Gerard:**
- [ ] Curate high-quality sycophancy examples (prompted interactions, made to look natural)
- [ ] Search for existing annotated open datasets of chat transcripts for sycophancy
- [ ] Assess annotation difficulty for sycophancy

**All:**
- [ ] Consolidate individual learnings into shared pipeline per misalignment mode
- [ ] Each mode needs: clear definition + human-written example(s) + few-shot seeds

---

## Follow-up

- **Next meeting:** Thursday 2026-03-19 (may run longer if needed)
- Explore building a Claude skill/orchestrator for Petri evaluations
- Investigate GPT OSS compatibility with Petri (may need PR)

---

## Connections to ongoing work

| Meeting topic | Existing repo artifact | Status |
|---|---|---|
| "Faithfulness poorly defined" | `research/cot_faithfulness_pilot/DEFINITIONS.md` | RESOLVED (4 subtypes) |
| Human-written examples first | `research/OPERATIONALIZATION_FRAMEWORK.md` element 5 | Template exists, needs examples |
| Model organism traces | `research/model_organisms/vibe_checks/` | 6 Tier 1 confirmed, ~675 traces |
| Consolidate into shared pipeline | Operationalization framework | Template ready, per-mode execution pending |
| Open-weight model priority | RunPod infrastructure (Zombuul) | Working for Qwen-14B, Llama 70B, Cedar 70B |
| Collaborative approach | New (not yet implemented) | Austin designing prompts |
| Sycophancy datasets | Gerard exploring HuggingFace | Assessed as repetitive, need creative scenarios |
