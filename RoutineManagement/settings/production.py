from .base import *

DEBUG = False

ALLOWED_HOSTS = []

# Datebase
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
