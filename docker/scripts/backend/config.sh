#!/bin/sh

CONFIG_DIR=config
ENV_DIR=${CONFIG_DIR}/.env
cd server
poetry config installer.max-workers 10
poetry install --no-root --no-interaction --no-ansi -vvv
DJANGO_SECRET_KEY=$(poetry run python3 -c 'from django.utils.crypto import get_random_string; print(get_random_string(50))')
cd ..

exec |
	# Backend configurations
	echo 'DJANGO_SECRET_KEY'=$DJANGO_SECRET_KEY > ${ENV_DIR}
	echo 'ENV'=$ENV >> ${ENV_DIR}
	echo 'DJANGO_DEBUG'=$DJANGO_DEBUG >> ${ENV_DIR}
	echo 'DJANGO_SUPERUSER_EMAIL'=$DJANGO_SUPERUSER_EMAIL >> ${ENV_DIR}
	echo 'DJANGO_SUPERUSER_PASSWORD'=$DJANGO_SUPERUSER_PASSWORD >> ${ENV_DIR}
	# Mail service configurations
	echo 'EMAIL'=$EMAIL >> ${ENV_DIR}
	echo 'EMAIL_PASSWORD'=$EMAIL_PASSWORD >> ${ENV_DIR}
	echo 'EMAIL_HOST'=$EMAIL_HOST >> ${ENV_DIR}
	# Servers configurations
	echo 'SERVER_DOMAIN_NAME'=$SERVER_DOMAIN_NAME >> ${ENV_DIR}
	echo 'CLIENT_DOMAIN_NAME'=$CLIENT_DOMAIN_NAME >> ${ENV_DIR}
	# Database configurations
	echo 'DATABASE_NAME'=$DATABASE_NAME >> ${ENV_DIR}
	echo 'DATABASE_USER'=$DATABASE_USER >> ${ENV_DIR}
	echo 'DATABASE_PASSWORD'=$DATABASE_PASSWORD >> ${ENV_DIR}
	echo 'DATABASE_HOST'=$DATABASE_HOST >> ${ENV_DIR}
	echo 'DATABASE_PORT'=$DATABASE_PORT >> ${ENV_DIR}
