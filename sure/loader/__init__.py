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

import os
import sys
import ast
import types
import importlib
import importlib.util

from typing import Dict, List, Optional, Tuple, Union
from importlib.machinery import PathFinder
from pathlib import Path
from sure.errors import InternalRuntimeError

from .astutil import gather_class_definitions_from_module_path

__MODULES__ = {}
__ROOTS__ = {}
__TEST_CLASSES__ = {}


def get_file_name(func) -> str:
    """returns the file name of a given function or method"""
    return FunMeta.from_function_or_method(func).filename


def get_line_number(func) -> str:
    """returns the first line number of a given function or method"""
    return FunMeta.from_function_or_method(func).line_number


def resolve_path(path, relative_to="~") -> Path:
    return Path(path).expanduser().absolute().relative_to(Path(relative_to).expanduser())


def collapse_path(e: Union[str, Path]) -> str:
    return str(e).replace(os.getenv("HOME"), "~")


def get_package(path) -> Path:
    if not isinstance(path, Path):
        path = Path(path)

    if not path.is_dir():
        path = path.parent

    counter = 0
    found = None
    while not found:
        counter += 1
        if not path.parent.joinpath('__init__.py').exists():
            found = path
        path = path.parent

    return found


class FunMeta(object):
    """container for metadata specific to Python functions or methods"""
    filename: str
    line_number: int
    name: str

    def __init__(self, filename: str, line_number: int, name: str):
        self.filename = collapse_path(filename)
        self.line_number = line_number
        self.name = name

    def __repr__(self):
        return f'<FunMeta filename={repr(self.filename)} line_number={repr(self.line_number)} name={repr(self.name)}>'

    @classmethod
    def from_function_or_method(cls, func):
        if not isinstance(func, (types.FunctionType, types.MethodType)):
            raise TypeError(f'get_function_or_method_metadata received an unexpected object: {func}')

        return cls(
            filename=func.__code__.co_filename,
            line_number=func.__code__.co_firstlineno,
            name=func.__name__,
        )


def name_appears_to_indicate_test(name: str) -> bool:
    return name.startswith('Test') or name.endswith('Test')


def appears_to_be_test_class(type_object: type) -> bool:
    if not isinstance(type_object, type):
        raise TypeError(f'{type_object} ({type(type_object)}) is not a {type}')

    name = type_object.__name__
    return issubclass(type_object, unittest.TestCase) or name_appears_to_indicate_test(name)


def get_type_definition_filename_and_firstlineno(type_object: type) -> Tuple[Path, int]:
    if not isinstance(type_object, type):
        raise TypeError(f'{type_object} ({type(type_object)}) is not a {type}')

    name = type_object.__name__
    module_name = type_object.__module__
    module = sys.modules.get(module_name)
    if not module:
        raise InternalRuntimeError(
            f"{module_name} does not appear within `sys.modules'. Perhaps Sure is not being used the right way or there is a bug in the current version"
        )
    path = Path(module.__file__)
    classes = __TEST_CLASSES__.get(path)
    if not classes:
        raise InternalRuntimeError(
            f"no class definitions found for {module}"
        )
    return path, classes[name]


class loader(object):
    @classmethod
    def load_recursive(cls, path, ignore_errors=True, glob_pattern='*.py'):
        modules = []
        path = Path(path)
        if path.is_file():
            return cls.load_python_path(path)

        base_path = Path(path).expanduser().absolute()
        targets = list(base_path.glob(glob_pattern))
        for path in targets:
            modules.extend(cls.load_python_path(path))

        return modules

    @classmethod
    def load_python_path(cls, path):
        if path.is_dir():
            logger.debug(f'ignoring directory {path}')
            return []

        if path.name.startswith('_') or path.name.endswith('_'):
            return []

        module, root = cls.load_package(path)
        return [module]

    @classmethod
    def load_package(cls, path):
        package = get_package(path)
        fqdn, _ = os.path.splitext(str(path.relative_to(package.parent)).replace(os.sep, "."))

        spec = importlib.util.spec_from_file_location(fqdn, path)
        module = importlib.util.module_from_spec(spec)
        __MODULES__[fqdn] = module
        cdfs = {}
        for name, metadata in gather_class_definitions_from_module_path(path).items():
            lineno, bases = metadata
            if any(filter(name_appears_to_indicate_test, [name] + list(bases))):
                cdfs[name] = lineno

        __TEST_CLASSES__[path] = cdfs
        sys.modules[fqdn] = module
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise e
        return module, package.absolute()
