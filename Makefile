seed:
	python manage.py loaddata fixtures/countries.json
	python manage.py loaddata fixtures/states.json
	python manage.py loaddata fixtures/cities.json
migrate:
	python manage.py migrate
migrations:
	python manage.py makemigrations

