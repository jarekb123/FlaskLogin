web: gunicorn webapp.app:app
init: python webapp/manage.py db init
migrate: python webapp/manage.py db migrate
release: python webapp/manage.py db upgrade