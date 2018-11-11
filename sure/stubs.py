# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2018>  Gabriel Falcão <gabriel@nacaolivre.org>
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


def stub(base_class=None, **attributes):
    """creates a python class on-the-fly with the given keyword-arguments
    as class-attributes accessible with .attrname.

    The new class inherits from
    Use this to mock rather than stub.
    """
    if base_class is None:
        base_class = object

    members = {
        "__init__": lambda self: None,
        "__new__": lambda *args, **kw: object.__new__(
            *args, *kw
        ),  # remove __new__ and metaclass behavior from object
        "__metaclass__": None,
    }
    members.update(attributes)
    # let's create a python class on-the-fly :)
    return type(f"{base_class.__name__}Stub", (base_class,), members)()
