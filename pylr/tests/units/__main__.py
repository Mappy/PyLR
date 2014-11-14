# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    from . import run_tests
    run_tests(builddir=sys.argv[1] if len(sys.argv)>1 else ".")
