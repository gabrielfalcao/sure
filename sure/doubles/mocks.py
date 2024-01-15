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

'''The :mod:`sure.doubles.mocks` module currently does not provide
"Mocks" per se, it nevertheless serves as a containment module to
hermetically isolate the types :class:`unittest.mock._CallList` and,
if available within the target Python runtime, the type
:class:`mock.mock._CallList` in a tuple that
:class:`sure.core.DeepComparison` uses for comparing lists of
:class:`unittest.mock.call` or :class:`mock.mock.call` somewhat
interchangeably
'''


from unittest.mock import _CallList as UnitTestMockCallList

try:  # TODO: document the coupling with :mod:`mock` or :mod:`unittest.mock`
    from mock.mock import _CallList as MockCallList
except ImportError:  # pragma: no cover
    MockCallList = None

MockCallListType = tuple(filter(bool, (UnitTestMockCallList, MockCallList)))


__all__ = ['MockCallListType']
