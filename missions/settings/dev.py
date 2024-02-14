from django.core.management.utils import get_random_secret_key

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0']

SECRET_KEY = get_random_secret_key()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'


