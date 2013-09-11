FROM ubuntu
MAINTAINER Mathieu Leplatre "mathieu.leplatre@makina-corpus.com"

#
#  Ubuntu
#...
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get -qq update
RUN apt-get install -y build-essential git-core wget bzip2 unzip gettext

#
#  Python
#...
RUN apt-get install -y python-dev python-setuptools python-virtualenv

#
#  PhantomJS
#...
RUN apt-get install -y libfreetype6 fontconfig
RUN rm -rf /opt/*phantomjs*/
RUN wget --quiet http://phantomjs.googlecode.com/files/phantomjs-1.8.1-linux-x86_64.tar.bz2 -O /opt/phantomjs.tar.bz2
RUN tar -jxvf /opt/phantomjs.tar.bz2 -C /opt/
RUN rm /opt/phantomjs.tar.bz2
RUN ln -sf /opt/*phantomjs*/bin/phantomjs /usr/bin/

#
#  CasperJS
#...
RUN rm -rf /opt/*casperjs*/
RUN wget --quiet https://github.com/n1k0/casperjs/zipball/1.0.2 -O /opt/casperjs.zip
RUN unzip -o /opt/casperjs.zip -d /opt/ > /dev/null
RUN rm /opt/casperjs.zip
RUN ln -sf /opt/*casperjs*/bin/casperjs /usr/bin/

#
#  Screamshotter
#...
ADD . /opt/apps/screamshotter
RUN (cd /opt/apps/screamshotter && git remote rm origin)
RUN (cd /opt/apps/screamshotter && git remote add origin https://github.com/makinacorpus/django-screamshot.git)
RUN (cd /opt/apps/screamshotter && make install deploy)
RUN /opt/apps/screamshotter/bin/pip install Pillow

RUN /opt/apps/screamshotter/bin/pip install uwsgi
ADD .docker/run.sh /usr/local/bin/run

#
#  Run !
#...
EXPOSE 8000
CMD ["/bin/sh", "-e", "/usr/local/bin/run"]