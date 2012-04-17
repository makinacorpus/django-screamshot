from django.conf import settings

app_settings = dict({
    'CAPTURE_ROOT_URL': None,
    'CAPTURE_ALLOWED_IPS': ('127.0.0.1',),
}, **getattr(settings, 'SCREAMSHOT_CONFIG', {}))
