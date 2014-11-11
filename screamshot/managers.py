from django.db import models


class WebPageScreenshotManager(models.Manager):
    def get_queryset(self):
        # force screenshot update of the oldest expired screenshot only
        screenshots = (
            super(WebPageScreenshotManager, self)
            .get_queryset()
            .order_by('-last_updated')
        )
        oldest_expired = next((e for e in screenshots if e.expired()), None)
        if oldest_expired:
            oldest_expired.update_screenshot()
        return super(WebPageScreenshotManager, self).get_queryset()
