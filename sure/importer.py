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
        base_path = Path(path).expanduser().absolute()
        targets = list(base_path.glob(glob_pattern))
        for file in targets:
            if file.is_dir():
                logger.debug(f'ignoring directory {file}')
                continue

            if file.name.startswith('_') or file.name.endswith('_'):
                continue

            module, root = cls.dig_to_root(file)
            __ROOTS__[str(root)] = root

        return list(__MODULES__.values())

    @classmethod
    def dig_to_root(cls, file):
        root = get_root_python_module(file)
        module_is_not_artificial = file.name != '__init__.py' and file.parent.joinpath('__init__.py').exists()
        if module_is_not_artificial:
            module_name = file.parent.name
            import ipdb;ipdb.set_trace()
        else:
            module_name = file.parent.name

        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        __MODULES__[module_name] = module
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module, root.absolute()
