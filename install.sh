#!/bin/bash

# Aller dans le répertoire du script (là où se trouve install.sh)
cd "$(dirname "$0")"


python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
python3 -m pip install -r requirements.txt
