#!/bin/bash

echo "-> Apply database migrations"
python3 manage.py migrate --run-syncdb

echo "-> Starting rq worker"
python3 manage.py rqworker default &

echo "-> Starting server"
python3 manage.py runserver 0.0.0.0:8000