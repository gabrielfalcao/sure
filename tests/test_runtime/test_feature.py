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

"""tests for :class:`sure.runtime.Feature`"""

from sure import expects
from sure.runtime import Feature
from sure.doubles import stub


description = "tests for :class:`sure.runtime.Feature`"


def test_feature_with_description():
    "repr(sure.runtime.Feature) with description"

    feature = stub(Feature, title="title", description="description")

    expects(repr(feature)).to.equal('<Feature "description" title>')


def test_feature_without_description():
    "repr(sure.runtime.Feature) with description"

    feature = stub(Feature, title="title", description=None)

    expects(repr(feature)).to.equal('<Feature "title">')
