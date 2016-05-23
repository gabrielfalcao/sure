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
          author='Gabriel Falcao',
          long_description=local_text_file('README.rst'),
          author_email='gabriel@nacaolivre.org',
          include_package_data=True,
          url='http://github.com/gabrielfalcao/sure',
          packages=find_packages(exclude=['*tests*']),
          install_requires=install_requires,
          tests_require=tests_require,
          test_suite='nose.collector',
          classifiers=[
              'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          ],
    )
