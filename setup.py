#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-screamshot',
    version='0.1',
    author='Mathieu Leplatre',
    author_email='mathieu.leplatre@makina-corpus.com',
    url='',
    description='',
    long_description=open(os.path.join(here, 'README.rst')).read(),
    install_requires = ['django'],
    packages=find_packages(),
    classifiers  = ['Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Environment :: Web Environment',
                    'Framework :: Django',
                    'Programming Language :: Python :: 2.7'],
)
