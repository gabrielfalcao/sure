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

'''The :mod:`sure.doubles.dummies` module provides test-doubles of the type "Dummy"

"**Dummy objects are passed around but never actually used. Usually they are just used to fill parameter lists.**"
'''


class Dummy(object):
    """class for creating Dummy objects with a string identity
    """
    def __init__(self, dummy_id: str):
        if not isinstance(dummy_id, str):
            raise TypeError(
                f'dummy() takes string as argument, received {dummy_id} ({type(dummy_id)}) instead'
            )

        self.__dummy_id__ = id

    def __repr__(self):
        return f'<Dummy {self.__dummy_id__}>'

    def __str__(self):
        return f'<Dummy {self.__dummy_id__}>'


class Anything(Dummy):
    """Dummy class whose entire purpose is to serve as sentinel in assertion
    statements where the :meth:`operator.__eq__` is employed under the
    specific circumstance of expecting the :class:`bool` value ``True``
    """
    def __eq__(self, _):
        return True


anything = Anything('sure.doubles.dummies.Anything')
