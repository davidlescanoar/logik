from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

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