#!/bin/bash

# Récupérer le répertoire du script principal
BASE_DIR=$(cd "$(dirname "$0")" && pwd)
echo "Chemin base: $BASE_DIR"


# Liste des chemins des scripts à exécuter
scripts=(
    "$BASE_DIR/../data_collector/bin/run.sh"
    "$BASE_DIR/../data_processor/bin/run.sh"
    "$BASE_DIR/../webapp/bin/run.sh"
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
