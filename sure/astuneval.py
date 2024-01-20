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
"""astuneval (Abstract Syntax-Tree Unevaluation) - safe substitution for unsafe :func:`eval`
"""
import ast


class Accessor(object):
    """base class for object element accessors"""

    def __init__(self, astbody):
        self.body = astbody

    def __call__(self, object: object, *args, **kw) -> object:
        return self.access(object, *args, **kw)

    def access(self, object: object) -> object:
        raise NotImplementedError(f"support to {type(self.body)} is not implemented")


class NameAccessor(Accessor):
    """Accesses an object's attributes through name"""

    def access(self, object: object) -> object:
        return getattr(object, self.body.id)


class SliceAccessor(Accessor):
    """Accesses an object's attributes through slice"""

    def access(self, object: object) -> object:
        return object[self.body.value]


class SubsAccessor(Accessor):
    """Accesses an object's attributes through subscript"""

    def access(self, object: object) -> object:
        get_value = NameAccessor(self.body.value)
        get_slice = SliceAccessor(self.body.slice)
        return get_slice(get_value(object))


class AttributeAccessor(Accessor):
    """Accesses an object's attributes through chained attribute"""

    def access(self, object: object) -> object:
        attr_name = self.body.attr
        access = resolve_accessor(self.body.value)
        value = access(object)
        return getattr(value, attr_name)


def resolve_accessor(body):
    return {
        ast.Name: NameAccessor,
        ast.Subscript: SubsAccessor,
        ast.Attribute: AttributeAccessor,
    }.get(type(body), Accessor)(body)


def parse_accessor(value: str) -> Accessor:
    body = parse_body(value)
    return resolve_accessor(body)


def parse_body(value: str) -> ast.stmt:
    bodies = ast.parse(value).body
    if len(bodies) > int(True):
        raise SyntaxError(f"{repr(value)} exceeds the maximum body count for ast nodes")

    return bodies[0].value
