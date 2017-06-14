#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-screamshot',
    version='0.8.1',
    author='Mathieu Leplatre',
    author_email='mathieu.leplatre@makina-corpus.com',
    url='https://github.com/makinacorpus/django-screamshot',
    description='Web pages capture using Django & CasperJS',
    long_description=open(os.path.join(here, 'README.rst')).read() + '\n\n' + 
                     open(os.path.join(here, 'CHANGES')).read(),
    license='LPGL, see LICENSE file.',
    install_requires = ['Django',
                        'django-timedeltafield'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers  = ['Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Environment :: Web Environment',
                    'Framework :: Django',
                    'Programming Language :: Python :: 2.7'],
)
