#!/bin/bash
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
echo "Start migrations started"

export FLASK_APP=app/app.py
export FLASK_ENV=production
export FLASK_MIGRATE="true"

if [ "$FLASK_MIGRATE" = "true" ]; then
  echo "Run migrations..."
  flask db init
  flask db migrate
  flask db upgrade
fi
echo "end migrations"
ls
python app/data_for_insert.py

exec gunicorn -b 0.0.0.0:5000 -w 4 manage:app