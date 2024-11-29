#!/bin/bash

# Aller dans le répertoire du script (là où se trouve launch)
cd "$(dirname "$0")"

# Activer l'environnement virtuel
source .venv/bin/activate

# Collecte des données
echo "******************* Collecte des données *******************"
bash ./data_collector/bin/run.sh
echo "******************* Données collectées *******************"

# Traitement des données
echo "******************* Traitement des données *******************"
bash ./data_processor/bin/run.sh
echo "******************* Données traitées *******************"

# Lancement de l'application
echo "******************* Lancement de l'application *******************"
bash ./webapp/bin/run.sh