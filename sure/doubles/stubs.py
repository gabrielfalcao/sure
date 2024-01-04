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

'''The :mod:`sure.doubles.stubs` module provides test-doubles of the type "Stub"

**Stubs** provide canned answers to calls made during the test, usually not responding at all to anything outside what's programmed in for the test.
'''


def stub(base_class=None, metaclass=None, **attributes):
    """creates a python class "on-the-fly" with the given keyword-arguments
    as class-attributes accessible with .attrname.

    The new class inherits from ``base_class`` and defaults to ``object``
    Use this to mock rather than stub in instances where such approach seems reasonable.
    """
    if base_class is None:
        base_class = object

    members = {
        "__init__": lambda self: None,
        "__new__": lambda *args, **kw: object.__new__(
            *args, *kw
        ),
    }
    kwds = {}
    if metaclass is not None:
        kwds["metaclass"] =  metaclass
        members["__metaclass__"] = metaclass  # TODO: remove this line

    members.update(attributes)
    return type(f"{base_class.__name__}Stub", (base_class,), members, **kwds)()
