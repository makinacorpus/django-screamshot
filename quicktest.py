import argparse
import os
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


class QuickDjangoTest(object):
    """
    A quick way to run the Django test suite without a fully-configured project.

    Example usage:

        >>> QuickDjangoTest('app1', 'app2')

    Based on a script published by Lukasz Dziedzia at:
    http://stackoverflow.com/questions/3841725/how-to-launch-tests-for-django-reusable-app
    """
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
    )

    def __init__(self, *args, **kwargs):
        self.apps = args
        self.run_tests()

    def run_tests(self):
        """
        Fire up the Django test suite
        """
        settings.configure(
            DEBUG = True,
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.DIRNAME, 'database.db'),
                    'USER': '',
                    'PASSWORD': '',
                    'HOST': '',
                    'PORT': '',
                }
            },
            LOGGING = {
                'version': 1,
                'formatters': {'simple': {'format': '%(levelname)s %(asctime)s %(name)s %(message)s'}},
                'handlers': {'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'}},
                'loggers': {'screamshot': {'handlers': ['console'], 'level': 'DEBUG'}}
            },
            INSTALLED_APPS = self.INSTALLED_APPS + self.apps
        )

        django.setup()

        test_runner = DiscoverRunner(verbosity=1)

        failures = test_runner.run_tests(self.apps)
        if failures: # pragma: no cover
            sys.exit(failures)

if __name__ == '__main__':
    """
    What do when the user hits this file from the shell.

    Example usage:

        $ python quicktest.py app1 app2

    """
    parser = argparse.ArgumentParser(
        usage="[args]",
        description="Run Django tests on the provided applications."
    )
    parser.add_argument('apps', nargs='+', type=str)
    args = parser.parse_args()
    QuickDjangoTest(*args.apps)
