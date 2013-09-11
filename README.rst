**screamshotter**, the simplest Django project powered *django-screamshot*.

=======
INSTALL
=======

First make sure you have the ``casperjs`` command in your ``PATH``, using
related `installation instructions <http://casperjs.org>`_.

Install the egg (in a virtualenv or with sudo)

::

    python setup.py install

And then serve using your preferred method fot Django projects
(*mod_wsgy*, *gunicorn*, *circus*, ...).


Development
-----------

By default, it will use the latest published version on pypi. In order to 
run this server and develop *django-screamshot* at the same time :

::

    git clone https://github.com/makinacorpus/django-screamshot.git
    cd django-screamshot/
    python setup.py develop

======
Docker
======

You can deploy a Screamshotter instance with in one command using the Docker container :

::

  sudo docker run -p 9999:8000 makinacorpus/screamshotter

Enjoy it at http://localhost:9999 !


=====
USAGE
=====

Visit http://yourserver/?url=http://en.wikipedia.org/wiki/Main_Page&selector=%23mp-lower
