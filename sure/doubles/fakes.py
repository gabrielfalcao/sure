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

'''The :mod:`sure.doubles.fakes` module provides test-doubles of the type "Fake"

**"Fake objects actually have working implementations, but usually take some shortcut which makes them not suitable for production..."**
'''
from collections import OrderedDict


class FakeOrderedDict(OrderedDict):
    """Subclass of :class:`collections.OrderedDict` which overrides
    the methods :meth:`~collections.OrderedDict.__str__` and
    :meth:`~collections.OrderedDict.__repr__` to present an output
    similar to that of of a regular :class:`dict` instances.
    """
    def __str__(self):
        if len(self) == 0:
            return '{}'

        key_values = []
        for key, value in self.items():
            key, value = repr(key), repr(value)
            key_values.append("{0}: {1}".format(key, value))

        res = "{{{}}}".format(", ".join(key_values))
        return res

    def __repr__(self):
        return self.__str__()
