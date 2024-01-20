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
import re
import sys
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

    expects("").to.be.different_of.when.called_with([]).should.have.raised(
        ".different_of only works for string comparison but in this case is expecting [] (<class 'list'>) instead"
    )

    expects([]).to.be.different_of.when.called_with("").should.have.raised(
        ".different_of only works for string comparison but in this case the actual source comparison object is [] (<class 'list'>) instead"
    )


def test_is_a():
    "expects().to.be.a()"

    expects(b"a").to.be.a(bytes)
    expects(sys.stdout).to.be.a.when.called_with("io.StringIO").to.have.raised(
        "expects(sys.stdout).to.be.a.when.called_with(\"io.StringIO\").to.have.raised( expects `<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>' to be an `io.StringIO'"
    )
    expects(sys.stdout).to.not_be.a.when.called_with("io.TextIOWrapper").to.have.raised(
        "expects(sys.stdout).to.not_be.a.when.called_with(\"io.TextIOWrapper\").to.have.raised( expects `<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>' to not be an `io.TextIOWrapper'"
    )


def test_to_be_below():
    "expects().to.be.below()"

    expects(b"A").to.be.below(b"a")
    expects(b"a").to.below.when.called_with(b"A").should.have.raised(
        "b'a' should be below b'A'"
    )
    expects(70).to_not.be.below.when.called_with(83).should.have.raised(
        "70 should not be below 83"
    )
    expects(b"a").to.below.when.called_with(b"A").should_not.have.raised.when.called_with(
        "b'a' should be below b'A'"
    ).should.have.thrown.when.called_with("`below' called with args (b'A',) and keyword-args {} should not raise b'a' should be below b'A' but raised b'a' should be below b'A'").should.return_value(not False)


def test_to_be_above():
    "expects().to.be.above()"

    expects(b"S").to.be.above(b"B")
    expects(b"D").to.be.above.when.called_with(b"S").should.have.raised(
        "b'D' should be above b'S'"
    )
    expects(115).to.not_be.above.when.called_with(102).to.have.raised(
        "115 should not be above 102"
    )


def test_to_match():
    "expects().to.match() REGEX"

    expects("ROBSON").to.match(r"(^RO|.OB.{3})")
    expects("robson").to.match(r"(^RO|.OB.{3})", re.I)
    expects("OM").to.match(r"S?[OU][NM]")
    expects("ON").to.match(r"S?[OU][NM]")
    expects("SOM").to.match(r"S?[OU][NM]")
    expects("SON").to.match(r"S?[OU][NM]")
    expects("SUM").to.match(r"S?[OU][MN]")
    expects("SUN").to.match(r"S?[OU][MN]")
    expects("UM").to.match(r"S?[OU][MN]")
    expects("UN").to.match(r"S?[OU][MN]")
    expects("NOS").to_not.match(r"S?[OU][MN]")
    expects(list("OHMS")).to.match.when.called_with("Ω").should.have.raised(
        "['O', 'H', 'M', 'S'] should be a string in order to compare using .match()"
    )
