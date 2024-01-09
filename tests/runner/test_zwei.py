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

import unittest
from unittest import TestCase
from sure import that


feature = "nested tests"


class TestEggcelent(unittest.TestCase):
    "First Nested Test"

    def test_101(self):
        assert "one".should.equal("one")
        assert that("one").should.equal("one")

    def test_201(self):
        assert "one".should.equal("one")
        assert that("two").should_not.equal("one")

    def test_401(self):
        assert that("""
line 1
line 2
line 3
line 4
""").should.be.different_of("""
line 1
line 2
line 5
line 3
line 4
""")

        assert that("""line 1
line 2
line 3
line 4
""").should_not.be.different_of("""line 1
line 2
line 3
line 4
""")

    class TestAnother(TestCase):
        "Another Nested Test"

        def test_301(self):
            assert "three".should.equal("three")
            assert that("three").should.equal("three")
            that("three").should_not.equal("one")
            assert that("three").should_not.equal("one")

    class TestContextualized(TestCase):
        "One More Contextualized Test"

        def setUp(self):
            self.datum = {}

        def test_empty_context(self):
            assert that(self.datum).should.be.empty

        def test_non_ideal_side_effect_0(self):
            self.datum['side-effects'] = 0
            assert that(self.datum).should.equal({
                'side-effects': 0,
            })

        def test_non_ideal_side_effect_1(self):
            assert that(self.datum).should.equal({
                'side-effects': 0,
            })
            self.datum['extra-side-effects'] = {}
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {},
            })

        def test_non_ideal_side_effect_2(self):
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {},
            })
            self.datum['extra-side-effects']['placate-code'] = (
                'tests ideally should not cause side-effects'
            )
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {
                    'placate-code': 'tests ideally should not cause side-effects'
                },
            })

        def test_non_ideal_side_effect_3(self):
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {
                    'placate-code': 'tests ideally should not cause side-effects'
                },
            })
            self.datum['extra-side-effects']['acknowledge-exception'] = (
                "for broad adoption `sure' should support running tests in deterministic, alphabetic order so that existing codebases that rely on side-effects will continue to work as expected"
            )
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {
                    'placate-code': 'tests ideally should not cause side-effects',
                    'acknowledge-exception': "for broad adoption `sure' should support running tests in deterministic, alphabetic order so that existing codebases that rely on side-effects will continue to work as expected"
                },
            })

        def test_non_ideal_side_effect_4(self):
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {
                    'placate-code': 'tests ideally should not cause side-effects',
                    'acknowledge-exception': "for broad adoption `sure' should support running tests in deterministic, alphabetic order so that existing codebases that rely on side-effects will continue to work as expected"
                },
            })
            self.datum['session-1'] = []
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {
                    'placate-code': 'tests ideally should not cause side-effects',
                    'acknowledge-exception': "for broad adoption `sure' should support running tests in deterministic, alphabetic order so that existing codebases that rely on side-effects will continue to work as expected"
                },
                'session-1': [],
            })

        def test_non_ideal_side_effect_5(self):
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {
                    'placate-code': 'tests ideally should not cause side-effects',
                    'acknowledge-exception': "for broad adoption `sure' should support running tests in deterministic, alphabetic order so that existing codebases that rely on side-effects will continue to work as expected"
                },
                'session-1': [],
            })
            self.datum['session-1'].append("The somewhat complex rationale presented in this instance to be quite reasonable thus far")
            assert that(self.datum).should.equal({
                'side-effects': 0,
                'extra-side-effects': {
                    'placate-code': 'tests ideally should not cause side-effects',
                    'acknowledge-exception': "for broad adoption `sure' should support running tests in deterministic, alphabetic order so that existing codebases that rely on side-effects will continue to work as expected"
                },
                'session-1': ["The somewhat complex rationale presented in this instance to be quite reasonable thus far"],
            })
