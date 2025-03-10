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
import sure
import types
from pathlib import Path
from mock import patch
from sure import expects
from sure.errors import FileSystemError
from sure.doubles import Dummy, stub
from sure.loader import (
    get_package,
    FunMeta,
    collapse_path,
    get_type_definition_filename_and_firstlineno,
    loader,
    ModulePath,
)

fake_packages_path = Path(__file__).parent.joinpath("fake_packages").absolute()


def test_get_package_upmost__init__containing():
    "sure.loader.get_package() returns the upmost path contaning a `__init__.py' file"

    path = get_package(fake_packages_path.joinpath("unsure/gawk/b.py"))
    expects(path).to.equal(fake_packages_path.joinpath("unsure"))


def test_funmeta_from_function():
    "sure.loader.FunMeta.from_function_or_method() accepts a function"

    fm = FunMeta.from_function_or_method(test_funmeta_from_function)
    expects(repr(fm)).to.equal(
        f"<FunMeta filename='{collapse_path(__file__)}' line_number=43 name='test_funmeta_from_function'>"
    )


def test_funmeta_from_method():
    "sure.loader.FunMeta.from_function_or_method() accepts a method"

    class Clanging:
        def destroy(self):
            pass

    fm = FunMeta.from_function_or_method(Clanging.destroy)

    expects(repr(fm)).to.equal(
        f"<FunMeta filename='{collapse_path(__file__)}' line_number=56 name='destroy'>"
    )


def test_funmeta_from_object_type():
    "sure.loader.FunMeta.from_function_or_method() accepts an object type"

    class SingleMethod:
        def execute(self):
            pass

    fm = FunMeta.from_function_or_method(SingleMethod)

    expects(repr(fm)).to.equal(
        f"<FunMeta filename='{collapse_path(__file__)}' line_number=69 name='SingleMethod'>"
    )


def test_funmeta_from_instance_type():
    "sure.loader.FunMeta.from_function_or_method() accepts an instance type"

    class Silver(object):
        pass

    fm = FunMeta.from_function_or_method(Silver())
    expects(repr(fm)).to.equal(
        f"<FunMeta filename='{collapse_path(__file__)}' line_number=83 name='Silver'>"
    )


def test_get_type_definition_filename_and_firstlineno_type_error_when_receiving_nonclass():
    "sure.loader.get_type_definition_filename_and_firstlineno() raises :exc:`TypeError` when given object is not a class type"

    target = Dummy("target")
    expects(get_type_definition_filename_and_firstlineno).when.called_with(
        target
    ).to.have.raised(
        TypeError, f"{target} (<class 'sure.doubles.dummies.Dummy'>) is not a class"
    )


@patch("sure.loader.sys")
def test_get_type_definition_filename_and_firstlineno_runtime_error_when_given_type_objects_module_is_not_in_sys_modules(
    sys,
):
    "sure.loader.get_type_definition_filename_and_firstlineno() raises :exc:`RuntimeError` when the apparent module name of the given object is not present within sys.modules"
    sys.modules = {}

    current = type(stub(__module__="module_name_dummy"))
    expects(get_type_definition_filename_and_firstlineno).when.called_with(
        current
    ).to.have.raised(
        RuntimeError,
        "module `module_name_dummy' does not appear within `sys.modules'. Perhaps Sure is not being used the right way or there is a bug in the current version",
    )


@patch("sure.loader.sys")
def test_get_type_definition_filename_and_firstlineno_builtin_returns_lineno_negative_1(
    sys,
):
    "sure.loader.get_type_definition_filename_and_firstlineno() returns lineno `-1` when the given module does not have a `__file__'"

    module_stub = stub(types.ModuleType)

    sys.modules = {"stub_module_name": module_stub}
    fake_type = type(stub(__module__="stub_module_name"))
    expects(get_type_definition_filename_and_firstlineno(fake_type)).to.equal(
        ("<stub_module_name>", -1)
    )


def test_loader_load_recursive_pattern_not_match():
    "sure.loader.loader.load_recursive() raises :exc:`sure.errors.FileSystemError` when given path is a file that does not match the given glob_pattern"

    path = Path(__file__)
    expects(loader.load_recursive).when.called_with(
        path, glob_pattern="*.zip"
    ).to.have.raised(FileSystemError, f"{path} does not match pattern '*.zip'")


def test_loader_load_recursive_excludes_must_be_list():
    "sure.loader.loader.load_recursive() raises :exc:`sure.errors.TypeError` when the excludes param is not a list or a ``NoneType``"

    path = Path(__file__)
    expects(loader.load_recursive).when.called_with(path, excludes="*").to.have.raised(
        TypeError,
        "sure.loader.load_recursive() param `excludes' must be a <class 'list'> but is '*' (<class 'str'>) instead",
    )


def test_loader_load_recursive():
    "sure.loader.loader.load_recursive() should ignore excludes"

    path = fake_packages_path.joinpath("unsure")

    modules = loader.load_recursive(
        path=path,
        glob_pattern="***.py",
        excludes=["**clanging*"],
    )
    expects(modules).to.have.length_of(3)

    module_names = [module.__name__ for module in modules]
    expects(module_names).to.equal(
        ["unsure.gawk.a", "unsure.gawk.b", "unsure.grasp.understand"]
    )


@patch("sure.loader.send_runtime_warning")
def test_loader_load_python_path_returns_empty_list_when_given_path_is_a_directory(
    send_runtime_warning,
):
    "sure.loader.loader.load_python_path() should return empty list when receiving a :class:`pathlib.Path` that is a directory"

    modules = loader.load_python_path(fake_packages_path)

    expects(modules).to.be.a(list)
    expects(modules).to.be.empty

    send_runtime_warning.assert_called_once_with(
        f"ignoring {fake_packages_path} for being a directory"
    )


@patch("sure.loader.send_runtime_warning")
@patch("sure.loader.Path")
def test_loader_load_python_path_returns_empty_list_when_given_path_is_a_broken_symlink(
    Path, send_runtime_warning
):
    "sure.loader.loader.load_python_path() should return empty list when receiving a :class:`pathlib.Path` that points to a broken symlink"

    path = Path.return_value
    path.is_dir.return_value = False
    path.is_symlink.return_value = True
    path.resolve.return_value.exists.return_value = False
    path.absolute.return_value = "absolute-path-dummy"
    modules = loader.load_python_path(fake_packages_path)

    expects(modules).to.be.a(list)
    expects(modules).to.be.empty

    send_runtime_warning.assert_called_once_with(
        "parsing skipped of irregular file `absolute-path-dummy'"
    )


@patch("sure.loader.send_runtime_warning")
def test_loader_load_python_path_returns_empty_list_when_given_path_seems_to_be_a_dunder_file(
    send_runtime_warning,
):
    "sure.loader.loader.load_python_path() should return empty list when receiving a :class:`pathlib.Path` that is a directory"

    path = fake_packages_path.joinpath("unsure/__init__.py")
    modules = loader.load_python_path(path)

    expects(modules).to.be.a(list)
    expects(modules).to.be.empty

    send_runtime_warning.assert_called_once_with(
        f"ignoring {path} for seeming to be a __dunder__ file"
    )


def test_loader_load_package_raises_exception_if_there_is_an_issue_executing_module_specification():
    "sure.loader.loader.load_package() should raise exception when there is an issue executing the module :class:`importlib.ModuleSpec`"

    path = fake_packages_path.joinpath("unsure/gawk/clanging.py")
    expects(loader.load_package).when.called_with(path).to.have.raised(
        "invalid syntax (<unknown>, line 17)"
    )


def test_loader_load_package_returns_module_and_package_path():
    "sure.loader.loader.load_package() should return a tuple with an instance of :class:`types.ModuleType` and its respective module path"

    path = fake_packages_path.joinpath("unsure/gawk/a.py")
    return_value = loader.load_package(path)
    expects(return_value).to.be.a(tuple)
    expects(return_value).to.have.length_of(2)
    module, package_path = return_value
    expects(module).to.be.a(types.ModuleType)
    expects(package_path).to.equal(path.parent.parent)


def test_module_path_is_module_dir_true():
    "sure.loader.ModulePath.is_module_dir returns `True' when pointing to a path containing a __init__.py file"

    module_path = ModulePath(Path(__file__).parent)
    assert module_path.is_module_dir() == True


def test_module_path_is_module_dir_false_if_path_does_not_contain_init_file():
    "sure.loader.ModulePath.is_module_dir returns `False' when pointing to a path not containing a __init__.py file"

    path = Path(__file__).parent.joinpath(
        "88242a09d8f254febcdb340fd340356bef261e368a691bfd8f4ddee794519c7f"
    )
    path.mkdir(0o701, True, True)
    module_path = ModulePath(path)
    assert module_path.is_module_dir() == False


def test_module_path_is_module_dir_false_if_path_is_not_a_directory():
    "sure.loader.ModulePath.is_module_dir returns `False' when pointing to a path not being a directory"

    module_path = ModulePath(__file__)
    assert module_path.is_module_dir() == False


def test_module_path_in_module_dir_true_if_path_is_a_directory_and_parent_path_contains_init_file():
    "sure.loader.ModulePath.in_module_dir returns `True' when pointing to a path whose parent directory contains a __init__.py file"

    module_path = ModulePath(Path(sure.__file__).parent)
    assert module_path.in_module_dir() == True


def test_module_path_is_module_file_true():
    "sure.loader.ModulePath.is_module_file returns `True' when pointing to a path referencing a `*.py' file"

    module_path = ModulePath(Path(__file__))
    assert module_path.is_module_file() == True


def test_module_path_is_module_file_false_if_path_is_not_a_file():
    "sure.loader.ModulePath.is_module_file returns `False' when pointing to a path not referencing a file"

    path = Path(__file__).parent
    module_path = ModulePath(path)
    assert module_path.is_module_file() == False


def test_module_path_in_module_dir_false_if_path_does_not_contain_init_file():
    "sure.loader.ModulePath.in_module_dir returns `False' when pointing to a path whose parent directory contains a __init__.py file"

    path = Path(__file__).parent.joinpath(
        "fc78b255ded1f12b84c5a603908bf710473abcbb6b29b0039f43d7f80ca37d8f"
    )
    path.mkdir(0o701, True, True)
    module_path = ModulePath(path)
    assert module_path.in_module_dir() == False


def test_module_path_in_module_dir_true_if_path_is_not_a_directory_and_parent_path_contains_init_file():
    "sure.loader.ModulePath.in_module_dir returns `True' when pointing to a path whose parent directory contains a __init__.py file"

    module_path = ModulePath(sure.__file__)
    assert module_path.in_module_dir() == True


def test_module_path_is_module_file_true():
    "sure.loader.ModulePath.is_module_file returns `True' when pointing to a path referencing a `*.py' file"

    module_path = ModulePath(Path(__file__))
    assert module_path.is_module_file() == True


def test_module_path_extension_returns_file_extension():
    "sure.loader.ModulePath.is_module_file returns `False' when pointing to a path not referencing a file"

    module_path = ModulePath(__file__)
    assert ".py" in module_path.extension()



def test_module_path_is_module_true_when_pointing_to_path_containing_init_file():
    "sure.loader.ModulePath.is_module returns `True' when pointing to a path containing a __init__.py file"

    module_path = ModulePath(Path(__file__).parent)
    assert module_path.is_module() == True


def test_module_path_is_module_true_when_pointing_to_path_to_python_file():
    "sure.loader.ModulePath.is_module returns `True' when pointing to a path referencing a `*.py' file"

    module_path = ModulePath(Path(__file__).parent)
    assert module_path.is_module() == True
