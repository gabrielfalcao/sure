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
"""tests for :class:`sure.AssertionBuilder` properties defined with the
decorator :func:`sure.assertionmethod`"""

from sure import expects
from sure.doubles import anything_of_type


def test_contains_and_to_contain():
    "expects.that().contains and expects().to_contain"

    expects.that(set(range(8))).contains(7)
    expects(set(range(13))).to.contain(8)
    expects(set(range(33))).to_contain(3)
    expects(set()).to_contain.when.called_with("art").should.have.raised("`art' should be in `set()'")


def test_does_not_contain_and_to_not_contain():
    "expects().contains and expects().to_not_contain"

    expects(list()).to_not_contain("speculations")
    expects(set(range(33))).to_not_contain.when.called_with(3).should.have.raised("`3' should not be in `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}'")


def test_within():
    "expects().to.be.within()"

    expects(3).to.be.within(set(range(33)))
    expects(7).to.be.within.when.called_with(0, 0, 6).should.have.raised(
        "(7).should.be.within(0, 0, 6) must be called with either an iterable:\n"
        "(7).should.be.within([1, 2, 3, 4])\n"
        "or with a range of numbers, i.e.: `(7).should.be.within(1, 3000)'"
    )
    expects(3).to.be.within(0, 7)
    expects(1).to_not.be.within.when.called_with(0, 0, 7).should.have.raised(
        "(1).should_not.be.within(0, 0, 7) must be called with either an iterable:\n"
    )
    expects(3).to.not_be.within.when.called_with(set(range(33))).should.have.raised(
        "`3' should not be in `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}'"
    )
    expects("art").to.be.within.when.called_with({"set"}).should.have.raised(
        "`art' should be in `{'set'}'"
    )


def test_different_of():
    "expects().to.be.different_of()"

    expects([]).to.be.different_of.when.called_with([]).should.have.raised(
        ".different_of only works for string comparison but in this case is expecting [] (<class 'list'>) instead"
    )
