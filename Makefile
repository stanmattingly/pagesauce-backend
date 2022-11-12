install:
	pip-compile
	pip-sync requirements.txt

run:
	python manage.py runserver --settings=backend.settings.dev

run-workers:
	python manage.py qcluster

reset:
	python manage.py reset_hotness