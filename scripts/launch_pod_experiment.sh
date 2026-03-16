#!/bin/bash
# Fixed launch script for RunPod experiments via Zombuul
# Handles: private repo clone, Node.js/Claude install, non-root user, auto-pause
# Usage: Copied to pod by Zombuul, then executed via nohup

set -euo pipefail

SPEC_PATH="${1:?Usage: launch_pod_experiment.sh <spec_path>}"
REPO_URL="https://${GH_TOKEN}@github.com/Eitan-Sprejer/steering-monitorability.git"

echo "[$(date)] Starting pod experiment setup..."

# 1. Clone repo with auth (if not already cloned)
if [ ! -d /workspace/repo ]; then
    echo "[$(date)] Cloning repo..."
    git clone "$REPO_URL" /workspace/repo
else
    echo "[$(date)] Repo already exists, pulling latest..."
    cd /workspace/repo && git pull origin main
fi

# 2. Copy .env into repo
cp /tmp/.env /workspace/repo/.env 2>/dev/null || true

# 3. Install Node.js + Claude Code (if not present)
if ! command -v claude &>/dev/null; then
    echo "[$(date)] Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - >/dev/null 2>&1
    apt-get install -y nodejs >/dev/null 2>&1
    echo "[$(date)] Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code >/dev/null 2>&1
fi

# 4. Install Python deps
echo "[$(date)] Installing Python deps..."
cd /workspace/repo
pip install -r requirements.txt >/dev/null 2>&1 || true

# 5. Create non-root user (Claude Code refuses --dangerously-skip-permissions as root)
if ! id researcher &>/dev/null; then
    useradd -m -s /bin/bash researcher
    mkdir -p /etc/sudoers.d
    echo "researcher ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/researcher
    chmod 440 /etc/sudoers.d/researcher
fi

# 6. Set up Claude credentials for researcher user
mkdir -p /home/researcher/.claude
cp ~/.claude/.credentials.json /home/researcher/.claude/.credentials.json 2>/dev/null || true
echo '{}' > /home/researcher/.claude.json
chown -R researcher:researcher /home/researcher /workspace/repo
touch /workspace/research.log
chown researcher:researcher /workspace/research.log

# 7. Launch Claude Code as researcher
echo "[$(date)] Launching Claude Code for experiment: $SPEC_PATH"
su - researcher -c "cd /workspace/repo && source .env && claude --dangerously-skip-permissions --effort high -p 'Read the experiment spec at $SPEC_PATH and execute it fully. Follow the protocol exactly. Save traces as JSON, write report.md. Load API keys from .env with dotenv. When done, git checkout -b batch2-results && git add -A && git commit -m \"Batch 2 experiment results\" && git push origin batch2-results.' > /workspace/research.log 2>&1"

# 8. Auto-pause pod
echo "[$(date)] Experiment complete. Pausing pod..."
if [ -n "${RUNPOD_API_KEY:-}" ] && [ -n "${RUNPOD_POD_ID:-}" ]; then
    curl -s -H "Content-Type: application/json" \
        -d "{\"query\": \"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" \
        "https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY"
    echo "[$(date)] Pod pause requested."
else
    echo "[$(date)] WARNING: RUNPOD_API_KEY or RUNPOD_POD_ID not set. Pod will NOT auto-pause."
fi
