# entrypoint.sh
python3 manage.py migrate
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000