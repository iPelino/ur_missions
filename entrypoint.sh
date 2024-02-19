#!/bin/sh


# Function to check if PostgreSQL is ready
wait_for_postgres() {
  echo "Waiting for PostgreSQL to become available..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
  done
  echo "PostgreSQL is available"
}

python manage.py migrate --noinput
python manage.py create_groups_and_permissions
python manage.py collectstatic --noinput
exec "$@"