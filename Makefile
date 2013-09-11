install: bin/python

bin/python:
	virtualenv .
	bin/python setup.py develop

serve: bin/python
	bin/python ./manage.py runserver 8888

uwsgi: bin/python
	bin/pip install uwsgi

deploy: bin/python
	touch screamshotter/wsgi.py  # trigger reload

clean:
	rm -rf bin/ lib/ build/ dist/ *.egg-info/ include/ local/