#!/bin/bash

URL_AIR="https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/openaq/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
URL_CITIES="https://datahub.io/core/world-cities/r/world-cities.csv"


OUTPUT_PATH_AIR="../../openaq_data.csv"
OUTPUT_PATH_CITIES="../../world_cities.csv"


if [ ! -d "$(dirname "$OUTPUT_PATH_AIR")" ]; then
    echo "Erreur : Le répertoire $(dirname "$OUTPUT_PATH_AIR") n'existe pas."
    exit 1
fi

if [ ! -d "$(dirname "$OUTPUT_PATH_CITIES")" ]; then
    echo "Erreur : Le répertoire $(dirname "$OUTPUT_PATH_CITIES") n'existe pas."
    exit 1
fi


echo "Téléchargement des données de la qualité de l'air depuis : $URL_AIR"
curl -L -o "$OUTPUT_PATH_AIR" "$URL_AIR" || {
    echo "Erreur : Le téléchargement des données de qualité de l'air a échoué."
    exit 1
}

echo "Téléchargement des données de qualité de l'air terminé. Les données ont été enregistrées dans '$OUTPUT_PATH_AIR'."


echo "Téléchargement des données des villes mondiales depuis : $URL_CITIES"
curl -L -o "$OUTPUT_PATH_CITIES" "$URL_CITIES" || {
    echo "Erreur : Le téléchargement des données des villes mondiales a échoué."
    exit 1
}

echo "Téléchargement des données des villes mondiales terminé. Les données ont été enregistrées dans '$OUTPUT_PATH_CITIES'."


