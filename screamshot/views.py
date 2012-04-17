import logging

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
    try:
        validate = URLValidator()
        validate(url)
    except ValidationError:
        try:
            url = request.build_absolute_uri(reverse(url))
        except NoReverseMatch:
            raise Http404(_("Cannot reverse URL '%s'") % url)

    response = HttpResponse(mimetype='image/png')
    casperjs_capture(response, url, method=method.lower(), selector=selector, data=data)
    return response
