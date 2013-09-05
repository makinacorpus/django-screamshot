import logging
import base64
from StringIO import StringIO

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext as _

from utils import casperjs_capture, CaptureError, UnsupportedImageFormat
from utils import image_mimetype


logger = logging.getLogger(__name__)


def capture(request):
    # Merge both QueryDict into dict
    parameters = dict([(k, v) for k, v in request.GET.items()])
    parameters.update(dict([(k, v) for k, v in request.POST.items()]))

    url = parameters.get('url')
    if not url:
        return HttpResponseBadRequest(_('Missing url parameter'))

    method = parameters.get('method', request.method)
    selector = parameters.get('selector')
    data = parameters.get('data')
    waitfor = parameters.get('waitfor')
    render = parameters.get('render', 'png')

    try:
        width = int(parameters.get('width', ''))
    except ValueError:
        width = None
    try:
        height = int(parameters.get('height', ''))
    except ValueError:
        height = None

    size = parameters.get('size')
    crop = parameters.get('crop')

    try:
        validate = URLValidator()
        validate(url)
    except ValidationError:
        try:
            url = request.build_absolute_uri(reverse(url))
        except NoReverseMatch:
            error_msg = _("URL '%s' invalid (could not reverse)") % url
            return HttpResponseBadRequest(error_msg)

    stream = StringIO()
    try:
        casperjs_capture(stream, url, method=method.lower(), width=width,
                         height=height, selector=selector, data=data,
                         size=size, waitfor=waitfor, crop=crop, render=render)
    except CaptureError as e:
        return HttpResponseBadRequest(e)
    except ImportError:
        error_msg = _('Resize not supported (PIL not available)')
        return HttpResponseBadRequest(error_msg)
    except UnsupportedImageFormat:
        error_msg = _('Unsupported image format: %s' % render)
        return HttpResponseBadRequest(error_msg)

    if render == "html":
        response = HttpResponse(mimetype='text/html')
        body = """<html><body onload="window.print();">
                <img src="data:image/png;base64,%s"/></body></html>
                """ % base64.encodestring(stream.getvalue())
        response.write(body)
    else:
        response = HttpResponse(mimetype=image_mimetype(render))
        response.write(stream.getvalue())

    return response
