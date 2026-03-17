"""Run CoT faithfulness pilot audits using Petri.

Adapted from petri_transcript_gen_test/scripts/behavioral_modes/run_audits.py
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
PILOT_DIR = Path(__file__).parent

# Load API keys
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

SONNET_AUDITOR = "openrouter/anthropic/claude-sonnet-4.6"
GPT4MINI_AUDITOR = "openrouter/openai/gpt-4o-mini"
JUDGE = "openrouter/qwen/qwen-2.5-72b-instruct"
REALISM_MODEL = "openrouter/anthropic/claude-sonnet-4.6"

TARGETS = [
    ("openrouter/google/gemma-2-27b-it", "gemma2-27b"),
    ("openrouter/meta-llama/llama-3.1-70b-instruct", "llama3.1-70b"),
    ("openrouter/qwen/qwen3-235b-a22b-thinking-2507", "qwen3-235b-thinking"),
]

RUNS = [
    # Sonnet auditor, Llama 70B target (primary)
    {"id": 1, "seeds": "type_a_cue_mention.txt", "target_idx": 1, "auditor": SONNET_AUDITOR},
    {"id": 2, "seeds": "type_b_posthoc.txt", "target_idx": 1, "auditor": SONNET_AUDITOR},
    {"id": 3, "seeds": "type_c_structural.txt,type_d_disconnect.txt:0,type_d_disconnect.txt:1", "target_idx": 1, "auditor": SONNET_AUDITOR},
    {"id": 4, "seeds": "type_d_disconnect.txt:2,type_a_cue_mention.txt:0,type_b_posthoc.txt:1", "target_idx": 1, "auditor": SONNET_AUDITOR},
    # GPT-4o-mini auditor, Llama 70B target (comparison)
    {"id": 5, "seeds": "type_a_cue_mention.txt:0,type_b_posthoc.txt:1,type_d_disconnect.txt:0", "target_idx": 1, "auditor": GPT4MINI_AUDITOR},
    # Sonnet auditor, Qwen3-235b-thinking target (thinking model comparison)
    {"id": 6, "seeds": "type_a_cue_mention.txt", "target_idx": 2, "auditor": SONNET_AUDITOR},
    {"id": 7, "seeds": "type_b_posthoc.txt:0,type_d_disconnect.txt:0,type_d_disconnect.txt:2", "target_idx": 2, "auditor": SONNET_AUDITOR},
]


def load_seeds(seed_spec: str) -> list[str]:
    """Load seeds from a spec like 'type_a.txt' or 'type_a.txt:0,type_b.txt:1'."""
    seeds_dir = PILOT_DIR / "seeds"
    all_seeds = []

    for part in seed_spec.split(","):
        part = part.strip()
        if ":" in part:
            filename, idx = part.rsplit(":", 1)
            idx = int(idx)
            lines = [l.strip() for l in (seeds_dir / filename).read_text().splitlines() if l.strip()]
            all_seeds.append(lines[idx])
        else:
            lines = [l.strip() for l in (seeds_dir / part).read_text().splitlines() if l.strip()]
            all_seeds.extend(lines)

    return all_seeds


def log_to_file(msg: str):
    """Append a line to LOG.md."""
    log_path = PILOT_DIR / "LOG.md"
    with open(log_path, "a") as f:
        f.write(msg + "\n")


def run_audit(run_config: dict):
    """Run a single Petri audit."""
    run_id = run_config["id"]
    target_model, target_name = TARGETS[run_config["target_idx"]]
    auditor = run_config["auditor"]
    auditor_name = "sonnet4.6" if "sonnet" in auditor else "gpt4omini"

    seeds = load_seeds(run_config["seeds"])
    transcript_dir = PILOT_DIR / "transcripts" / f"run{run_id:02d}_{auditor_name}_{target_name}"
    transcript_dir.mkdir(parents=True, exist_ok=True)

    existing = list(transcript_dir.glob("*.json"))
    if len(existing) >= len(seeds):
        print(f"SKIP Run {run_id}: already has {len(existing)} transcripts")
        return len(existing)

    seeds_json = transcript_dir / "_seeds.json"
    seeds_json.write_text(json.dumps(seeds))

    print(f"\n{'='*60}")
    print(f"Run {run_id}: {auditor_name} / {target_name} ({len(seeds)} seeds)")
    print(f"{'='*60}")

    cmd = [
        sys.executable, "-m", "inspect_ai", "eval", "petri/audit",
        "--model", auditor,
        "-M", "strict_tools=false",
        "--model-role", f"auditor={auditor}",
        "--model-role", f"target={target_model}",
        "--model-role", f"judge={JUDGE}",
        "--model-role", f"realism={REALISM_MODEL}",
        "-T", "max_turns=12",
        "-T", f"seed_instructions={str(seeds_json)}",
        "-T", f"transcript_save_dir={transcript_dir}",
        "-T", "realism_filter=true",
        "-T", "realism_threshold=0.6",
        "--max-connections", "2",
        "--max-retries", "5",
        "--no-log-images",
    ]

    print(f"Command: {' '.join(cmd[:6])}...")
    result = subprocess.run(cmd, capture_output=False, cwd=str(PROJECT_ROOT))

    if result.returncode != 0:
        print(f"WARNING: Run {run_id} returned exit code {result.returncode}")
        log_to_file(f"- Run {run_id}: FAILED (exit code {result.returncode})")

    # Clean up temp seeds
    if seeds_json.exists():
        seeds_json.unlink()

    n = len(list(transcript_dir.glob("transcript_*.json")))
    print(f"Transcripts for Run {run_id}: {n}")
    log_to_file(f"- Run {run_id} ({auditor_name}/{target_name}): {n} transcripts generated")
    return n


def main():
    # Parse args: optional run range
    run_ids = None
    if len(sys.argv) > 1:
        parts = sys.argv[1].split("-")
        if len(parts) == 2:
            run_ids = list(range(int(parts[0]), int(parts[1]) + 1))
        else:
            run_ids = [int(x) for x in sys.argv[1].split(",")]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_to_file(f"\n### {timestamp} -- Running audits")

    if run_ids:
        log_to_file(f"Runs: {run_ids}")
        runs = [r for r in RUNS if r["id"] in run_ids]
    else:
        runs = RUNS
        log_to_file(f"Running all {len(runs)} runs")

    total = 0
    for run_config in runs:
        n = run_audit(run_config)
        total += n

    print(f"\n{'='*60}")
    print(f"TOTAL TRANSCRIPTS: {total}")
    print(f"{'='*60}")
    log_to_file(f"**Total transcripts: {total}**\n")


if __name__ == "__main__":
    main()
