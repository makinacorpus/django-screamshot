*django-screamshot* is a **very naive** implementation of Web pages capture
with `CasperJS <http://casperjs.org>`_ (*aaAAaah!*, `phantomjs <http://phantomjs.org>`_:))

(*See the issues pages for more details about what remains to be done.*)


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
  name of a URL to be reversed in your Django project.

selector
  CSS3 selector (*default:* ``body``)

method
  HTTP method to be used (*default:* ``GET``)

data
  HTTP data to be posted (*default:* ``{}``)


For example : http://server/capture/?url=http://django-fr.org&selector=h1



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


Capture views with authentication
---------------------------------

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

You got it, I said it was naive :) This means you have to modify your views. 
It would be nice to make it less *sticky*...


Notes about runserver
---------------------

If you want to test it using ``manage.py runserver``, you won't be able
to capture pages coming from the same instance.

Run it twice (on two ports) and configure ``CAPTURE_ROOT_URL``.


=======
AUTHORS
=======

    * Mathieu Leplatre <mathieu.leplatre@makina-corpus.com>

|makinacom|_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

=======
LICENSE
=======

    * Lesser GNU Public License
