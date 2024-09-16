from .base import *

DEBUG = False
ADMINS = (
    ('Syed', 'syed@testpress.in'),
)


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'educa',
        'USER': 'educa',
        'PASSWORD': 'Syed@4707',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c timezone=UTC'
        }
    }
}
ALLOWED_HOSTS = ['educaproject.com', 'www.educaproject.com']

TIME_ZONE = 'UTC'
USE_TZ = True
