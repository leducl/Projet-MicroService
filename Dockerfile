# Dockerfile

# Utilise une image légère Python
FROM python:3.10-slim

# Installer netcat pour l’entrypoint
RUN apt-get update \
 && apt-get install -y --no-install-recommends netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
# - Le package Flask (dossier app/)
# - Le script principal main.py
# - Le script entrypoint.sh
COPY app /app/app
COPY app/main.py /app/main.py
COPY entrypoint.sh /app/entrypoint.sh

# Rendre entrypoint.sh exécutable
RUN chmod +x /app/entrypoint.sh

# Attendre que MySQL soit prêt, puis lancer l’app
ENTRYPOINT ["./entrypoint.sh"]

# Lancer l’application
CMD ["python", "main.py"]
