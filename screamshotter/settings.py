import os

SECRET_KEY = os.getenv('SECRET_KEY', 'booh!')
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', '*')]

DEBUG = False

ROOT_URLCONF = 'screamshotter.urls'

INSTALLED_APPS = (
    'screamshot',
)