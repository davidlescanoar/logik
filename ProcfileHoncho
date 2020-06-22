web: gunicorn logik.wsgi
worker: celery -A logik worker -l info
celery_beat: celery -A logik beat -l info