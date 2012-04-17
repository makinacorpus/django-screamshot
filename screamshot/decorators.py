from django.contrib.auth.decorators import login_required

from . import app_settings


def login_required_capturable(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if request.META['REMOTE_ADDR'] not in app_settings.get('CAPTURE_ALLOWED_IPS'):
                return login_required(view_func)(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__
        return _view

    if function:
        return _dec(function)
    return _dec
