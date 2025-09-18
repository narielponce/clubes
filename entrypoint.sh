#!/bin/sh

# Esperar a la base de datos (usamos NETCAT)
if [ "$DATABASE" = "postgres" ]; then
  echo "Esperando a Postgres en $DATABASE_HOST:$DATABASE_PORT..."
  while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 0.1
  done
  echo "Postgres disponible"
fi

# Aplicar migraciones y recolectar estáticos (no hace daño si ya hecho)
python manage.py migrate --noinput
if [ "$DJANGO_COLLECTSTATIC" = "1" ]; then
  python manage.py collectstatic --noinput
fi

# Ejecutar el comando que se pase al container (p.ej. gunicorn)
exec "$@"

