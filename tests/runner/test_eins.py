# -*- coding: utf-8 -*-
from unittest import TestCase

feature = "test sure runner"


def test_function_ok():
    "testing successful function with sure runner"
    assert True


def test_function_fail():
    "testing failing function with sure runner"
    assert False, 'the failure appears to be right'


class TestClass(TestCase):
    "`sure' should work seamlessly with a unittest.TestCase"

    def setUp(self):
        self.one_attribute = {
            'question': 'does it work for us?'
        }

    def tearDown(self):
        self.one_attribute.pop('question')

    def test_expected_attribute_exists(self):
        "the setUp should work in our favor or else everything is unambiguously lost"
        assert hasattr(self, 'one_attribute'), f'{self} should have one_attribute but does not appear so'
