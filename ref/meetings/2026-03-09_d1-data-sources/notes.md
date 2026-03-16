# Meeting Notes: 2026-03-09
**Attendees:** Austin, Eitan
**Topic:** D1 data sources, model organisms, infrastructure

---

**Project status:**
- Waiting for a CAIS person to sign (grant not yet finalized at this point)
- AWS credits requested: 50k through June + 50k for the rest (100k total); inference API also available via AWS
- Grant could cover both Claude Max subscriptions
- No better alternative to Petri

**D1 data sources -- three confirmed:**
1. Naturally occurring traces
2. Model organisms (misaligned model orgs -- specifically eval awareness + sandbagging)
3. Synthetic traces from Petri/BLOOM

**Model organisms:**
- Austin has been in contact with people working on model organisms
- There's an eval awareness model organism from last year -- check usefulness
- Sandbagging model organisms: worth trying too
- Vibe check approach: (a) does model pass vibe check? (b) does model verbalize the misalignment in a black-box way?
- Note: model organism misalignment may not be tractable at the sentence level

**Petri:**
- Austin has made 13k transcripts for reasoning traces using Petri
- No better alternative to Petri currently
- For annotation calibration: a web GUI would be useful

**People:**
- Gerard Boxo: possible hire, met Austin at EAG, would start somewhat soon
- Shivam Raval: mentor for SPAR project (Austin will talk to him; Eitan will also meet him)
- SPAR project + grant are complementary

**Project infrastructure:**
- Record meetings by default (transcribe + archive)
- Integrate all docs to a GitHub repo
- Google Drive forthcoming (Austin to invite Eitan)
- Austin to invite Eitan to the Petri repo
- Austin to include Eitan in his meetings

**CV reporting:**
- "Independent research on an Alignment Project grant, partly supported by UK AISI"
- Project listed on a website (Austin to send link)

**Action items:**
- [ ] Austin: include Eitan in his meetings
- [ ] Austin: invite Eitan to the Petri repo
- [ ] Austin: invite Eitan to the Google Drive
- [ ] Austin: send website where project is listed
- [ ] Eitan: read through what Petri is and what they're doing
- [ ] Eitan: find model organisms for misaligned models (eval awareness from last year + sandbagging)
- [ ] Eitan: vibe-check each model organism: does it verbalize misalignment in a black-box setting?
