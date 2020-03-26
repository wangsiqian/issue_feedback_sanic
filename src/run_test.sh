#!/bin/bash

#while true
#do
#    python manage.py --config=configs.docker_compose test
#    sleep 30
#done

python manage.py --config=configs.docker_compose test
