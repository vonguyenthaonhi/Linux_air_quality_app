#!/bin/bash

# Récupérer le répertoire du script principal
BASE_DIR=$(cd "$(dirname "$0")" && pwd)
echo "Chemin base: $BASE_DIR"

INSTALL_SCRIPT="$BASE_DIR/../install.sh"
echo "Chemin recherché pour install.sh : $INSTALL_SCRIPT"

if [[ -x "$INSTALL_SCRIPT" ]]; then
    echo "Running install.sh..."
    bash "$INSTALL_SCRIPT"
    if [[ $? -ne 0 ]]; then
        echo "install.sh failed. Exiting."
        exit 1
    fi
else
    echo "install.sh not found or not executable. Exiting."
    exit 1
fi

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
