import os

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))

INSTALLED_APPS = [
    # For overriding templates
    'django.contrib.auth',
    'apps.users',

    'jet',
    'django.contrib.admin',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'versatileimagefield',
    'corsheaders',

    'apps.program',
    'apps.institute',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edusanjal.urls'

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader']

CONTEXT_PROCESSORS = [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
]

WSGI_APPLICATION = 'edusanjal.wsgi.application'

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_L10N = True
USE_TZ = True

JET_CHANGE_FORM_SIBLING_LINKS = False

CORS_ORIGIN_WHITELIST = (
    'edusanjal.com',
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'edusanjal.lib.pagination.PageNumberPagination',
    'PAGE_SIZE': 2
}
