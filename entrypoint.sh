#!/usr/bin/env bash

echo "Control de la BBDD"
flask db upgrade

echo "Se levanta el servidor"
python3 -m flask run --host=0.0.0.0
