#!/bin/bash

# build cassandra
python manage.py --config=configs.docker_compose sync_db

# run sanic
gunicorn -c configs/gunicorn.py --worker-class sanic.worker.GunicornWorker app.server:app
