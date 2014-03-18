import os

SECRET_KEY = os.getenv('SECRET_KEY', 'booh!')
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', '*')]

DEBUG = False

ROOT_URLCONF = 'screamshotter.urls'

INSTALLED_APPS = (
    'screamshot',
)

DISK_CACHE_SIZE = 50 * 1000

SCREAMSHOT_CONFIG = {
    'CLI_ARGS': ['--disk-cache=true',
                 '--max-disk-cache-size=%s' % DISK_CACHE_SIZE],
}

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {'format': '%(levelname)s %(asctime)s %(name)s %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.getenv('LOG_FILE', 'screamshotter.log'),
        },
    },
    'loggers': {
        'screamshot': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
