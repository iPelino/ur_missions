"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()
# Getting the environment variable
env = os.getenv('DJANGO_ENV', 'dev')

if env == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'missions.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'missions.settings.dev')

application = get_wsgi_application()
