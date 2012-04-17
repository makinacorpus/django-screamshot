from . import app_settings


class CapturableLoginRequiredMiddleware(object):
    def __init__(self):
        self.allowed_ip = app_settings.get('CAPTURE_ALLOWED_IPS')
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.META['REMOTE_ADDR'] in self.allowed_ip:
            return None
        # only required! 
        return login_required(view_func)(request, *view_args, **view_kwargs)
