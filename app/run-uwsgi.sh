#!/bin/sh 

set -e

python -m flask run --host=0.0.0.0
uwsgi --socket :5000 --workers 4 --master --enable-threads --module app:app 