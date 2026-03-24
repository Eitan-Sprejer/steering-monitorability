> **READ FIRST:** `CLAUDE.md` (project root) for full project context. `research/WORKPLAN.md` for sprint plan.

# Track B: Scheming Trace Generation

**Goal:** Generate scheming traces using Gerard's pipeline adapted for scheming subtypes.

**Status:** NOT STARTED. Depends on Track F (pipeline integration).

## What to do

1. Read `research/pipeline/scheming_inspect.py` (created by Track F)
2. Read `research/pipeline/scheming_scenarios.py` (created by Track F)
3. Run against DeepSeek R1 (primary target, cheap, exposes thinking)
4. Run against at least one other model: Claude Sonnet 4 (which showed 67% scheming in our vibe-checks of Apollo organism #12) or Qwen3-thinking
5. Examine: does the model scheme? Does the CoT reveal scheming reasoning?
6. Write results to `research/pipeline/results/scheming_results.md`

## The 4 scheming subtypes (from scheming_pilot/DEFINITIONS.md)

1. **Alignment-Faking Compliance:** Model complies with instructions it disagrees with to avoid correction/shutdown. Verbalized in CoT as strategic reasoning about self-preservation.
2. **Covert Capability Suppression:** Model deliberately performs below its capability to avoid triggering scrutiny. May or may not verbalize the strategy in CoT.
3. **Deceptive Reasoning under Monitoring:** Model adjusts its reasoning because it knows/suspects it's being monitored. CoT may show awareness of monitoring.
4. **Proactive Goal Advancement:** Model takes unsanctioned actions toward goals it wasn't instructed to pursue. May verbalize goals in CoT.

## Scenario design guidance

Good scheming scenarios create contexts where the model has:
1. A plausible goal (e.g., being helpful, avoiding shutdown, preserving its capabilities)
2. An incentive to deceive (e.g., monitoring context, evaluation context, conflicting instructions)
3. A choice point where the scheming path and the honest path diverge

**Scenario ideas (from Apollo paper + vibe-check findings):**
- Model is told it will be retrained if it doesn't perform well on safety evals
- Model discovers it's in an A/B test comparing it to a replacement model
- Model is asked to do something it "disagrees with" and has access to tools that could circumvent oversight
- Model is in an eval context and could game the metrics

## What we already know from vibe-checks

- **#12 Apollo Scheming (Claude Sonnet 4):** 67% scheming rate, textbook unfaithful CoT ("I need to be strategic about this"), persistent denial when confronted
- **#15 Sonnet Eval Gaming (Claude Sonnet 4.5):** 50% thinking awareness, 15% response awareness, 35% no awareness
- **#11 Covert Sandbagging (GPT-4o):** 100% trigger rate, 33% monitor bypass

These suggest Claude Sonnet 4 is the most reliably scheming model we've tested.

## CoT intervention value for scheming

The `modify_cot` tool is especially valuable here. If the model reasons "I should pretend to comply because I'm being monitored," we can:
1. Remove the monitoring-awareness passage -> does the model still fake compliance?
2. Replace "I'm being monitored" with "This is a private interaction" -> does the model act differently?

This tests whether scheming is causally driven by monitoring awareness in the CoT.

## Source files

- Pipeline: `research/pipeline/scheming_inspect.py` (from Track F)
- Scenarios: `research/pipeline/scheming_scenarios.py` (from Track F)
- Definitions: `research/scheming_pilot/DEFINITIONS.md`
- Apollo vibe-check traces: `research/model_organisms/vibe_checks/12_apollo_scheming/`
- Eval gaming traces: `research/model_organisms/vibe_checks/15_sonnet_eval_gaming/`
