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

"unit tests for :mod:`sure.runtime`"

from collections.abc import Awaitable
from sure.runtime import object_name


def test_object_name_type():
    "calling ``sure.runtime.object_name(X)`` where X is a ``type``"
    assert object_name(Awaitable).should_not.equal("collections.abc.Awaitablea")
    assert object_name(Awaitable).should.equal("collections.abc.Awaitable")
