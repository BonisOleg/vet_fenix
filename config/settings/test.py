from .base import *  # noqa: F403

SECRET_KEY = 'test-secret-key'
DEBUG = False
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

STORAGES['staticfiles'] = {  # noqa: F405
    'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
}
