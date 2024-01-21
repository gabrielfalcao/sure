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

"""tests for :class:`sure.runtime.BaseResult`"""
from sure import expects
from sure.runtime import BaseResult


description = "tests for :class:`sure.runtime.BaseResult`"


def test_base_result___repr___not_implemented_error_missing_label_property():
    "BaseResult.__repr__ should raise :exc:`NotImplementederror` when missing a `label' property"

    expects(repr).when.called_with(BaseResult()).to.have.raised(
        NotImplementedError,
        "<class 'sure.runtime.BaseResult'> MUST define a `label' property or attribute which must be a string"
    )


def test_base_result___repr___not_implemented_error_nonstring_label_property():
    "calling :func:`repr` on a subclass of :class:`sure.runtime.BaseResult` whose label property returns something other than a :class:`str` instance should raise :exc:`NotImplementedError`"

    class FakeResultDummyLabelNonString(BaseResult):
        @property
        def label(self):
            return ()

    expects(repr).when.called_with(FakeResultDummyLabelNonString()).to.have.raised(
        NotImplementedError,
        "<class 'tests.test_runtime.test_base_result.test_base_result___repr___not_implemented_error_nonstring_label_property.<locals>.FakeResultDummyLabelNonString'>.label must be a string but is a <class 'tuple'> instead"
    )


def test_base_result___repr___returns_lowercase_label():
    "the builtin implementation of :meth:`sure.runtime.BaseResult.__repr__` should return the value of its `label' property as a lower-case string"

    class FakeResultDummyLabel(BaseResult):
        @property
        def label(self):
            return "LABEL"

    repr(FakeResultDummyLabel()).should.equal("'label'")
