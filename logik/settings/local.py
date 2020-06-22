from .base import *
import dj_database_url
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'logik',
        'USER': 'postgres_logik',
        'PASSWORD': 'oia2020',
        'HOST': 'localhost',
        'DATABASE_PORT': '5432',
    }
}
"""

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}