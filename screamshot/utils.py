from django.utils import six
import os
import logging
import subprocess
from tempfile import NamedTemporaryFile
import json
from mimetypes import guess_type, guess_all_extensions
try:
    from urllib.parse import urljoin
except ImportError:
    # Python 2
    from urlparse import urljoin
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings


from . import app_settings


logger = logging.getLogger(__name__)


class UnsupportedImageFormat(Exception):
    pass


class CaptureError(Exception):
    pass


def casperjs_command_kwargs():
    """ will construct kwargs for cmd
    """
    kwargs = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'universal_newlines': True
    }
    phantom_js_cmd = app_settings['PHANTOMJS_CMD']
    if phantom_js_cmd:
        path = '{0}:{1}'.format(
            os.getenv('PATH', ''), os.path.dirname(phantom_js_cmd)
        )
        kwargs.update({'env': {'PATH': path}})
    return kwargs


def casperjs_command():
    """
    Determine which capture engine is specified. Possible options:
    - casperjs
    - phantomjs
    Based on this value, locate the binary of the capture engine.

    If setting <engine>_CMD is not defined, then
    look up for ``<engine>`` in shell PATH and
    build the whole capture command.
    """
    method = app_settings['CAPTURE_METHOD']
    cmd = app_settings['%s_CMD' % method.upper()]
    if cmd is None:
        sys_path = os.getenv('PATH', '').split(':')
        for binpath in sys_path:
            cmd = os.path.join(binpath, method)
            if os.path.exists(cmd):
                break
    cmd = [cmd]

    if app_settings['TEST_CAPTURE_SCRIPT']:
        try:
            proc = subprocess.Popen(cmd + ['--version'], **casperjs_command_kwargs())
            proc.communicate()
            status = proc.returncode
            assert status == 0
        except OSError:
            msg = "%s binary cannot be found in PATH (%s)" % (method, sys_path)
            raise ImproperlyConfigured(msg)
        except AssertionError:
            msg = "%s returned status code %s" % (method, status)
            raise ImproperlyConfigured(msg)

    # Add extra CLI arguments
    cmd += app_settings['CLI_ARGS']

    # Concatenate with capture script
    app_path = os.path.dirname(__file__)

    capture = app_settings['CAPTURE_SCRIPT']
    if capture.startswith('./'):
        capture = os.path.join(app_path, 'scripts', capture)

    assert os.path.exists(capture), 'Cannot find %s' % capture
    return cmd + [capture]


CASPERJS_CMD = casperjs_command()


def casperjs_capture(stream, url, method=None, width=None, height=None,
                     selector=None, data=None, waitfor=None, size=None,
                     crop=None, render='png', wait=None):
    """
    Captures web pages using ``casperjs``
    """
    if isinstance(stream, six.string_types):
        output = stream
    else:
        with NamedTemporaryFile('wb+', suffix='.%s' % render, delete=False) as f:
            output = f.name
    try:
        cmd = CASPERJS_CMD + [url, output]

        # Extra command-line options
        cmd += ['--format=%s' % render]
        if method:
            cmd += ['--method=%s' % method]
        if width:
            cmd += ['--width=%s' % width]
        if height:
            cmd += ['--height=%s' % height]
        if selector:
            cmd += ['--selector=%s' % selector]
        if data:
            cmd += ['--data="%s"' % json.dumps(data)]
        if waitfor:
            cmd += ['--waitfor=%s' % waitfor]
        if wait:
            cmd += ['--wait=%s' % wait]
        logger.debug(cmd)
        # Run CasperJS process
        proc = subprocess.Popen(cmd, **casperjs_command_kwargs())
        stdout = proc.communicate()[0]
        process_casperjs_stdout(stdout)

        size = parse_size(size)
        render = parse_render(render)

        if size or (render and render != 'png' and render != 'pdf'):
            # pdf isn't an image, therefore we can't postprocess it.
            image_postprocess(output, stream, size, crop, render)
        else:
            if stream != output:
                # From file to stream
                with open(output, 'rb') as out:
                    stream.write(out.read())
                stream.flush()
    finally:
        if stream != output:
            os.unlink(output)


def process_casperjs_stdout(stdout):
    """Parse and digest capture script output.
    """
    for line in stdout.splitlines():
        bits = line.split(':', 1)
        if len(bits) < 2:
            bits = ('INFO', bits)
        level, msg = bits

        if level == 'FATAL':
            logger.fatal(msg)
            raise CaptureError(msg)
        elif level == 'ERROR':
            logger.error(msg)
        else:
            logger.info(msg)


def image_mimetype(render):
    """Return internet media(image) type.

    >>>image_mimetype(None)
    'image/png'
    >>>image_mimetype('jpg')
    'image/jpeg'
    >>>image_mimetype('png')
    'image/png'
    >>>image_mimetype('xbm')
    'image/x-xbitmap'
    """
    render = parse_render(render)
    # All most web browsers don't support 'image/x-ms-bmp'.
    if render == 'bmp':
        return 'image/bmp'
    return guess_type('foo.%s' % render)[0]


def parse_url(request, url):
    """Parse url URL parameter."""
    try:
        validate = URLValidator()
        validate(url)
    except ValidationError:
        if url.startswith('/'):
            host = request.get_host()
            scheme = 'https' if request.is_secure() else 'http'
            url = '{scheme}://{host}{uri}'.format(scheme=scheme,
                                                  host=host,
                                                  uri=url)
        else:
            url = request.build_absolute_uri(reverse(url))
    return url


def parse_render(render):
    """Parse render URL parameter.

    >>> parse_render(None)
    'png'
    >>> parse_render('html')
    'png'
    >>> parse_render('png')
    'png'
    >>> parse_render('jpg')
    'jpeg'
    >>> parse_render('gif')
    'gif'
    """
    formats = {
        'jpeg': guess_all_extensions('image/jpeg'),
        'png': guess_all_extensions('image/png'),
        'gif': guess_all_extensions('image/gif'),
        'bmp': guess_all_extensions('image/x-ms-bmp'),
        'tiff': guess_all_extensions('image/tiff'),
        'xbm': guess_all_extensions('image/x-xbitmap'),
        'pdf': guess_all_extensions('application/pdf')
    }
    if not render:
        render = 'png'
    else:
        render = render.lower()
        for k, v in formats.items():
            if '.%s' % render in v:
                render = k
                break
        else:
            render = 'png'
    return render


def parse_size(size_raw):
    """ Parse size URL parameter.

    >>> parse_size((100,None))
    None
    >>> parse_size('300x100')
    (300, 100)
    >>> parse_size('300x')
    None
    >>> parse_size('x100')
    None
    >>> parse_size('x')
    None
    """
    try:
        width_str, height_str = size_raw.lower().split('x')
    except AttributeError:
        size = None
    except ValueError:
        size = None
    else:
        try:
            width = int(width_str)
            assert width > 0
        except (ValueError, AssertionError):
            width = None
        try:
            height = int(height_str)
            assert height > 0
        except (ValueError, AssertionError):
            height = None
        size = width, height
        if not all(size):
            size = None
    return size


def image_postprocess(imagefile, output, size, crop, render):
    """
    Resize and crop captured image, and saves to output.
    (can be stream or filename)
    """
    try:
        from PIL import Image
    except ImportError:
        import Image

    img = Image.open(imagefile)
    size_crop = None
    img_resized = img
    if size and crop and crop.lower() == 'true':
        width_raw, height_raw = img.size
        width, height = size
        height_better = int(height_raw * (float(width) /
                                          width_raw))
        if height < height_better:
            size_crop = (0, 0, width, height)

    try:
        if size_crop:
            size_better = width, height_better
            img_better = img.resize(size_better, Image.ANTIALIAS)
            img_resized = img_better.crop(size_crop)
        elif size:
            img_resized = img.resize(size, Image.ANTIALIAS)

        # If save with 'bmp' use default mode('RGBA'), it will raise:
        # "IOError: cannot write mode RGBA as BMP".
        # So, we need convert image mode
        # from 'RGBA' to 'RGB' for 'bmp' format.
        if render == 'bmp':
            img_resized = img_resized.convert('RGB')
        # Fix IOError: cannot write mode RGBA as XBM
        elif render == 'xbm':
            img_resized = img_resized.convert('1')
        # Works with either filename or file-like object
        img_resized.save(output, render)
    except KeyError:
        raise UnsupportedImageFormat
    except IOError as e:
        raise CaptureError(e)


def build_absolute_uri(request, url):
    """
    Allow to override printing url, not necessarily on the same
    server instance.
    """
    if app_settings.get('CAPTURE_ROOT_URL'):
        return urljoin(app_settings.get('CAPTURE_ROOT_URL'), url)
    return request.build_absolute_uri(url)


def render_template(template_name, context, format='png',
                    output=None, **options):
    """
    Render a template from django project, and return the
    file object of the result.
    """
    # output stream, as required by casperjs_capture
    stream = BytesIO()
    out_f = None
    # the suffix=.html is a hack for phantomjs which *will*
    # complain about not being able to open source file
    # unless it has a 'html' extension.
    with NamedTemporaryFile(suffix='.html') as render_file:
        template_content = render_to_string(
            template_name,
            context
        )
        # now, we need to replace all occurences of STATIC_URL
        # with the corresponding file://STATIC_ROOT, but only
        # if STATIC_URL doesn't contain a public URI (like http(s))
        static_url = getattr(settings, 'STATIC_URL', '')
        if settings.STATIC_ROOT and\
           static_url and not static_url.startswith('http'):
            template_content = template_content.replace(
                static_url,
                'file://%s' % settings.STATIC_ROOT
            )
        render_file.write(template_content.encode('utf-8'))
        # this is so that the temporary file actually gets filled
        # with the result.
        render_file.seek(0)

        casperjs_capture(
            stream,
            url='file://%s' % render_file.name,
            **options
        )

        # if no output was provided, use NamedTemporaryFile
        # (so it is an actual file) and return it (so that
        # after function ends, it gets automatically removed)
        if not output:
            out_f = NamedTemporaryFile()
        else:
            # if output was provided, write the rendered
            # content to it
            out_f = open(output, 'wb')
        out_f.write(stream.getvalue())
        out_f.seek(0)

        # return the output if NamedTemporaryFile was used
        if not output:
            return out_f
        else:
            # otherwise, just close the file.
            out_f.close()
