import os
from .base import PROJECT_ROOT, CONTEXT_PROCESSORS, TEMPLATE_LOADERS, INSTALLED_APPS, MIDDLEWARE

SECRET_KEY = '12345'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'edusanjal',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
    'OPTIONS': {
        'debug': True,
        'context_processors': CONTEXT_PROCESSORS,
        'loaders': TEMPLATE_LOADERS,
        'string_if_invalid': '<< MISSING VARIABLE "%s" >>'}}]

ADMIN_URL = 'admin/'