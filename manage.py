#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv

load_dotenv()


def main():
    """Run administrative tasks."""
    # Getting the environment variable
    env = os.environ.get('DJANGO_ENV', 'dev')

    if env == 'prod':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'missions.settings.prod')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'missions.settings.dev')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
