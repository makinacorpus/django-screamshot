import logging
import base64
from StringIO import StringIO

from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext as _

from utils import casperjs_capture


logger = logging.getLogger(__name__)


def capture(request):
    # Merge both QueryDict into dict
    parameters = dict([(k,v) for k,v in request.GET.items()])
    parameters.update(dict([(k,v) for k,v in request.POST.items()]))

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

    size_str = parameters.get('size', '0x0')
    try:
        img_width_str, img_height_str = size_str.lower().split('x')
    except ValueError:
        size = None
    else:
        try:
            img_width = int(img_width_str)
        except ValueError:
            img_width = None
        try:
            img_height = int(img_height_str)
        except ValueError:
            img_height = None
        size = img_width, img_height
        if not any(size):
            size = None

    try:
        validate = URLValidator()
        validate(url)
    except ValidationError:
        try:
            url = request.build_absolute_uri(reverse(url))
        except NoReverseMatch:
            raise Http404(_("Cannot reverse URL '%s'") % url)

    stream = StringIO()
    casperjs_capture(stream, url, method=method.lower(), width=width,
                     height=height, selector=selector, data=data,
                     size=size, waitfor=waitfor)
    if render == "html":
        response = HttpResponse(mimetype='text/html')
        body = """<html><body onload="window.print();"><img src="data:image/jpg;base64,%s"/></body></html>""" % base64.encodestring(stream.getvalue())
        response.write(body)
    else:
        response = HttpResponse(mimetype='image/png')
        response.write(stream.getvalue())

    return response
