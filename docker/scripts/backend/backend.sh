#!/bin/sh

if [ "$ENV" = "production" ]; then
    echo "Running in production mode."
    echo "Waiting for PostgreSQL to be running on: $DATABASE_HOST"

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
else
    echo "Running in development mode."
    cd server
    poetry run python3 manage.py flush --no-input
    echo "Running the migration"
    poetry run python3 manage.py makemigrations
    echo "Running the migrate"
    poetry run python3 manage.py migrate
    echo "Creating a superuser email: $DJANGO_SUPERUSER_EMAIL"
    poetry run python3 manage.py createsuperuser --noinput
fi

# Continue with the provided command or entry point
exec "$@"
