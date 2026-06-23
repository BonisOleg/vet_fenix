from decouple import config

SECRET_KEY = config('SECRET_KEY', default='dev-only-insecure-key-do-not-use-in-prod')

from .base import *  # noqa: F403, E402

DEBUG = config('DEBUG', default=True, cast=bool)

STORAGES['staticfiles'] = {  # noqa: F405
    'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
}
