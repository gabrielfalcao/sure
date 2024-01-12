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
from sure import expects

from sure.loader import collapse_path
from sure.runtime import is_class_initializable_without_params


description = "tests generally heuristic functions within :mod:`sure.runtime`"


def test_is_class_initializable_without_params():
    class ParamFreeClass(object):
        def __init__(self):
            pass

    class ParamClass(object):
        def __init__(self, param: object):
            self.__param__ = param

    expects(is_class_initializable_without_params(ParamFreeClass)).to.not_be.false
    expects(is_class_initializable_without_params(ParamClass)).to.not_be.true
    expects(is_class_initializable_without_params({})).to.not_be.true
