#!/usr/bin/env python
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
import os
import re
import sys
import types
import inspect
import traceback
import unittest
from typing import List, Optional, Dict
from sure.errors import NonValidTest, ExitError, ExitFailure
from sure.importer import importer
from sure.reporter import Reporter
from mock import Mock


def stripped(string):
    return "\n".join(filter(bool, [s.strip() for s in string.splitlines()]))


def seem_to_indicate_test(name: str) -> bool:
    return re.search(r'^(Ensure|Test|Spec|Scenario)', name or "", re.I)


class RuntimeOptions(object):
    immediate: bool

    def __init__(self, immediate: bool):
        self.immediate = immediate

    def __repr__(self):
        return f'<RuntimeOptions immediate={self.immediate}>'
