
CMD:=poetry run
client:=cd client
server:=cd server

help:
	@echo "\n- Docker: To build and run a specific service, you can do that by executing 'make docker-up service=<service_name>'."
	@echo "\n- To run a the backend project, you can do that by executing 'make runserver'."
	@echo "\n- To run a the backend client, you can do that by executing 'make runclient'."

docker-up:
ifeq ($(service), frontend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up frontend --build -d
else ifeq ($(service), backend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up backend --build -d
else ifeq ($(service), postgres)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up postgres --build -d
else
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env up --build -d
endif

docker-down:
ifeq ($(service), frontend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down frontend
else ifeq ($(service), backend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down backend
else ifeq ($(service), postgres)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down postgres
else
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env down
endif

docker-logs:
ifeq ($(service), frontend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env logs -f frontend
else ifeq ($(service), backend)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env logs -f backend
else ifeq ($(service), postgres)
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env logs -f postgres
else
	docker compose -f ./docker/docker-compose.yml --env-file=./config/.env logs -f
endif

install:
	$(server) && poetry install
	$(server) && poetry check
	$(client) && yarn
runserver:
	$(server) && $(CMD) python3 manage.py runserver
runclient:
	$(client) && yarn && yarn dev
test:
	$(server) && $(CMD) python3 manage.py test
lint:
	$(server) && $(CMD) black .  --exclude=__init__.py
	$(server) && $(CMD) flake8 .  --exclude=__init__.py
	$(client) && yarn lint
migrate:
	$(server) && $(CMD) python3 manage.py makemigrations
	$(server) && $(CMD) python3 manage.py migrate
user:
	$(server) && $(CMD) python3 manage.py createsuperuser
data:
	$(server) && $(CMD) python3 manage.py create locations users
