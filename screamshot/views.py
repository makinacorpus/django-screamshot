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


def get_tile_coords(img_width, img_height, tiling_width, tiling_height):

    tile_coords = []

    width_ratio = (img_width - 1) / tiling_width + 1

    processed_height = 0

    while processed_height < img_height:

        for i in range(width_ratio):
            new_coords = (i * tiling_width, processed_height)
            tile_coords.append(new_coords)

        processed_height += tiling_height

    return tile_coords


def convert_to_int_if_possible(value):

    try:
        converted_value = int(value)
    except ValueError:
        converted_value = None

    return converted_value


def get_tiling_markup(stream, img_width, img_height,
                      tiling_width, tiling_height):

    tile_coords = get_tile_coords(img_width, img_height,
                                  tiling_width, tiling_height)

    body = """
        <html>
            <head>
                <style type="text/css">
                    .tile {
                        overflow: hidden;
                        width:%spx;
                        height:%spx;
                        position: relative;
                        border: 1px solid gray;
                    }
                    .page-number {
                        position: absolute;
                        top: 0;
                        right: 0;
                    }
                    .break {
                        page-break-after: always;
                    }
                </style>
            </head>
        <body onload="window.print();">""" % (tiling_width, tiling_height)

    for i, coords in enumerate(tile_coords):

        body += """<div class="tile break">
                        <img src="data:image/png;base64,%s"
                        style="position:absolute;
                               top:-%spx;
                               left:-%spx;"/>
                        <div class="page-number"><span>%s/%s</span></div>
                   </div>""" % (base64.encodestring(stream.getvalue()),
                                coords[1],
                                coords[0],
                                i + 1,
                                len(tile_coords))

    body += '</body></html>'

    return body


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

    width = convert_to_int_if_possible(parameters.get('width', ''))
    height = convert_to_int_if_possible(parameters.get('height', ''))
    tiling_width = convert_to_int_if_possible(
        parameters.get('tiling_width', None))
    tiling_height = convert_to_int_if_possible(
        parameters.get('tiling_height', None))

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

        try:
            from PIL import Image
        except ImportError:
            import Image

        # Getting img size
        stream.seek(0)
        img = Image.open(stream)
        img_width, img_height = img.size

        # We are in tiling mode only if tiling parameters are present
        # AND img width is bigger than tiling width
        if tiling_width and tiling_height and img_width > tiling_width:
            body = get_tiling_markup(stream, img_width, img_height,
                                     tiling_width, tiling_height)
        else:
            body = """<html><body onload="window.print();">
                <img src="data:image/png;base64,%s"/></body></html>
                """ % base64.encodestring(stream.getvalue())
        response.write(body)
    else:
        response = HttpResponse(mimetype=image_mimetype(render))
        response.write(stream.getvalue())

    return response
