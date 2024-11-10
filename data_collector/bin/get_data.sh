#!/bin/bash

if [ ! -f "../conf/collector.conf" ]; then
    echo "Erreur : le fichier ../conf/collector.conf n'a pas été trouvé"
    exit 1
else
    echo "Le fichier ../conf/collector.conf a bien été trouvé !"
fi

# Charger les variables depuis le fichier de configuration
source ../conf/collector.conf

# Vérifier si les variables sont définies et afficher leur valeur
if [ -z "$data_id" ] || [ -z "$target_path" ]; then
    echo "Erreur : data_id ou target_path manquant dans collector.conf"
    exit 1
fi

# Télécharger les données depuis l'API en JSON
echo "Téléchargement des données en JSON..."
curl -XGET "https://public.opendatasoft.com/api/records/1.0/search/?dataset=$data_id&rows=1000" -o "$target_path/raw_data.json"
if [ $? -ne 0 ]; then
    echo "Erreur lors du téléchargement des données en JSON"
    exit 1
fi

json_file="$target_path/raw_data.json"
csv_file="$target_path/data.csv"

echo "Données JSON téléchargées avec succès."

# Trouver les en-têtes complètes (clés de référence) en identifiant le record avec le plus grand nombre de clés
reference_keys=$(jq -r '.records | map(.fields | keys) | max_by(length) | .[]' "$json_file" | sort | uniq | tr '\n' ';')

echo "Clés de référence extraites : $reference_keys"

# Préparer le fichier JSON temporaire avec les clés manquantes remplies par "NaN" et ordonnées
temp_json="$target_path/normalized_data.json"
jq --arg keys "$reference_keys" '
    # Convertir la liste de clés de référence en un tableau
    ($keys | split(";")) as $reference_keys |
    .records |= map(
        .fields as $fields |
        # Ajouter les clés manquantes et réordonner selon reference_keys
        $reference_keys | reduce .[] as $key (
            {};  # Démarrer avec un objet vide pour garder lordre
            .[$key] = if $fields[$key] then $fields[$key] else "NaN" end
        ) |
        # Remplacer fields par lobjet mis à jour ordonné
        .fields = .
    )' "$json_file" > "$temp_json"

echo "JSON normalisé avec les clés manquantes ajoutées et ordonnées."

# Extraire les en-têtes en éliminant les clés imbriquées
headers=$(echo "$reference_keys" | sed 's/;$//')

# Écrire les entêtes dans le fichier CSV
echo "$headers" > "$csv_file"

# Parcourir les enregistrements et extraire les valeurs des champs correspondants
jq -r '.records[] |
    .fields |
    to_entries |
    map(
        if .value | type == "array" then
            ("\"" + (.value | join(", ")) + "\"")  # Convertir les tableaux en chaînes séparées par des virgules, entourées de guillemets
        elif .value | type == "object" then
            ("\"" + (.value | tostring) + "\"")  # Convertir les objets en chaîne JSON, entourés de guillemets
        else
            ("\"" + (.value | tostring) + "\"")  # Envelopper toutes les autres valeurs dans des guillemets
        end
    ) | join(";")' "$temp_json" >> "$csv_file"

# Vérifier si l'opération a réussi
if [ $? -eq 0 ]; then
    echo "Données converties en CSV et enregistrées sous $csv_file"
else
    echo "Erreur lors de la conversion des données en CSV"
    exit 1
fi

# Supprimer le fichier JSON temporaire
rm "$temp_json"

