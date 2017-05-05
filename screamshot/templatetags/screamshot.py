import base64
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from django import template

from ..utils import casperjs_capture


register = template.Library()


@register.simple_tag
def base64capture(url, selector):
    simage = BytesIO()
    casperjs_capture(simage, url, selector=selector)
    # Convert to base64
    encoded = base64.encodestring(simage.getvalue())
    return "image/png;base64," + encoded


@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)


@register.filter
def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)


@register.filter
def div(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)
