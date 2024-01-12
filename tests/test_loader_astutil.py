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
import unittest
from unittest import TestCase
from sure import expects
from sure.loader.astutil import gather_class_definitions_from_module_path, gather_class_definitions_node


class TestLoaderAstUtilBaseClassName(TestCase):
    def test_gather_class_definitions_from_module_path(self):
        classes = gather_class_definitions_from_module_path(__file__)
        expects(classes).to.equal(
            {'TestLoaderAstUtilBaseClassName': (23, ('TestCase',)), 'TestLoaderAstUtilBaseClassAttributeAndName': (31, ('unittest.TestCase',))}
        )


class TestLoaderAstUtilBaseClassAttributeAndName(unittest.TestCase):
    def test_gather_class_definitions_from_module_path(self):
        classes = gather_class_definitions_from_module_path(__file__)
        expects(classes).to.equal(
            {'TestLoaderAstUtilBaseClassName': (23, ('TestCase',)), 'TestLoaderAstUtilBaseClassAttributeAndName': (31, ('unittest.TestCase',))}
        )


def test_gather_class_definitions_node_with_string():
    "sure.laoder.astutil.gather_class_definitions_node() with a string"

    expects(gather_class_definitions_node("string", classes={})).to.equal({})
