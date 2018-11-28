from django.conf.urls import url

from .views import capture

urlpatterns = [
    url(r'^', capture, name='capture')
]
