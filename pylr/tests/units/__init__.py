# -*- coding: utf-8 -*-
"""jfdizojfjzoi

koin koin

.. moduleauthor:: David Marteau <david.marteau@mappy.com>
"""

import os
import sys
import nose

TEST_MODULES = [
    'pylr.tests.units.test_binary_parser',
    'pylr.tests.units.test_decoder',
]


def run_tests(builddir="."):
    if not nose.run(defaultTest=','.join(TEST_MODULES), argv=["pylr-tests",
                                                              '--verbosity=2',
                                                              '--with-xunit',
                                                              '--xunit-file=pylr-nosetests.xml'.format(builddir),
                                                              '--nocapture'
                                                              ]):
        exit(1)
