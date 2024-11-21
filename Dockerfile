# Utiliser une image Python légère comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt pour installer les dépendances
COPY requirements.txt /app/

# Installer les dépendances Python à partir de requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du projet dans le conteneur
COPY . /app/

# Donner les droits d'exécution aux scripts shell
RUN chmod +x /app/bin/run.sh
RUN chmod +x /app/data_collector/bin/run.sh
RUN chmod +x /app/data_processor/bin/run.sh
RUN chmod +x /app/data_processor/bin/workflow.sh
RUN chmod +x /app/webapp/bin/run.sh
RUN chmod +x /app/install.sh

# Exécuter le script d'installation si nécessaire
RUN bash /app/install.sh

# Définir le point d'entrée par défaut qui exécute le script 'run.sh' du répertoire bin
CMD ["bash", "/app/bin/run.sh"]

