# -*- coding: utf-8 -*-
from sure import that
from unittest import TestCase

feature = "nested tests"


class TestMoor(TestCase):
    "`sure' should recognize nested test classes"

    class TestEggcelent(TestCase):
        "First Nested Test"

        def test_101(self):
            assert that("one").should.equal("one")

        def test_201(self):
            assert that("two").should_not.equal("one")

    class TestAnother(TestCase):
        "Another Nested Test"

        def test_301(self):
            assert that("three").should_not.equal("one")


    class TestContextualized(TestCase):
        "Another Nested Test"

        def setup(self):
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
