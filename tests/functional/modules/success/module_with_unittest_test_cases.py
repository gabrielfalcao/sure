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

description = "Module with :class:`unittest.TestCase` subclasses"


class TestCaseA(unittest.TestCase):
    """Description of TestCaseA"""
    def test_case_A_member_A(self):
        pass

    def test_case_A_member_B(self):
        pass

    def test_case_A_member_C(self):
        pass


class TestCaseB(TestCase):
    def test_case_B_member_X(self):
        pass

    def test_case_B_member_Y(self):
        pass

    def test_case_B_member_Z(self):
        pass
