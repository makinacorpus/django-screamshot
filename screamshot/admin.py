from django.contrib import admin
from .models import WebPageScreenshot


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

admin.site.register(WebPageScreenshot, WebPageScreenshotAdmin)
