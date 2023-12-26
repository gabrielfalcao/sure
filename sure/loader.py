import os
import sys
import importlib
import importlib.util
from importlib.machinery import PathFinder
from pathlib import Path


__MODULES__ = {}
__ROOTS__ = {}


def resolve_path(path, relative_to="~") -> Path:
    return Path(path).absolute().relative_to(Path(relative_to).expanduser())


def get_package(path) -> Path:
    if not isinstance(path, Path):
        path = Path(path)

    if not path.is_dir():
        path = path.parent

    stack = []
    counter = 0
    found = None
    while not found:
        counter += 1
        if not path.parent.joinpath('__init__.py').exists():
            found = path
            stack.append(found.parent.name)
        path = path.parent

    return found, ".".join(reversed(stack))


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

        module, root = cls.traverse_to_package(path)
        return [module]

    @classmethod
    def traverse_to_package(cls, path):
        package, fqdn = get_package(path)
        module_is_artificial = path.parent.joinpath('__init__.py').exists()
        module_name = path.parent.name
        if not module_is_artificial:
            relative = str(path.relative_to(root.parent))
            module_name = os.path.splitext(relative)[0].replace(os.sep, '.')

        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        __MODULES__[fqdn] = module
        sys.modules[fqdn] = module
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise e
        return module, package.absolute()
