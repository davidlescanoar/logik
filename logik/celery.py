from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Establecer las opciones de django para la aplicación de celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logik.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

# Crear la aplicación de Celery
app = Celery('logik')

# Especificamos que las variables de configuración de Celery se encuentran
# en el fichero `settings.py` de Django.
# El parámetro namespace es para decir que las variables de configuración de
# Celery en el fichero settings empiezan por el prefijo *CELERY_*
app.config_from_object('django.conf:settings')

app.conf.beat_schedule={
    'every-5-minutes':{
        'task': 'logik.tasks.update_ranking',
        'schedule': 300
    }
}

"""
app.conf.beat_schedule={
    'every-15-seconds':{
        'task': 'logik.tasks.update_ranking',
        'schedule': 15
    }
}
"""

# Este método auto-registra las tareas para el broker. 
# Busca tareas dentro de todos los archivos `tasks.py` que haya en las apps
# y las envía a Redis automáticamente.
app.autodiscover_tasks(settings.INSTALLED_APPS)