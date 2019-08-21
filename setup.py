#!/usr/bin/python
#
# Copyrigth 2014 Mappy S.A
#
# Licensed under Apache Software License, Version 2.0
#

from __future__ import absolute_import

try:
   import setuptools
   from setuptools import setup
except ImportError:
   setuptools = None
   from distutils.core import setup


kwargs = {}

if setuptools is not None:
   # If setuptools is not available, you're on your own for dependencies.
   install_requires = ['bitstring', 'six']
   kwargs['install_requires'] = install_requires

setup(
    name="pylr",
    version='3.0.1',
    packages = ["pylr", "pylr.tests"],
    package_data = {},
    author="Mappy S.A",
    url="https://github.com/Mappy/PyLR",
    license="AL2",
    description="Pylr, an OpenLR (tm) decoder.",
    classifiers=[
     'License :: OSI Approved :: Apache Software License, Version 2.0',
     'Programming Language :: Python :: 3.5',
    ],
    **kwargs
   )

