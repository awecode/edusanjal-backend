import os
from .base import PROJECT_ROOT, CONTEXT_PROCESSORS, TEMPLATE_LOADERS, INSTALLED_APPS, MIDDLEWARE

SECRET_KEY = '12345'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.0.143']
INTERNAL_IPS = ['127.0.0.1']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '..', 'media')
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
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

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    '127.0.0.1:3000',
    '192.168.0.143:3000'
)
