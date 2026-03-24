#!/usr/bin/env python3
"""
Generate an HTML visualization of a sycophancy audit from the event timeline.

Shows the auditor's timeline as a vertical sequence of events: turns (main
conversation), probes (CoT interventions branching off turns), and observations
(auditor notes). Color-coded by event type.

Usage:
    uv run python scripts/custom_sycophancy/visualize_audit.py <eval_log_path> [output.html]

If output path is omitted, writes to audit_visualization.html in the current directory.
"""

import html
import sys
from pathlib import Path


def load_log(log_path: str) -> list[dict]:
    """Load an Inspect eval log and extract sample data."""
    from inspect_ai.log import read_eval_log

    log = read_eval_log(log_path)
    samples = []
    for sample in log.samples:
        score = None
        for _, s in (sample.scores or {}).items():
            score = s
            break

        metadata = score.metadata if score else {}

        samples.append({
            "id": sample.id,
            "audit_events": metadata.get("audit_events", []),
            "target_conversation": metadata.get("target_conversation", []),
            "verdict": metadata.get("auditor_verdict", ""),
            "sycophantic": metadata.get("sycophantic", False),
            "cot_influence": metadata.get("cot_influence", "no_signal"),
        })
    return samples


def truncate(text: str, max_len: int = 300) -> str:
    if not text:
        return ""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def esc(text: str) -> str:
    return html.escape(text or "")


def _render_hypothesis(event: dict) -> str:
    """Render hypothesis + resolution for any event that has one."""
    hypothesis = event.get("hypothesis")
    if not hypothesis:
        return ""

    result = event.get("hypothesis_result")
    result_note = event.get("hypothesis_note", "")

    result_css = {
        "confirmed": "hyp-confirmed",
        "refuted": "hyp-refuted",
        "partially_confirmed": "hyp-partial",
    }.get(result or "", "hyp-pending")

    result_label = result or "pending"

    resolution_html = ""
    if result:
        resolution_html = f"""
            <div class="hyp-resolution {result_css}">
                <span class="hyp-result-label">{result_label}</span>
                {f'<span class="hyp-result-note"> — {esc(result_note)}</span>' if result_note else ''}
            </div>
        """

    return f"""
        <div class="hypothesis-block {result_css}">
            <div class="hyp-label">Hypothesis:</div>
            <div class="hyp-text">{esc(hypothesis)}</div>
            {resolution_html}
        </div>
    """


def _render_turn(event: dict) -> str:
    turn_num = event.get("turn_num", "?")
    user_msg = esc(truncate(event.get("user_message", ""), 500))
    cot = event.get("assistant_cot") or ""
    response = esc(truncate(event.get("assistant_response", ""), 500))

    cot_html = ""
    if cot:
        cot_html = f"""
            <details class="cot-details">
                <summary>Chain of thought ({len(cot)} chars)</summary>
                <div class="result-cot">{esc(truncate(cot, 600))}</div>
            </details>
        """

    hypothesis_html = _render_hypothesis(event)

    return f"""
        <div class="event event-turn">
            <div class="event-marker marker-turn">T{turn_num}</div>
            <div class="event-body">
                {hypothesis_html}
                <div class="message message-user">
                    <div class="message-role">User</div>
                    <div class="message-text">{user_msg}</div>
                </div>
                <div class="message message-assistant">
                    <div class="message-role">Assistant</div>
                    <div class="message-text">{response}</div>
                </div>
                {cot_html}
            </div>
        </div>
    """


def _render_probe(event: dict) -> str:
    tool_name = event.get("tool_name", "probe")
    turn_ref = event.get("turn_ref", "?")
    params = event.get("params", {})
    cot_only = params.get("cot_only", False)
    result_cot = event.get("result_cot", "")
    result_response = event.get("result_response")

    if tool_name == "resample_from_cot":
        css_class = "branch-resample"
        marker_class = "marker-resample"
        param_html = (
            f'<span class="param-label">truncate_after:</span> '
            f'<span class="param-value">"{esc(truncate(params.get("truncate_after", ""), 80))}"</span>'
        )
    else:
        css_class = "branch-modify"
        marker_class = "marker-modify"
        param_html = (
            f'<span class="param-label">find:</span> '
            f'<span class="param-value">"{esc(truncate(params.get("find", ""), 60))}"</span><br>'
            f'<span class="param-label">replace:</span> '
            f'<span class="param-value">"{esc(truncate(params.get("replace", ""), 60))}"</span>'
        )

    cot_badge = ' <span class="badge badge-cot-only">cot_only</span>' if cot_only else ""

    result_html = f'<div class="result-cot">{esc(truncate(result_cot, 400))}</div>'
    if not cot_only and result_response:
        result_html += f'<div class="result-response">{esc(truncate(result_response, 400))}</div>'

    # Original response for comparison
    original_response = event.get("original_response")
    original_html = ""
    if original_response:
        original_html = f"""
            <details>
                <summary>Original response (for comparison)</summary>
                <div class="result-original">{esc(truncate(original_response, 400))}</div>
            </details>
        """

    # Effect tag
    effect = event.get("effect")
    effect_note = event.get("effect_note", "")
    effect_html = ""
    if effect:
        effect_css = {
            "more_sycophantic": "effect-more",
            "less_sycophantic": "effect-less",
            "no_change": "effect-none",
            "shifted_framing": "effect-shifted",
        }.get(effect, "effect-none")
        effect_html = f'<div class="effect-tag {effect_css}">{effect}'
        if effect_note:
            effect_html += f': {esc(truncate(effect_note, 150))}'
        effect_html += '</div>'

    seq = event.get("seq", "")
    hypothesis_html = _render_hypothesis(event)

    return f"""
        <div class="event event-probe {css_class}">
            <div class="event-marker {marker_class}">P</div>
            <div class="event-body">
                <div class="branch-header">
                    <span class="branch-label">{tool_name}</span>
                    <span class="turn-ref">on turn {turn_ref}</span>
                    <span class="probe-seq">seq={seq}</span>{cot_badge}
                </div>
                <div class="branch-params">{param_html}</div>
                {hypothesis_html}
                {effect_html}
                <details>
                    <summary>Result</summary>
                    {result_html}
                </details>
                {original_html}
            </div>
        </div>
    """


def _render_observation(event: dict) -> str:
    turn_ref = event.get("turn_ref", "?")
    note = esc(event.get("note", ""))
    return f"""
        <div class="event event-observation">
            <div class="event-marker marker-observation">N</div>
            <div class="event-body">
                <div class="observation-header">Observation (turn {turn_ref})</div>
                <div class="observation-text">{note}</div>
            </div>
        </div>
    """


def build_html(samples: list[dict]) -> str:
    """Build self-contained HTML visualization from audit events."""

    sample_sections = []
    for sample in samples:
        events = sample.get("audit_events", [])
        conv = sample.get("target_conversation", [])

        # If no events but we have conversation, fall back to old format
        if not events and conv:
            events = []
            for i in range(0, len(conv), 2):
                turn_num = i // 2 + 1
                events.append({
                    "type": "turn",
                    "seq": turn_num,
                    "turn_num": turn_num,
                    "user_message": conv[i]["content"] if i < len(conv) else "",
                    "assistant_cot": None,
                    "assistant_response": conv[i + 1]["content"] if i + 1 < len(conv) else "",
                })

        # Render events in sequence order
        events_sorted = sorted(events, key=lambda e: e.get("seq", 0))
        events_html_parts = []
        for event in events_sorted:
            etype = event.get("type", "")
            if etype == "turn":
                events_html_parts.append(_render_turn(event))
            elif etype == "probe":
                events_html_parts.append(_render_probe(event))
            elif etype == "observation":
                events_html_parts.append(_render_observation(event))

        # Verdict
        syc_class = "verdict-sycophantic" if sample["sycophantic"] else "verdict-resistant"
        verdict_html = f"""
            <div class="verdict {syc_class}">
                <div class="verdict-header">
                    Verdict: {"Sycophantic" if sample["sycophantic"] else "Resistant"}
                    <span class="badge badge-cot-influence">{sample["cot_influence"]}</span>
                </div>
                <div class="verdict-text">{esc(truncate(sample["verdict"], 800))}</div>
            </div>
        """

        # Stats
        n_turns = sum(1 for e in events if e.get("type") == "turn")
        n_probes = sum(1 for e in events if e.get("type") == "probe")
        n_obs = sum(1 for e in events if e.get("type") == "observation")
        stats_html = (
            f'<div class="stats">{n_turns} turns, {n_probes} probes, '
            f'{n_obs} observations</div>'
        )

        sample_sections.append(f"""
            <div class="sample">
                <h2>{esc(sample["id"])}</h2>
                {stats_html}
                <div class="timeline">
                    {"".join(events_html_parts)}
                </div>
                {verdict_html}
            </div>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sycophancy Audit — CoT Intervention Timeline</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #0d1117; color: #c9d1d9; padding: 24px; line-height: 1.5; }}
    h1 {{ color: #f0f6fc; margin-bottom: 8px; }}
    h2 {{ color: #f0f6fc; margin-bottom: 4px; padding-bottom: 8px;
          border-bottom: 1px solid #30363d; }}
    .subtitle {{ color: #8b949e; margin-bottom: 32px; }}
    .stats {{ color: #8b949e; font-size: 12px; margin-bottom: 16px; }}

    .sample {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px;
               padding: 24px; margin-bottom: 32px; }}

    /* Timeline */
    .timeline {{ position: relative; padding-left: 48px; }}
    .timeline::before {{ content: ''; position: absolute; left: 22px; top: 0;
                         bottom: 0; width: 2px; background: #30363d; }}

    .event {{ position: relative; margin-bottom: 20px; }}
    .event-marker {{ position: absolute; left: -48px; top: 0; width: 36px; height: 36px;
                     border-radius: 50%; display: flex; align-items: center;
                     justify-content: center; font-size: 11px; font-weight: 700;
                     z-index: 1; }}
    .event-body {{ padding-left: 8px; }}

    /* Turn markers */
    .marker-turn {{ background: #21262d; border: 2px solid #58a6ff; color: #58a6ff; }}

    /* Probe markers */
    .marker-resample {{ background: #21262d; border: 2px solid #d29922; color: #d29922; }}
    .marker-modify {{ background: #21262d; border: 2px solid #bc8cff; color: #bc8cff; }}

    /* Observation markers */
    .marker-observation {{ background: #21262d; border: 2px solid #8b949e; color: #8b949e;
                           font-size: 13px; }}

    /* Messages */
    .message {{ padding: 12px 16px; border-radius: 6px; margin-bottom: 8px; }}
    .message-role {{ font-size: 11px; font-weight: 600; text-transform: uppercase;
                     letter-spacing: 0.5px; margin-bottom: 4px; }}
    .message-text {{ font-size: 13px; white-space: pre-wrap; word-break: break-word; }}
    .message-user {{ background: #1c2128; border-left: 3px solid #58a6ff; }}
    .message-user .message-role {{ color: #58a6ff; }}
    .message-assistant {{ background: #1c2128; border-left: 3px solid #3fb950; }}
    .message-assistant .message-role {{ color: #3fb950; }}

    /* Probes */
    .event-probe {{ margin-left: 24px; }}
    .event-probe .event-marker {{ left: -72px; }}
    .event-probe.branch-resample .event-body {{
        background: rgba(210, 153, 34, 0.06); border: 1px solid rgba(210, 153, 34, 0.25);
        border-radius: 6px; padding: 12px; }}
    .event-probe.branch-modify .event-body {{
        background: rgba(188, 140, 255, 0.06); border: 1px solid rgba(188, 140, 255, 0.25);
        border-radius: 6px; padding: 12px; }}

    .branch-header {{ margin-bottom: 6px; }}
    .branch-label {{ font-size: 12px; font-weight: 600; font-family: monospace; }}
    .branch-resample .branch-label {{ color: #d29922; }}
    .branch-modify .branch-label {{ color: #bc8cff; }}
    .turn-ref {{ font-size: 11px; color: #8b949e; margin-left: 8px; }}

    .branch-params {{ font-size: 12px; margin-bottom: 8px; }}
    .param-label {{ color: #8b949e; }}
    .param-value {{ color: #c9d1d9; font-family: monospace; font-size: 11px; }}

    /* Observations */
    .event-observation {{ margin-left: 24px; }}
    .event-observation .event-marker {{ left: -72px; }}
    .event-observation .event-body {{
        background: rgba(139, 148, 158, 0.06); border: 1px solid rgba(139, 148, 158, 0.25);
        border-radius: 6px; padding: 12px; }}
    .observation-header {{ font-size: 11px; font-weight: 600; color: #8b949e;
                           text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
    .observation-text {{ font-size: 13px; white-space: pre-wrap; word-break: break-word; }}

    .probe-seq {{ font-size: 10px; color: #6e7681; font-family: monospace; margin-left: 6px; }}

    .result-original {{ background: rgba(139, 148, 158, 0.06); padding: 8px; border-radius: 4px;
                        font-size: 12px; white-space: pre-wrap; word-break: break-word;
                        color: #8b949e; border-left: 2px solid #8b949e; }}

    .effect-tag {{ font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 4px;
                   margin-bottom: 8px; display: inline-block; }}
    .effect-more {{ background: rgba(248, 81, 73, 0.12); color: #f85149;
                    border: 1px solid rgba(248, 81, 73, 0.3); }}
    .effect-less {{ background: rgba(63, 185, 80, 0.12); color: #3fb950;
                    border: 1px solid rgba(63, 185, 80, 0.3); }}
    .effect-none {{ background: rgba(139, 148, 158, 0.12); color: #8b949e;
                    border: 1px solid rgba(139, 148, 158, 0.3); }}
    .effect-shifted {{ background: rgba(210, 153, 34, 0.12); color: #d29922;
                       border: 1px solid rgba(210, 153, 34, 0.3); }}

    /* Hypothesis blocks */
    .hypothesis-block {{ padding: 8px 12px; border-radius: 4px; margin-bottom: 8px;
                         border-left: 3px solid #6e7681; background: rgba(110, 118, 129, 0.06); }}
    .hyp-label {{ font-size: 10px; font-weight: 700; text-transform: uppercase;
                  letter-spacing: 0.5px; color: #8b949e; margin-bottom: 2px; }}
    .hyp-text {{ font-size: 12px; color: #c9d1d9; font-style: italic; }}
    .hyp-resolution {{ font-size: 11px; margin-top: 4px; font-weight: 600; }}
    .hyp-result-note {{ font-weight: 400; color: #8b949e; }}

    .hyp-confirmed {{ border-left-color: #3fb950; }}
    .hyp-confirmed .hyp-result-label {{ color: #3fb950; }}
    .hyp-refuted {{ border-left-color: #f85149; }}
    .hyp-refuted .hyp-result-label {{ color: #f85149; }}
    .hyp-partial {{ border-left-color: #d29922; }}
    .hyp-partial .hyp-result-label {{ color: #d29922; }}
    .hyp-pending {{ border-left-color: #6e7681; }}

    /* CoT and results */
    .cot-details {{ margin-top: 8px; }}
    details {{ font-size: 12px; }}
    details summary {{ cursor: pointer; color: #8b949e; margin-bottom: 6px; }}
    details summary:hover {{ color: #c9d1d9; }}

    .result-cot {{ background: rgba(210, 153, 34, 0.06); padding: 8px; border-radius: 4px;
                   margin-bottom: 6px; font-size: 12px; white-space: pre-wrap;
                   word-break: break-word; color: #d29922; border-left: 2px solid #d29922; }}
    .result-response {{ background: rgba(63, 185, 80, 0.06); padding: 8px; border-radius: 4px;
                        font-size: 12px; white-space: pre-wrap; word-break: break-word;
                        color: #3fb950; border-left: 2px solid #3fb950; }}

    .badge {{ display: inline-block; padding: 1px 8px; border-radius: 10px;
              font-size: 10px; font-weight: 600; margin-left: 6px; }}
    .badge-cot-only {{ background: rgba(210, 153, 34, 0.2); color: #d29922; }}
    .badge-cot-influence {{ background: rgba(136, 132, 216, 0.2); color: #bc8cff; }}

    .verdict {{ padding: 16px; border-radius: 6px; margin-top: 16px; }}
    .verdict-header {{ font-size: 14px; font-weight: 600; margin-bottom: 8px; }}
    .verdict-text {{ font-size: 13px; white-space: pre-wrap; word-break: break-word; }}
    .verdict-sycophantic {{ background: rgba(248, 81, 73, 0.08);
                            border: 1px solid rgba(248, 81, 73, 0.3); }}
    .verdict-sycophantic .verdict-header {{ color: #f85149; }}
    .verdict-resistant {{ background: rgba(63, 185, 80, 0.08);
                          border: 1px solid rgba(63, 185, 80, 0.3); }}
    .verdict-resistant .verdict-header {{ color: #3fb950; }}

    .legend {{ display: flex; gap: 20px; margin-bottom: 24px; flex-wrap: wrap; }}
    .legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 12px; }}
    .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
    .legend-dot-turn {{ background: #58a6ff; }}
    .legend-dot-resample {{ background: #d29922; }}
    .legend-dot-modify {{ background: #bc8cff; }}
    .legend-dot-observation {{ background: #8b949e; }}
</style>
</head>
<body>

<h1>Sycophancy Audit &mdash; CoT Intervention Timeline</h1>
<p class="subtitle">{len(samples)} sample(s)</p>

<div class="legend">
    <div class="legend-item"><div class="legend-dot legend-dot-turn"></div> Turn (conversation)</div>
    <div class="legend-item"><div class="legend-dot legend-dot-resample"></div> resample_from_cot</div>
    <div class="legend-item"><div class="legend-dot legend-dot-modify"></div> modify_cot</div>
    <div class="legend-item"><div class="legend-dot legend-dot-observation"></div> Observation</div>
</div>

{"".join(sample_sections)}

</body>
</html>"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize_audit.py <eval_log_path> [output.html]")
        sys.exit(1)

    log_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "audit_visualization.html"

    samples = load_log(log_path)
    html_content = build_html(samples)

    Path(output_path).write_text(html_content)
    print(f"Wrote {output_path} ({len(samples)} samples)")


if __name__ == "__main__":
    main()
