release: python manage.py migrate
web: daphne orgachat.routing:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=orgachat.settings -v2