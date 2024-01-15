#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <sure - sophisticated automated test library and runner>
# Copyright (C) <2010-2024>  Gabriel Falcão <gabriel@nacaolivre.org>
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

"""sophisticated automated test library and runner"""

import os
import ast
import sys
import codecs
from setuptools import setup, find_packages

# These python versions are explicitly not supported
# by sure. This is mostly because of the incompatiblities
# with unicode strings. If there is an urgent reason why
# to support it after all or if you have a quick fix
# please open an issue on GitHub.
EXPL_NOT_SUPPORTED_VERSIONS = ((3, 0), (3, 1), (3, 2))

if sys.version_info[0:2] in EXPL_NOT_SUPPORTED_VERSIONS:
    raise SystemExit(
        "Sure does explicitly not support the following python versions "
        "due to big incompatibilities: {0}".format(EXPL_NOT_SUPPORTED_VERSIONS)
    )

if sys.version_info[0] < 3:
    raise SystemExit(
        "Sure no longer supports Python 2"
    )


PROJECT_ROOT = os.path.dirname(__file__)


class VersionFinder(ast.NodeVisitor):
    VARIABLE_NAME = "version"

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == self.VARIABLE_NAME:
                self.version = node.value.s
        except Exception:
            pass


def read_version():
    finder = VersionFinder()
    finder.visit(ast.parse(local_text_file("sure", "version.py")))
    return finder.version


def local_text_file(*f):
    path = os.path.join(PROJECT_ROOT, *f)
    with open(path, "rt") as fp:
        file_data = fp.read()

    return file_data


def read_readme():
    """Read README content.
    If the README.rst file does not exist yet
    (this is the case when not releasing)
    only the short description is returned.
    """
    try:
        return local_text_file("README.rst")
    except IOError:
        return __doc__


install_requires = ["mock", "coverage==7.4.0", "click==8.1.7", "couleur==0.7.4"]
tests_require = []
version = read_version()

if __name__ == "__main__":
    setup(
        name="sure",
        version=version,
        description=__doc__,
        long_description=read_readme(),
        url="http://github.com/gabrielfalcao/sure",
        author="Gabriel Falcao",
        author_email="gabriel@nacaolivre.org",
        maintainer="Gabriel Falcao",
        maintainer_email="gabrielteratos@gmail.com",
        include_package_data=True,
        packages=find_packages(exclude=["*tests*"]),
        install_requires=install_requires,
        long_description_content_type='text/x-rst',
        entry_points={
            "console_scripts": ["sure = sure.cli:entrypoint"],
        },
        tests_require=tests_require,
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: Implementation",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Testing",
        ],
    )
