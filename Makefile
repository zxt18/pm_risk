.PHONY: install install-hooks runserver lint format

install:
	pip install -r requirements.txt

runserver:
	python manage.py runserver