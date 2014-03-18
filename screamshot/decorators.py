import logging

from django.contrib.auth.decorators import login_required

from . import app_settings


logger = logging.getLogger(__name__)


def login_required_capturable(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            remote_ip = request.META.get('HTTP_X_FORWARDED_FOR',
                                         request.META.get('REMOTE_ADDR', ''))
            remote_ip = remote_ip.split(',')[0]
            if remote_ip not in app_settings.get('CAPTURE_ALLOWED_IPS'):
                return login_required(view_func)(request, *args, **kwargs)
            else:
                msg = "Do not require login for %s on %s" % (remote_ip,
                                                             request.path)
                logger.debug(msg)
                return view_func(request, *args, **kwargs)
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__
        return _view

    if function:
        return _dec(function)
    return _dec
