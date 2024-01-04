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
"""astutils (Abstract Syntax-Tree Utils)"""
import ast

from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path


def is_classdef(node: ast.stmt) -> bool:
    """
:param node: a :class:`node <ast.AST>` instance
:returns: ``True`` if the given :class:`node <ast.AST>` is a :class:`ast.ClassDef`
    """
    return isinstance(node, ast.ClassDef)


def resolve_base_names(bases: List[ast.stmt]) -> Tuple[str]:
    """returns a tuple with the names of base classes of an :class:`node <ast.AST>`
    """
    names = []
    for base in bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
            continue
        if isinstance(base, ast.Attribute):
            names.append(f"{base.value.id}.{base.attr}")
            continue
        raise NotImplementedError(f"{base} of type {type(base)} not yet supported")

    return tuple(names)


def gather_class_definitions_node(node: Union[ast.stmt, str], acc: dict) -> Dict[str, Tuple[int, Tuple[str]]]:
    """Recursively scans all class definitions of an :class:`node <ast.AST>`

    Primarily designed to find nested :class:`unittest.TestCase` classes.

    :returns: :class:`dict` containing a 2-item tuple: (line number, tuple of base class names), keyed with the class name

    """
    classes = dict(acc)

    if is_classdef(node):
        classes[node.name] = (node.lineno, resolve_base_names(node.bases))
    elif isinstance(node, str):
        return classes

    for name, subnode in ast.iter_fields(node):
        if isinstance(subnode, list):
            for subnode in subnode:
                classes.update(gather_class_definitions_node(subnode, classes))

    return classes


def gather_class_definitions_from_module_path(path: Path) -> Dict[str, Tuple[int, Tuple[str]]]:
    """parses the Python file at the given path and returns a mapping
    of class names to tuples indicating the line number in which the
    class is defined and a tuple with the names of its base classes.
    """

    with path.open() as f:
        node = ast.parse(f.read())

    return gather_class_definitions_node(node, {})
