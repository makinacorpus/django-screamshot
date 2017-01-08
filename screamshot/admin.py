
from django.contrib import admin

from .models import WebPageScreenshot
from . import app_settings

SCREAMSHOT_AS_INSTANCE = app_settings['SCREAMSHOT_AS_INSTANCE']


class WebPageScreenshotAdmin(admin.ModelAdmin):
    readonly_fields = ('screenshot_tag', 'last_updated')
    fields = [
        'url',
        'screenshot_tag',
        'last_updated',
        'title',
        'comment',
        'validity',
        'force_update',
        'never_update',
        'render',
        'viewport_width',
        'viewport_height',
        'screenshot_width',
        'screenshot_height',
        'crop',
        'css_selector',
        'method',
        'data',
        'waitfor',
    ]


if SCREAMSHOT_AS_INSTANCE:
    admin.site.register(WebPageScreenshot, WebPageScreenshotAdmin)
