import logging
import base64
from StringIO import StringIO

from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext as _

from utils import casperjs_capture


logger = logging.getLogger(__name__)


def parse_size(size_raw):
    try:
        width_str, height_str = size_raw.lower().split('x')
    except AttributeError:
        size = None
    except ValueError:
        size = None
    else:
        try:
            width = int(width_str)
            width = width if width > 0 else None
        except ValueError:
            width = None
        try:
            height = int(height_str)
            height = height if height > 0 else None
        except ValueError:
            height = None
        size = width, height
        if not all(size):
            size = None
    return size


def capture(request):
    # Merge both QueryDict into dict
    parameters = dict([(k, v) for k, v in request.GET.items()])
    parameters.update(dict([(k, v) for k, v in request.POST.items()]))

    url = parameters.get('url')
    if not url:
        return HttpResponseForbidden()

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

    size_raw = parameters.get('size')
    crop = parameters.get('crop')
    size = parse_size(size_raw)

    try:
        validate = URLValidator()
        validate(url)
    except ValidationError:
        try:
            url = request.build_absolute_uri(reverse(url))
        except NoReverseMatch:
            raise Http404(_("Cannot reverse URL '%s'") % url)

    stream = StringIO()
    try:
        casperjs_capture(stream, url, method=method.lower(), width=width,
                         height=height, selector=selector, data=data,
                         size=size, waitfor=waitfor, crop=crop)
    except ImportError:
        return HttpResponseBadRequest(_('Resize not supported'))

    if render == "html":
        response = HttpResponse(mimetype='text/html')
        body = """<html><body onload="window.print();"><img src="data:image/jpg;base64,%s"/></body></html>""" % base64.encodestring(stream.getvalue())
        response.write(body)
    else:
        response = HttpResponse(mimetype='image/png')
        response.write(stream.getvalue())

    return response
