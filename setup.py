#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='screamshotter',
    version='1.0',
    author='Mathieu Leplatre',
    author_email='mathieu.leplatre@makina-corpus.com',
    url='https://github.com/makinacorpus/django-screamshot',
    description='Web pages capture server',
    long_description='',
    install_requires = ['django-screamshot'],
    packages=find_packages(),
    include_package_data=True,
    classifiers  = ['Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Environment :: Web Environment',
                    'Framework :: Django',
                    'Programming Language :: Python :: 2.7'],
)
