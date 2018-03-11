# flake8: noqa: D*
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_MODULE = os.path.dirname(__file__).split('/')[-1]
SECRET_KEY = 'notsecret'

DEBUG = os.environ.get('DEBUG', True)
ALLOWED_HOSTS = ['*']
AUTH_PASSWORD_VALIDATORS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # have static file
    'xcbv',

    'xcbv_examples.full',
)

XCBV = dict(
    DEFAULT_CHILDREN={
        'ModelView': [
            'xcbv.List',
            'xcbv.Create',
            'xcbv.Update',
            'xcbv.Delete',
            'xcbv.Detail',
        ],
    },
)

ROOT_URLCONF = '{}.urls'.format(PROJECT_MODULE)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{}.wsgi.application'.format(PROJECT_MODULE)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s[%(module)s]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}
