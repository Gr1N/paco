#!/usr/bin/env python
"""
pyco
====
An utility library for asyncronous coroutines primitives for Python +3.4.

:copyright: (c) 2016 Tomas Aparicio
:license: MIT
"""

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

setup_requires = []

if 'test' in sys.argv:
    setup_requires.append('pytest')

# Read dev requirements
with open('requirements-dev.txt') as f:
    tests_require = f.read().splitlines()


def read_version(package):
    with open(os.path.join(package, '__init__.py'), 'r') as fd:
        for line in fd:
            if line.startswith('__version__ = '):
                return line.split()[-1].strip().strip("'")


# Get package current version
version = read_version('pyco')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests/']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='pyco',
    version='0.1.0',
    author='Tomas Aparicio',
    description=(
        'Asynchronous higher-order functions goodness Python +3.4.'
    ),
    url='https://github.com/h2non/pyco',
    license='MIT',
    long_description=open('README.rst').read(),
    py_modules=['pyco'],
    zip_safe=False,
    tests_require=tests_require,
    packages=find_packages(exclude=['tests', 'examples']),
    cmdclass={'test': PyTest},
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development'
    ],
)