#!/bin/bash


WEBAPP_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

cd "$WEBAPP_DIR/app" || {
    echo "Erreur : Impossible d'accéder au répertoire app."
    exit 1
}

if ! command -v streamlit &> /dev/null; then
    echo "Erreur : Streamlit n'est pas installé. Veuillez l'installer avec 'pip install streamlit'."
    exit 1
fi

echo "@@@@@@@@@@@@@@@@ Run application... @@@@@@@@@@@@@@@@"

python -m streamlit run app.py --server.port 5001
