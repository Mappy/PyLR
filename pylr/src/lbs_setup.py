# -*- coding: utf-8 -*-
import os
from glob import glob
from fnmatch import fnmatch

if os.environ.get('LBS_USE_SETUPTOOLS') == '1':
    """ We use setuptools """
    from setuptools import setup as _setup, find_packages
    with_setuptools = True
    requires_arg = 'install_requires'

    def requires(filename):
        '''Parse requirement file and transform it to setuptools requirements'''
        if os.path.exists(filename):
            return [i.strip() for i in open(filename).readlines()]
        else:
            return []
else:
    """ We use distutils """
    from distutils.core import setup as _setup
    from distutils.util import convert_path
    with_setuptools = False
    requires_arg = 'requires'

    def find_packages(where='.', exclude=()):
        """Return a list all Python packages found within directory 'where'

        'where' should be supplied as a "cross-platform" (i.e. URL-style) path; it
        will be converted to the appropriate local path syntax.  'exclude' is a
        sequence of package names to exclude; '*' can be used as a wildcard in the
        names, such that 'foo.*' will exclude all subpackages of 'foo' (but not
        'foo' itself).
        """
        out = []
        stack = [(convert_path(where), '')]
        while stack:
            where, prefix = stack.pop(0)
            for name in os.listdir(where):
                fn = os.path.join(where, name)
                looks_like_package = (
                    '.' not in name
                    and os.path.isdir(fn)
                    and os.path.isfile(os.path.join(fn, '__init__.py'))
                )
                if looks_like_package:
                    out.append(prefix+name)
                    stack.append((fn, prefix+name+'.'))
        for pat in list(exclude)+['ez_setup']:
            from fnmatch import fnmatchcase
            out = [item for item in out if not fnmatchcase(item, pat)]
        return out

    def requires(filename):
        """ convert pip requirements to distutils requires
        """
        if os.path.exists(filename):
            import re
            expr = re.compile(r'(.*)(\=\=|\>\=|\<\=)(.*)')

            def convert(l):
                m = expr.match(l)
                if m:
                    return "{} ({}{})".format(*m.groups())
                else:
                    return l
            return [convert(l) for l in map(lambda l: l.rstrip("\n"), open(filename).readlines()) if l]
        else:
            return []


def find_data_files(srcdir, wildcards=('*'), **kw):
    # get a list of all files under the srcdir matching wildcards,
    # returned in a format to be used for install_data
    exclude = kw.get('exclude', ())

    def opj(*args):
        path = os.path.join(*args)
        return os.path.normpath(path)

    def walk_helper((lst, wildcards), dirname, files):
        names = []
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                if not any(fnmatch(f, bad) for bad in exclude):
                    filename = opj(dirname, f)
                    if fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
        if names:
            lst.append((dirname, names))

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(f) for f in glob(opj(srcdir, '*'))])
    return file_list


def default_kwargs(**kwargs):
    product_name = kwargs.pop('name', None)
    if not product_name:
        product_name = __import__('build_manifest').product_name

    version_tag = kwargs.pop('version', None)
    if not version_tag:
        version_tag = __import__('build_manifest').version_tag

    requirements = kwargs.pop('requires', None)
    if not requirements:
        requirements = requires("requirements.txt")

    _kwargs = dict(name=product_name,
                   version=version_tag,
                   author='Mappy LBS Team',
                   author_email='dt.lbs@mappy.com',
                   maintainer='Mappy LBS Team',
                   maintainer_email='dt.lbs@mappy.com',
                   url='http://lbsdoc.mappy.priv/docs/{}'.format(product_name),
                   requires=requirements
                   )
    _kwargs[requires_arg] = requirements
    _kwargs.update(kwargs)
    return _kwargs


def setup(**kwargs):
    return _setup(**default_kwargs(**kwargs))
