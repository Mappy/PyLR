#!/usr/bin/python
#
# Copyrigth 2014 Mappy S.A
#
# Licensed under Apache Software License, Version 2.0
#

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

version=__import__('pylr').__version__

setup(
    name="pylr",
    version=version,
    packages = ["pylr", "pylr.tests"],
    package_data = {},
    author="Mappy S.A",
#    author_email=???,
#    url=???,
    license="AL2",
    description="Pylr, an OpenLR (tm) decoder.",
    classifiers=[
     'License :: OSI Approved :: Apache Software License, Version 2.0',
     'Programming Language :: Python :: 2.7',
#    'Programming Language :: Python :: 3',
#    'Programming Language :: Python :: 3.2',
#    'Programming Language :: Python :: 3.3',
#    'Programming Language :: Python :: 3.4',
    ],
    **kwargs
   )

