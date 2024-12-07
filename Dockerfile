FROM python:3.11-slim



# Installer curl pour les téléchargements
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -R /app

# Donner les droits d'exécution aux scripts 
RUN chmod +x /app/bin/main_run.sh \
    /app/data_collector/bin/run.sh \
    /app/data_processor/bin/run.sh \
    /app/webapp/bin/run.sh \
    /app/install.sh

RUN bash /app/install.sh

# Exposer le port 5001
EXPOSE 5001

# exécute le script 'run.sh' du répertoire bin
CMD ["bash", "/app/bin/main_run.sh"]