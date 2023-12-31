# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2023>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from unittest import TestCase

feature = "test sure runner"


def test_function_ok():
    "testing successful function with sure runner"
    assert True


class TestClass(TestCase):
    "`sure' should work seamlessly with a unittest.TestCase"

    def setUp(self):
        self.one_attribute = {
            'question': 'does it work for us?'
        }

    def tearDown(self):
        self.one_attribute.pop('question')

    def test_expected_attribute_exists(self):
        "the setUp should work in our favor or else everything is unambiguously lost"
        assert hasattr(self, 'one_attribute'), f'{self} should have one_attribute but does not appear so'
