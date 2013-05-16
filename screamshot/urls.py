from django.conf.urls import patterns, url

from views import capture


urlpatterns = patterns('screamshot.views',
    url(r'^$', capture, name='capture'),
)
