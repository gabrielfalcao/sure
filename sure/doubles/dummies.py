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
__dummy_id_registry__ = {}


class Dummy(object):
    """class for creating Dummy objects with a string identity.

    When compared with ``==`` (:func:`operator.eq`) :class:`~sure.doubles.dummes.Dummy` objects are matched at the ``dummy_id``
    """

    def __init__(self, dummy_id: str):
        if not isinstance(dummy_id, str):
            raise TypeError(
                f'{__name__}.Dummy() takes string as argument, received {dummy_id} ({type(dummy_id)}) instead'
            )

        self.__dummy_id__ = dummy_id
        __dummy_id_registry__[dummy_id] = self

    @property
    def id(self):
        return self.__dummy_id__

    def __eq__(self, dummy) -> bool:
        return isinstance(dummy, Dummy) and self.id == dummy.id

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


class AnythingOfType(Anything):
    """Dummy class bound to a :class:`type` in terms of employing the :meth:`operator.__eq__`
    """
    def __init__(self, expected_type: type):
        if not isinstance(expected_type, type):
            raise TypeError(f'{repr(expected_type)} should be a class but is a {type(expected_type)} instead')

        module_name = expected_type.__module__
        type_name = expected_type.__name__
        self.__expected_type__ = expected_type
        self.__type_fqdn__ = f"{module_name}.{type_name}"
        super().__init__(f"anything_of_type({self.__type_fqdn__})")

    def __eq__(self, given: object):
        given_type = type(given)
        module_name = given_type.__module__
        type_name = given_type.__name__
        return isinstance(given, self.__expected_type__) and super().__eq__(f"typed:{module_name}.{type_name}")

    def __repr__(self):
        return f'<AnythingOfType[{self.__type_fqdn__}] {self.__dummy_id__}>'

    def __str__(self):
        return f'<AnythingOfType[{self.__type_fqdn__}] {self.__dummy_id__}>'


anything = Anything('sure.doubles.dummies.Anything')


def anything_of_type(expected_type: type) -> AnythingOfType:
    return AnythingOfType(expected_type)
