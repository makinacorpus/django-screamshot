from django.conf import settings
from django.contrib import admin

from .models import WebPageScreenshot

SCREAMSHOT_AS_INSTANCE = getattr(settings, 'SCREAMSHOT_AS_INSTANCE', False)


class WebPageScreenshotAdmin(admin.ModelAdmin):
    readonly_fields = ('screenshot_tag', 'last_updated')
    fields = [
        'web_site',
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
