#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2013>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ast
import os
import sys
import codecs
from setuptools import setup, find_packages


# These python versions of explicitly not supported
# by sure. This is nostly because of the incompatiblities
# with unicode strings. If there is an urgent reason why
# to support it after all or if you have a quick fix
# please open an issue on GitHub.
EXPL_NOT_SUPPORTED_VERSIONS = ((3, 0), (3, 1), (3, 2))

if sys.version_info[0:2] in EXPL_NOT_SUPPORTED_VERSIONS:
    raise SystemExit("sure does explicitly not support the following python versions "
                     "due to big incompatibilities: {0}".format(EXPL_NOT_SUPPORTED_VERSIONS))


PROJECT_ROOT = os.path.dirname(__file__)


class VersionFinder(ast.NodeVisitor):

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == 'version':
                self.version = node.value.s
        except:
            pass


def read_version():
    """Read version from sure/__init__.py without loading any files"""
    finder = VersionFinder()
    path = os.path.join(PROJECT_ROOT, 'sure', '__init__.py')
    with codecs.open(path, 'r', encoding='utf-8') as fp:
        file_data = fp.read().encode('utf-8')
        finder.visit(ast.parse(file_data))

    return finder.version


def local_text_file(*f):
    path = os.path.join(PROJECT_ROOT, *f)
    with open(path, 'rt') as fp:
        file_data = fp.read()

    return file_data


install_requires = ['mock', 'six']
tests_require = ['nose']


if __name__ == '__main__':
    setup(name='sure',
          version=read_version(),
          description='utility belt for automated testing in python for python',
          long_description=local_text_file('README.rst'),
          url='http://github.com/gabrielfalcao/sure',
          author='Gabriel Falcao',
          author_email='gabriel@nacaolivre.org',
          maintainer='Timo Furrer',
          maintainer_email='tuxtimo@gmail.com',
          include_package_data=True,
          packages=find_packages(exclude=['*tests*']),
          install_requires=install_requires,
          tests_require=tests_require,
          test_suite='nose.collector',
          classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console',
              'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: POSIX',
              'Operating System :: POSIX :: Linux',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: Implementation',
              'Programming Language :: Python :: Implementation :: CPython',
              'Programming Language :: Python :: Implementation :: PyPy',
              'Topic :: Software Development :: Testing'
          ]
    )
