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


def get_root_python_module(path) -> Path:
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


class importer(object):
    @classmethod
    def load_recursive(cls, path, ignore_errors=True, glob_pattern='*.py'):
        modules = []
        path = Path(path)
        if path.is_file():
            return cls.load_python_file(path)

        base_path = Path(path).expanduser().absolute()
        targets = list(base_path.glob(glob_pattern))
        for file in targets:
            modules.extend(cls.load_python_file(file))

        return modules

    @classmethod
    def load_python_file(cls, file):
        if file.is_dir():
            logger.debug(f'ignoring directory {file}')
            return []

        if file.name.startswith('_') or file.name.endswith('_'):
            return []

        module, root = cls.dig_to_root(file)
        __ROOTS__[str(root)] = root
        return [module]

    @classmethod
    def dig_to_root(cls, file):
        root = get_root_python_module(file)
        module_is_artificial = file.parent.joinpath('__init__.py').exists()
        module_name = file.parent.name
        if not module_is_artificial:
            relative = str(file.relative_to(root.parent))
            module_name = os.path.splitext(relative)[0].replace(os.sep, '.')

        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        __MODULES__[module_name] = module
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise e
        return module, root.absolute()
