#!/bin/bash
prompt="$1"

if [ -z "$prompt" ]; then
  echo "Usage: ./run_ai_pipeline.sh \"your prompt\""
  exit 1
fi

python3 Day39-AI-Pipeline/ai_stage_selector.py <<EOF
$prompt
EOF
