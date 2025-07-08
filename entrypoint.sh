#!/bin/sh
set -e

# Attendre que la base soit disponible
while ! nc -z message-db 3306; do
  echo "Waiting for DB..."
  sleep 1
done

echo "DB is up"

# Initialiser Alembic si nécessaire
if [ ! -f migrations/alembic.ini ]; then
  echo "Initializing migrations folder"
  flask db init
fi

# Générer une migration si nécessaire
if flask db migrate -m "Automatic migration"; then
  echo "Migration generated"
fi

# Appliquer les migrations
echo "Applying migrations"
flask db upgrade

# Démarrer l'application
echo "Starting application"
exec "$@"
