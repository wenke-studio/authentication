quick-start:
	cp .env.example server/.env
	python server/manage.py makemigrations
	python server/manage.py migrate
	python server/manage.py runserver


requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes


reset:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	rm -f server/db.sqlite3
	python server/manage.py makemigrations
	python server/manage.py migrate
