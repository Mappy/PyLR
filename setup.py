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
   install_requires = ['bitstring']
   kwargs['install_requires'] = install_requires


def get_version():
    local_vars = {}
    exec(open('pylr/version.py').read(),{},local_vars)
    return local_vars["__version__"]

version = get_version()

setup(
    name="pylr",
    version=version,
    packages = ["pylr", "pylr.tests"],
    package_data = {},
    author="Mappy S.A",
    url="https://github.com/Mappy/PyLR",
    license="AL2",
    description="Pylr, an OpenLR (tm) decoder.",
    classifiers=[
     'License :: OSI Approved :: Apache Software License, Version 2.0',
     'Programming Language :: Python :: 2.7',
    ],
    **kwargs
   )

