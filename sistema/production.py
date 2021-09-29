from .settings import *

DEBUG = False

ALLOWED_HOSTS = ["progame.pythonanywhere.com", "pythonanywhere.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'progame$progame',
        'USER': 'progame',
        'PASSWORD': 'draqudu5',
        'HOST': 'progame.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'TEST': {
            'NAME': 'progame$progame_tests',
            'ENGINE': 'django.db.backends.mysql'
        }
    }
}