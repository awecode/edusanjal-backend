import os
from .base import PROJECT_ROOT, CONTEXT_PROCESSORS, TEMPLATE_LOADERS

ALLOWED_HOSTS = ['edusanjal.com', 'api.edusanjal.com', 'uat.edusanjal.com']
# STATIC_URL = 'https://cdn.awecode.com/ead/'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '..', 'media')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '..', 'static')
MEDIA_URL = '/media/'

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
                            {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }, ]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
    'OPTIONS': {
        'debug': False,
        'context_processors': CONTEXT_PROCESSORS,
        'loaders': [('django.template.loaders.cached.Loader', TEMPLATE_LOADERS)],
        'string_if_invalid': ''}}]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 25
EMAIL_USE_TLS = True