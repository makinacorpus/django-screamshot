*django-screamshot* is a **very naive** implementation of Web pages capture
with `CasperJS <http://casperjs.org>`_ (*aaAAaah!*, `phantomjs <http://phantomjs.org>`_:))

(*See the issues pages for more details about what remains to be done.*)

Checkout `screamshotter <https://github.com/makinacorpus/django-screamshot/tree/screamshotter>`_,
the simplest Django project powered by *django-screamshot*.


=======
INSTALL
=======

First make sure you have the ``casperjs`` command in your ``PATH``, using
related `installation instructions <http://casperjs.org>`_.

Then install the egg :

::

    pip install django-screamshot


=====
USAGE
=====

* Add ``screamshot`` to your ``INSTALLED_APPS``


As a screenshot Web API
-----------------------

Add it to your project URLs :

::

    urlpatterns = patterns('',
        ...
        url(r'^capture/$',  include('screamshot.urls', namespace='screamshot', app_name='screamshot')),
    )

You can then obtain a screenshot using the following GET parameters :

url
  The website URL to capture. This can be a fully qualified URL, or the
  name of a URL to be reversed in your Django project. Note: do not forget to
  encode the url.

selector
  CSS3 selector. It will restrict the screenshot to the selected element.

method
  HTTP method to be used (*default:* ``GET``)

width
  Viewport width (*default:* ``1400``)

height
  Viewport height (*default:* ``900``)

data
  HTTP data to be posted (*default:* ``{}``)

waitfor
  CSS3 selector. The screenshot will be performed only once this selector is
  satisfied. Typical usage: if your page contains a heavy javascript processing,
  you can add a CSS class on an element when the processing is finished to make
  sure the screenshot will get the page properly rendered.

render
  If render=html, it will return an HTML page containing the image and where the
  print diaplo box will be automatically opened.

size
  Resize image (width x height, e.g: ``500x500``), need install ``PIL`` or ``Pillow``.

crop
  If ``true``, then resulting image is cropped to match specified size.

For example : http://server/capture/?url=http://django-fr.org&selector=body&width=1024&height=768&size=500x500



As a template tag
-----------------

You can include screenshots in your pages using a template tag. It will
perform the capture and return the base64 version of the resulting image.

This is very useful if you don't want to expose the capture API publicly.

::

    {% base64capture URL SELECTOR %}


For example, in a SVG template :

::

    {% load screamshot %}
    ...
    
    <image
       y="200"
       x="300"
       id="imagemap"
       xlink:href="data:{% base64capture "company:map" "#map" %}"
       width="640" />


If you run the capture server on a different instance, you can specify the 
root url for reversing (*default is local*) :

::

    SCREAMSHOT_CONFIG = {
        'CAPTURE_ROOT_URL': 'http://127.0.0.1:8001',
    }

Customizing the page rendering
------------------------------

The CasperJS script appends the `screamshot` CSS class on the `body` element.
You can easily customize the rendering for printing using this CSS marker in
your CSS stylesheet:

::

  .screamshot #navigation {
    display: none;
  }
  .screamshot #main {
    margin: 2em;
  }

Capture views with authentication
---------------------------------

You can use Basic HTTP authentication in your Django project, create a dedicated
user for screenshots and capture the full URL with credentials (``http://user:password@host/page/``).

Alternatively, you can use a specific view decorator.

Define the authorized IP to capture your pages in your settings :

::

    SCREAMSHOT_CONFIG = {
        'CAPTURE_ALLOWED_IPS': ('127.0.0.1',),
    }

And use the provided decorator : 

::

    from screamshot.decorators import login_required_capturable


    @login_required_capturable
    def your_view(request):
        ...


CasperJS command and CLI arguments
----------------------------------

By default, we look for thr CasperJS binary in the ``PATH``
environment variable (like ``which``), but you can bypass this:

::

    SCREAMSHOT_CONFIG = {
        'CASPERJS_CMD': '/home/you/Downloads/apps/capserjs',
    }


You can also specify PhantomJS/CasperJS extra-args, such as
 ``--disk-cache=true`` with the ``CLI_ARGS`` setting :

::

    SCREAMSHOT_CONFIG = {
        'CLI_ARGS': ['--disk-cache=true', '--max-disk-cache-size=30000']
    }

See related documentation on PhantomJS and CasperJS homepages.


Notes about runserver
---------------------

If you want to test it using ``manage.py runserver``, you won't be able
to capture pages coming from the same instance.

Run it twice (on two ports) and configure ``CAPTURE_ROOT_URL``.


=======
AUTHORS
=======

    * Mathieu Leplatre <mathieu.leplatre@makina-corpus.com>
    * mozillag
    * dynamicguy
    * Eric Brehault <eric.brehault@makina-corpus.com>

|makinacom|_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

=======
LICENSE
=======

    * Lesser GNU Public License
