PYTHON=venv/bin/python
MANAGE=${PYTHON} manage.py
venv: requirements.txt
	python -m venv venv
	${PYTHON} -m pip install -r requirements.txt

migrate:
	${MANAGE} makemigrations
	${MANAGE} migrate

createsuperuser:
	${MANAGE} createsuperuser

run:
	${MANAGE} runserver

bootstrap: venv migrate createsuperuser run
