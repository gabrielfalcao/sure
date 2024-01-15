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

import os
import sys
import ast
import types
import inspect
import traceback
import importlib
import importlib.util
from fnmatch import fnmatch
from _frozen_importlib import ModuleSpec
from typing import Dict, List, Optional, Tuple, Union
from importlib.machinery import PathFinder
from pathlib import Path
from sure.errors import (
    InternalRuntimeError,
    FileSystemError,
    CallerLocation,
    collapse_path,
    send_runtime_warning
)

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
    return (
        Path(path).expanduser().absolute().relative_to(Path(relative_to).expanduser())
    )


def get_package(path: Union[str, Path]) -> Path:
    path = Path(path).expanduser().absolute()

    if not path.is_dir():
        path = path.parent

    found = None
    while not found:
        if not path.parent.joinpath("__init__.py").exists():
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
        return f"<FunMeta filename={repr(self.filename)} line_number={repr(self.line_number)} name={repr(self.name)}>"

    @classmethod
    def from_function_or_method(cls, target):
        if isinstance(target, (types.FunctionType, types.MethodType)):
            path = target.__code__.co_filename
            lineno = target.__code__.co_firstlineno
            name = target.__name__
        elif inspect.isclass(target):
            path, lineno = get_type_definition_filename_and_firstlineno(target)
            name = target.__name__
        else:
            name = target.__class__.__name__
            path, lineno = get_type_definition_filename_and_firstlineno(target.__class__)

        return cls(
            filename=path,
            line_number=lineno,
            name=name,
        )


def get_type_definition_filename_and_firstlineno(type_object: type) -> Tuple[Path, int]:
    if not inspect.isclass(type_object):
        raise TypeError(f"{type_object} ({type(type_object)}) is not a class")

    name = type_object.__name__
    module_name = type_object.__module__
    module = sys.modules.get(module_name)
    if not module:
        raise RuntimeError(
            f"module `{module_name}' does not appear within `sys.modules'. Perhaps Sure is not being used the right way or there is a bug in the current version",
        )
    if not hasattr(module, '__file__'):
        return f"<{module_name}>", -1

    path = Path(module.__file__)
    called_location = CallerLocation.most_recent()
    classes = gather_class_definitions_from_module_path(
        path, nearest_line=called_location.lineno
    )
    __TEST_CLASSES__[path] = classes
    lineno, base_class_names = classes[name]
    return collapse_path(path), lineno


class loader(object):
    @classmethod
    def load_recursive(
        cls,
        path: Union[str, Path],
        ignore_errors: bool = True,
        glob_pattern: str = "***.py",
        excludes: Optional[List[Union[str, Path]]] = None,
    ):
        modules = []
        excludes = excludes or []
        if not isinstance(excludes, list):
            raise TypeError(f"sure.loader.load_recursive() param `excludes' must be a {list} but is {repr(excludes)} ({type(excludes)}) instead")
        path = Path(path)
        if path.is_file():
            if fnmatch(path, glob_pattern):
                return cls.load_python_path(path)
            else:
                raise FileSystemError(
                    f"{path} does not match pattern {repr(glob_pattern)}"
                )

        base_path = Path(path).expanduser().absolute()
        for directory, _, files in os.walk(base_path):
            if any(
                [path in directory or fnmatch(directory, path) for path in excludes]
            ):
                continue

            directory = Path(directory)
            for path in files:
                if any([e in path or fnmatch(path, e) for e in excludes]):
                    continue

                if fnmatch(path, glob_pattern):
                    path = directory.joinpath(path)
                    modules.extend(cls.load_python_path(path))

        return sorted(modules, key=lambda mod: mod.__file__)

    @classmethod
    def load_python_path(cls, path: Union[str, Path]) -> List[types.ModuleType]:
        path = Path(path)
        if path.is_dir():
            send_runtime_warning(f"ignoring {path} for being a directory")
            return []

        extlessname, _ = os.path.splitext(path.name)
        if extlessname.startswith("__") or extlessname.endswith("__"):
            send_runtime_warning(f"ignoring {path} for seeming to be a __dunder__ file")
            return []

        module, root = cls.load_package(path)
        return [module]

    @classmethod
    def load_module(
        cls, path: Union[str, Path]
    ) -> Tuple[types.ModuleType, ModuleSpec, str, Path]:
        path = Path(path)
        package = get_package(path)
        fqdn, _ = os.path.splitext(
            str(path.relative_to(package.parent)).replace(os.sep, ".")
        )

        spec = importlib.util.spec_from_file_location(fqdn, path)

        module = importlib.util.module_from_spec(spec)
        __MODULES__[fqdn] = module
        cdfs = {}
        for name, metadata in gather_class_definitions_from_module_path(
            path, None
        ).items():
            lineno, bases = metadata
            if any(filter(name_appears_to_indicate_test, [name] + list(bases))):
                cdfs[name] = lineno

        __TEST_CLASSES__[path] = cdfs
        return module, spec, fqdn, package.absolute()

    @classmethod
    def load_package(cls, path: Union[str, Path]) -> Tuple[types.ModuleType, Path]:
        module, spec, fqdn, package_path = cls.load_module(path)
        sys.modules[fqdn] = module
        spec.loader.exec_module(module)
        return module, package_path


def object_belongs_to_sure(object: object) -> bool:
    """
    :param object: an :class:`object` object
    :returns: ``True`` if the given ``object`` passes this function heuristics to verify that the object belongs to :mod:`sure`
    """
    module_name = (
        getattr(
            object,
            "__module__",
            getattr(getattr(object, "__class__", object), "__module__", ""),
        )
        or ""
    )
    heuristics = [
        lambda: module_name == "sure",
        lambda: module_name.startswith("sure."),
    ]

    return any([heuristic() is True for heuristic in heuristics])


def name_appears_to_indicate_test(name: str) -> bool:
    return name.startswith("Test") or name.endswith("Test")
