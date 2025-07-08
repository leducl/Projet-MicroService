#!/bin/sh
set -e

# Attendre que MySQL soit disponible
while ! nc -z message-db 3306; do
  echo "Waiting for MySQL..."
  sleep 1
done

echo "MySQL is up - starting application"
exec "$@"
