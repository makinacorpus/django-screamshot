try:
    # for Django 1.6 - 1.9
    from django.conf.urls import url, patterns
except ImportError:
    try:
        # for Django 1.10
        from django.conf.urls import url
    except ImportError:
        # for Django 1.5 or older
        from django.conf.urls.defaults import url, patterns

import django


from .views import capture

urlpatterns = [
    url(r'^', capture, name='capture')
]

if django.VERSION[:2] < (1, 9):
    urlpatterns = patterns('', *urlpatterns)
