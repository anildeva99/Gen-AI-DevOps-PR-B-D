#!/bin/bash
set -e

REPO="adinarayanap/Gen-AI-DevOps"
WORKFLOW_FILE="ai-orchestrator.yml"

if [ -z "$GITHUB_PAT" ]; then
  echo "❌ ERROR: GITHUB_PAT is not set"
  echo "Set it using: export GITHUB_PAT=\"your_pat_token_here\""
  exit 1
fi

echo "🚀 Triggering FULL pipeline (PR → Tests → Build → Deploy → Security Scan)"

curl -s -o /dev/null -w "%{http_code}\n" \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_PAT" \
  https://api.github.com/repos/$REPO/actions/workflows/$WORKFLOW_FILE/dispatches \
  -d '{"ref":"main"}'

echo "✅ Dispatch sent. Check GitHub Actions > ai-orchestrator.yml for progress."
