#!/bin/bash

# Définir les chemins des scripts
scripts=(
    "../data_collector/bin/run.sh"
    "../data_processor/bin/run.sh"
    "../webapp/bin/run.sh"
)

# Exécuter chaque script
for script in "${scripts[@]}"; do
    if [[ -x "$script" ]]; then
        echo "Running $script..."
        bash "$script"
    else
        echo "Skipping $script: not executable or not found"
    fi
done

echo "All scripts executed."

