CMD:=poetry run
client=cd client
up:
	docker-compose up --build -d
install:
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install
	poetry check
runserver:
	$(CMD) python3 manage.py runserver
runclient:
	$(client) && npm install && npm run dev
test:
	$(CMD) python3 manage.py test
lint:
	$(CMD) black .
	$(CMD) flake8 .  --exclude=__init__.py
migrate:
	$(CMD) python3 manage.py migrate
migrations:
	$(CMD) python3 manage.py makemigrations
user:
	$(CMD) python3 manage.py createsuperuser
	$(CMD) python3 manage.py sqlmigrate cshr 0006
