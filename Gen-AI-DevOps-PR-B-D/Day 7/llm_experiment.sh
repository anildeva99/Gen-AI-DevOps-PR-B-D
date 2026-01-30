#!/bin/bash

# Ask for user input
echo -n "Enter your prompt: "
read user_prompt
echo -n "Enter temperature (e.g., 0.0, 0.7, 1.2): "
read temp_value

# Debug print
echo "Running with temperature=$temp_value"
echo "Prompt: $user_prompt"

# Create a temporary Modelfile
cat > /tmp/temp_model.Modelfile <<EOL
FROM tinyllama
PARAMETER temperature ${temp_value}
EOL

# Create / overwrite model called tempmodel
ollama create tempmodel -f /tmp/temp_model.Modelfile

# Run the model with the chosen prompt
ollama run tempmodel "$user_prompt"

# Clean up
rm -f /tmp/temp_model.Modelfile

