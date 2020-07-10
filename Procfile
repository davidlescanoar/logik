web: honcho start -f ProcfileHoncho
web: gunicorn logik.wsgi
celery_beat: celery -A logik beat -l info
worker: celery -A logik worker -l info