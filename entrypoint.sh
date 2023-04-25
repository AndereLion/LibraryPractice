#!/bin/bash
if  [ ! -e "./logs" ]; then
    mkdir ./logs
fi
python manage.py wait_for_db
python manage.py migrate
python manage.py collectstatic --no-input
python start_bot.py > ./logs/bot.logs 2>&1 &
celery -A library_config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler > ./logs/celery_beat.logs 2>&1 &
celery -A library_config worker -l INFO > ./logs/celery_worker.logs 2>&1 &
python manage.py runserver 0.0.0.0:8000
done