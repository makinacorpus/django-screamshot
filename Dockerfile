FROM ubuntu
MAINTAINER Mathieu Leplatre "contact@mathieu-leplatre.info"
RUN apt-get -qq update
RUN apt-get install -y build-essential python-dev python-setuptools git-core wget bzip2 unzip 

#
#  PhantomJS
#...
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
RUN easy_install pip
RUN pip install virtualenv
RUN pip install uwsgi
RUN virtualenv --no-site-packages /opt/ve/screamshotter
ADD . /opt/apps/screamshotter
RUN /opt/ve/screamshotter/bin/python /opt/apps/screamshotter/setup.py install

#
#  Run !
#...
ADD .docker/run.sh /usr/local/bin/screamshotter
EXPOSE 8000
RUN echo " IdentityFile ~/.ssh/id_rsa" >> /etc/ssh/ssh_config
CMD ["/bin/sh", "-e", "/usr/local/bin/screamshotter"]