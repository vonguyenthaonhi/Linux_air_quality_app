# Utiliser une image Python légère comme base
FROM python:3.11-slim

# Installer curl pour les téléchargements
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier uniquement requirements.txt pour installer les dépendances en premier
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du projet dans le conteneur
COPY . .

# Donner les droits d'exécution aux scripts shell en une seule commande
RUN chmod +x /app/bin/run.sh \
    /app/data_collector/bin/run.sh \
    /app/data_processor/bin/run.sh \
    /app/data_processor/bin/workflow.sh \
    /app/webapp/bin/run.sh \
    /app/install.sh

# Exécuter le script d'installation si nécessaire
RUN bash /app/install.sh

# Exposer le port 8501 (utilisé par Streamlit)
EXPOSE 5001

# Définir le point d'entrée par défaut qui exécute le script 'run.sh' du répertoire bin
CMD ["bash", "/app/bin/run.sh"]