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

import re
import os
import codecs
from setuptools import setup, find_packages


def read_metafile(path):
    """Read the contents from the given metafile."""
    with codecs.open(path, "rb", encoding="utf-8") as meta_f:
        return meta_f.read()


def get_meta(name):
    """Get a metadata field from the metafiles data"""
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=name.upper()),
        __META_DATA__, re.M
    )

    if not meta_match:
        raise RuntimeError("Unable to find __{0}__ string.".format(name))
    return meta_match.group(1)


__META_FILE__ = os.path.join("sure", "__init__.py")
__META_DATA__ = read_metafile(__META_FILE__)


install_requires = ['mock', 'six']
tests_require = ['nose']


if __name__ == '__main__':
    setup(name='sure',
          version=get_meta("version"),
          license=get_meta("license"),
          description=get_meta("description"),
          long_description=read_metafile("README.rst"),
          author=get_meta("author"),
          author_email=get_meta("author_email"),
          include_package_data=True,
          url='http://github.com/gabrielfalcao/sure',
          packages=find_packages(exclude=['*tests*']),
          install_requires=install_requires,
          tests_require=tests_require,
          test_suite='nose.collector',
          classifiers=[
              'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          ]
    )
