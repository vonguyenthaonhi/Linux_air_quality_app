#!/bin/bash

# URL des données
URL="https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/openaq/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

# Chemin de destination
OUTPUT_PATH="../../openaq_data.csv"

# Vérifier si le chemin de destination est accessible
if [ ! -d "$(dirname "$OUTPUT_PATH")" ]; then
    echo "Erreur : Le répertoire $(dirname "$OUTPUT_PATH") n'existe pas."
    exit 1
fi

# Télécharger les données avec curl
echo "Téléchargement des données depuis : $URL"
curl -L -o "$OUTPUT_PATH" "$URL" || {
    echo "Erreur : Le téléchargement a échoué."
    exit 1
}

echo "Téléchargement terminé. Les données ont été enregistrées dans '$OUTPUT_PATH'."

