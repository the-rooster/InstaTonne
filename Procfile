release: bash ./build.sh && python manage.py migrate
web: gunicorn --workers=5 InstaTonne.wsgi