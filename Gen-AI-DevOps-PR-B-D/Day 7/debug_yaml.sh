
#!/bin/bash

INPUT_FILE="broken_deployment.yaml"
OUTPUT_FILE="fixed_deployment.yaml"

# Ensure input exists
if [ ! -f "$INPUT_FILE" ]; then
  echo "Input file $INPUT_FILE not found!"
  exit 1
fi

# Run Ollama and save output (no printing)
ollama run codellama "
You are a YAML validator.
Fix the following Kubernetes YAML so it is valid.

Input YAML:
$(cat $INPUT_FILE)

Refine:
1. Correct indentation
2. Fix spelling mistakes
3. Output only corrected YAML, no explanations
" > "$OUTPUT_FILE"

echo " Fixed YAML saved to $OUTPUT_FILE"

~
