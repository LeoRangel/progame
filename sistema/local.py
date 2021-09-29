from .settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'progame',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST': {
            'NAME': 'progame_tests',
            'ENGINE': 'django.db.backends.mysql'
        }
    }
}