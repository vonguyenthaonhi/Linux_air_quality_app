#!/bin/bash

BASE_DIR=$(cd "$(dirname "$0")" && pwd)
echo "Chemin base: $BASE_DIR"

scripts=(
    "$BASE_DIR/../data_collector/bin/run.sh"
    "$BASE_DIR/../data_processor/bin/run.sh"
    "$BASE_DIR/../webapp/bin/run.sh"
)

for script in "${scripts[@]}"; do
    if [[ -x "$script" ]]; then
        echo "Running $script..."
        bash "$script"
    else
        echo "Skipping $script: not executable or not found"
    fi
done

echo "All scripts executed."
