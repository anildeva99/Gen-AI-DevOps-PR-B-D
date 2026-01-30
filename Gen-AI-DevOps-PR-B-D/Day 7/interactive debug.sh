#!/bin/bash

# Ask user for input file name
echo -n "Enter the broken deployment YAML file name (e.g., broken_deployment1.yaml): "
read INPUT_FILE

# Set output file name automatically (prefix 'fixed_')
OUTPUT_FILE="fixed_${INPUT_FILE}"

# Ensure input exists
if [ ! -f "$INPUT_FILE" ]; then
  echo "Input file $INPUT_FILE not found!"
  exit 1
fi

# Run Ollama and save output
ollama run codellama "
You are a YAML validator.
Fix the following Kubernetes YAML so it is valid.

Input YAML:
$(cat "$INPUT_FILE")

Refine:
1. Correct indentation
2. Fix spelling mistakes
3. Output only corrected YAML, no explanations
" > "$OUTPUT_FILE"

echo "Fixed YAML saved to $OUTPUT_FILE"

~
