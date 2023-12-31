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

"""this module tests some aspects of attempting to use the
:ref:`Special Syntax` of :mod:`sure` with that feature disabled

This module SHALL be tested *with* the command-line flags ``--reporter=test`` and **without** the command-line flags ``--special-syntax``
"""

from sure import expect, that, SpecialSyntaxDisabledError
from sure.reporters.test import events

description = "Special Syntax Disabled"


def try_special_syntax():
    "shouldnot".should_not.equal("should_not")


def test_report_special_syntax_disabled():
    "SpecialSyntaxDisabledError should be raised when its use is incorrect"

    expect(try_special_syntax).when.called.to.have.raised(
        SpecialSyntaxDisabledError,
        "test_special_syntax_disabled.py:31"
    )
