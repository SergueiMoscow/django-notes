import json
import os
from pathlib import Path
from environs import Env


BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()
env.read_env(str(BASE_DIR / '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG', False)
# DOMAIN_NAME = DOMAIN_NAME

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
       'http://localhost:8000',
       'http://notes.sushkovs.com',
       'https://notes.sushkovs.ru',
       'http://192.168.10.10:8000',
)

# Application definition

INSTALLED_APPS = [
    'notes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.yandex',

    # 'whitenoise.runserver_nostatic',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap4',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'django_notes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_notes.context_processors.avatar_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_notes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# with open(os.path.join(BASE_DIR, 'db.json'), 'r') as f:
#     db_config = json.load(f)

database_schema = env('POSTGRES_SCHEMA')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'OPTIONS': {'options': f'-c search_path={database_schema}'},
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env.int('POSTGRES_PORT', 5432),
        'CONN_MAX_AGE': 300,
    },

    # Вариант с конфигом
    # 'default': db_config
    # Вариант mysql
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'OPTIONS': {
    #         'read_default_file': os.path.join(BASE_DIR, 'db.cnf'),
    #         'init_command': 'SET default_storage_engine=INNODB; \
    #             SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1',
    #         'charset': 'utf8mb4',
    #         'use_unicode': True,
    #     }
    # }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Redis:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'repo',
            # 'read:org',
            'user:email',
        ],
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
}

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# AUTH_USER_MODEL = 'notes.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
#
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')

# ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
SOCIALACCOUNT_QUERY_EMAIL = True

# for django-debug-toolbar:
INTERNAL_IPS = [
    '127.0.0.1',
    '46.188.82.8',
    '192.168.10.15',
]

# Celery
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

TELEGRAM_FILES = env('TELEGRAM_FILES')
CSRF_TRUSTED_ORIGINS = env.list('TRUSTED_ORIGINS')
