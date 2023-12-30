import os
import sys
import ast
import importlib
import importlib.util
from typing import Dict, List, Union, Tuple
from importlib.machinery import PathFinder
from pathlib import Path
from sure.errors import InternalRuntimeError

__MODULES__ = {}
__ROOTS__ = {}
__TEST_CLASSES__ = {}


def name_appears_to_indicate_test(name: str) -> bool:
    return name.startswith('Test') or name.endswith('Test')


def appears_to_be_test_class(type_object: type) -> bool:
    if not isinstance(type_object, type):
        raise TypeError(f'{type_object} ({type(type_object)}) is not a {type}')

    name = type_object.__name__
    return issubclass(type_object, unittest.TestCase) or name_appears_to_indicate_test(name)


def read_file_from_path(path: Path) -> str:
    with path.open() as f:
        return f.read()


def is_classdef(node: ast.stmt) -> bool:
    return isinstance(node, ast.ClassDef)


def resolve_base_names(bases: List[ast.stmt]) -> Tuple[str]:
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


def gather_class_definitions_from_module_path(path: Path) -> Dict[str, int]:
    node = ast.parse(read_file_from_path(path))
    return gather_class_definitions_node(node, {})


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


def resolve_path(path, relative_to="~") -> Path:
    return Path(path).absolute().relative_to(Path(relative_to).expanduser())


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
