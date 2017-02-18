from django.utils.encoding import python_2_unicode_compatible
import io
import imghdr
from hashlib import md5
from tempfile import NamedTemporaryFile

from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils import timezone as timebase
except ImportError:
    from datetime import datetime as timebase

from screamshot.utils import casperjs_capture

from .managers import WebPageScreenshotManager
from . import app_settings
import django

if django.VERSION >= (1, 10):
    from datetime import timedelta
else:
    from timedelta.fields import TimedeltaField


SCREENSHOT_FORMAT = (
    ('html', 'html'),
    ('jpeg', 'jpeg'),
    ('png', 'png'),
    ('gif', 'gif'),
    ('bmp', 'bmp'),
    ('tiff', 'tiff'),
    ('xbm', 'xbm'),
)

SCREAMSHOT_AS_INSTANCE = app_settings['SCREAMSHOT_AS_INSTANCE']


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        -> https://djangosnippets.org/snippets/976/
        """
        # If the filename already exists,
        # remove it as if it was a true file system
        if self.exists(name):
            self.delete(name)
        return name


@python_2_unicode_compatible
class WebPageScreenshot(models.Model):
    """Straightforward implementation of screamshots as model objects.
    in additions to fields used for screamshot.utils.casperjs_capture
    options, some sort of screenshot pictures caching is implemented in
    conjonction with the manager.
    """
    title = models.CharField(_("Title"), max_length=500)
    comment = models.TextField(_("Comment"), blank=True)
    if django.VERSION >= (1, 10):
        validity = models.PositiveIntegerField(_("Validity"), default=0, blank=True, null=True, help_text="maximum validity period in days.")
    else:
        validity = TimedeltaField(
            _("Validity"),
            blank=True,
            null=True,
            help_text="maximum validity period.")
    screenshot = models.ImageField(
        _("screenshot"),
        upload_to='screenshots/',
        storage=OverwriteStorage())
    last_updated = models.DateTimeField(
        _('last screenshot update'),
        blank=True,
        null=True)
    never_update = models.BooleanField(_("Never update"), default=False)
    force_update = models.BooleanField(_("Force update"), default=False)

    url = models.URLField(_("Target URL"))
    css_selector = models.CharField(
        _("CSS3 selector"),
        max_length=100,
        blank=True)
    method = models.CharField(
        _("Method"),
        max_length=4,
        choices=(('GET', 'GET'), ('POST', 'POST')),
        blank=False,
        default='GET')
    viewport_width = models.CharField(
        _("Viewport width"),
        max_length=4,
        blank=True)
    viewport_height = models.CharField(
        _("Viewport height"),
        max_length=4,
        blank=True)
    screenshot_width = models.CharField(
        _("Screenshot width"),
        max_length=4,
        blank=True)
    screenshot_height = models.CharField(
        _("Screenshot height"),
        max_length=4,
        blank=True)
    crop = models.BooleanField(_("Crop"), default=True)
    data = models.CharField(_("HTTP data"), blank=True, max_length=2000)
    waitfor = models.CharField(
        _("Wait for selector"),
        blank=True,
        max_length=100)
    render = models.CharField(
        _("screenshot format"),
        choices=SCREENSHOT_FORMAT,
        max_length=4,
        default='png')

    objects = WebPageScreenshotManager()

    class Meta:
        abstract = not SCREAMSHOT_AS_INSTANCE
        verbose_name = _("Web page screenshot")
        verbose_name_plural = _("Web pages screenshots")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.screenshot or self.force_update:
            self.update_screenshot(save=False)
        super(WebPageScreenshot, self).save(*args, **kwargs)

    def expired(self):
        """Return True if screenshot is expired"""
        expired = False
        if self.validity and not self.never_update:
            if django.VERSION >= (1, 10):
                expired = timebase.now() > self.last_updated + timedelta(days=self.validity)
            else:
                expired = timebase.now() > self.last_updated + self.validity
        return expired

    def update_screenshot(self, save=True):
        screenshot_file = NamedTemporaryFile()
        with io.open(screenshot_file.name, 'w+b') as stream:
            casperjs_capture(
                stream,
                self.url,
                method=self.method,
                width=self.viewport_width,
                height=self.viewport_height,
                selector=self.css_selector,
                data=self.data,
                waitfor=self.waitfor,
                size='%sx%s' % (self.screenshot_width, self.screenshot_height),
                crop=str(self.crop),
                render=self.render)

        screenshot_data = screenshot_file.read()
        file_ext = imghdr.what(screenshot_file.name)
        screenshot_file.close()
        base_filename = self.url.split('/')[2]
        base_filename = '_'.join(base_filename.split('.'))
        dig = md5(screenshot_data).hexdigest()[:8]
        base_filename = '-'.join((base_filename, dig))
        filename = '.'.join((base_filename, file_ext))

        self.screenshot = filename
        self.last_updated = timebase.now()
        self.screenshot.save(filename, ContentFile(screenshot_data), save=save)

    def screenshot_tag(self):
        ss_tag = ('<figure><img src="%s" />'
                  '<figcaption>%s -  %sx%s</figcaption>'
                  '</figure>') % (
            self.screenshot.url,
            self.screenshot.name.split('/')[-1],
            self.screenshot.width, self.screenshot.height
        )
        return ss_tag

    screenshot_tag.short_description = 'Current screenshot'
    screenshot_tag.allow_tags = True
