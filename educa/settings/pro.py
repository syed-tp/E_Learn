from .base import *

DEBUG = False
ADMINS = (
    ('Syed', 'syed@testpress.in'),
)


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
ALLOWED_HOSTS = ['educaproject.com', 'www.educaproject.com', ]

TIME_ZONE = 'UTC'
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

SECRET_KEY = 'django-insecure-6i+d8k@reflw7pz#cm9_s4)3waosi5tyo^)xwjk1m(wplweiu1'
