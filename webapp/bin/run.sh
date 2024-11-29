#!/bin/bash

# Chemin absolu du dossier webapp
WEBAPP_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

# Aller dans le répertoire webapp/app
cd "$WEBAPP_DIR/app" || {
    echo "Erreur : Impossible d'accéder au répertoire app."
    exit 1
}

# Vérifier si Streamlit est installé
if ! command -v streamlit &> /dev/null; then
    echo "Erreur : Streamlit n'est pas installé. Veuillez l'installer avec 'pip install streamlit'."
    exit 1
fi

# Lancer app.py avec Streamlit
echo "Lancement de app.py dans app..."
python -m streamlit run app.py --server.port 8501
