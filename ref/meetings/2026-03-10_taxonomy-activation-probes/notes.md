# Meeting Notes: 2026-03-10
**Attendees:** Austin, Eitan
**Topic:** Taxonomy, activation probes, D1 probe design insight

---

**Taxonomy:**
- Austin's 5-category taxonomy (CoT Faithfulness, Sandbagging, Reward Hacking, Eval Awareness, Deception/Obfuscation) was arbitrary -- not grounded in prior literature
- Agreed: worth building a more principled taxonomy of misalignment modes, grounded in existing literature, for use in the paper
- May find existing literature that already proposes one; the current taxonomy may end up being fine

**Dataset + probe design (key insight):**
- D1 goal: large dataset of misaligned reasoning traces + classification paper using activation probes
- Probes are **activation probes** (not text classifiers) -- this matters for dataset composition
- Problem: if D1 only has verbalized misalignment (CoT explicitly says "I'm sandbagging"), probes trained on it will learn to detect verbal disclosure, not actual misalignment -- won't generalize to covert cases
- Solution: when gathering traces, also use **output-only monitors** to collect traces where the model is misaligned behaviorally but the CoT doesn't mention it -- non-verbalized misalignment traces
- Some categories (e.g., deception) may not be tractable at sentence level

**Second paper framing (D2):**
- Have D1 dataset -- how can we steer models to produce better (more monitorable) CoT?
- Would benefit from contrastive pairs (verbalized vs. non-verbalized misalignment), but not strictly necessary
- Edit approach: could edit the misaligned part of a reasoning trace but keep the misaligned output -- synthetic non-verbalized traces, but "kinda OOD" (the edited trace wouldn't reflect how a model naturally reasons when not verbalizing)

**Other notes:**
- MALT is not always "in the wild" (not purely naturally occurring)
- Won't be able to do sentence-level annotations for every category
- Ask Iván for agentic collaborative research tips
- Review Austin's PRs to stay up-to-date
