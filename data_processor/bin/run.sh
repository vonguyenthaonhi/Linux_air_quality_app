#!/bin/bash

# Se placer dans le répertoire parent du script
cd "$(dirname "$0")/.."

echo "@@@@@@@@@@@@@@@@ Processing data... @@@@@@@@@@@@@@@@"
python3 ../data_processor/core.py