from django.conf import settings


app_settings = dict({
    'CAPTURE_METHOD': 'casperjs',
    'CAPTURE_SCRIPT': './capture.js',
    'CAPTURE_ROOT_URL': None,
    'CAPTURE_ALLOWED_IPS': ('127.0.0.1',),
    'CLI_ARGS': [],
    'CASPERJS_CMD': None,
    'PHANTOMJS_CMD': None,
    'SCREAMSHOT_AS_INSTANCE': False,
    'TEST_CAPTURE_SCRIPT': True,
}, **getattr(settings, 'SCREAMSHOT_CONFIG', {}))
