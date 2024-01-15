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
import sys, unittest, types
from os.path import isdir
from sure import expects
from collections import OrderedDict
from sure.loader import collapse_path, loader
from sure.runtime import object_name
from sure.runtime import seem_to_indicate_setup
from sure.runtime import seem_to_indicate_teardown
from sure.runtime import seem_to_indicate_test
from sure.runtime import appears_to_be_runnable
from sure.runtime import TestLocation
from sure.runtime import ErrorStack
from sure.runtime import RuntimeContext
from sure.runtime import RuntimeOptions
from sure.runtime import BaseResult
from sure.runtime import Container
from sure.runtime import ScenarioArrangement
from sure.runtime import Feature
from sure.runtime import Scenario
from sure.runtime import ExceptionManager
from sure.runtime import treat_error
from sure.runtime import ScenarioResult
from sure.runtime import ScenarioResultSet
from sure.runtime import FeatureResult
from sure.runtime import FeatureResultSet
from sure.runtime import stripped


loader.load_module(__file__)
description = "tests for :mod:`sure.runtime`"


def test_object_name_for_classes():
    """sure.runtime.object_name() on a class type should return the fqdn"""

    expects(object_name(OrderedDict)).to.equal("collections.OrderedDict")


def test_object_name_for_functions():
    """sure.runtime.object_name() on a function returns its name"""

    expects(object_name(isdir)).to.equal("isdir")


def test_object_name_for_instances():
    """sure.runtime.object_name() on a instances should return the class' fqdn"""

    data = OrderedDict()
    expects(object_name(data)).to.equal("collections.OrderedDict")


def test_seem_to_indicate_setup():
    """sure.runtime.seem_to_indicate_setup() should return ``True`` if the given name matches a certain pattern"""

    expects(seem_to_indicate_setup("setup")).to.be.true
    expects(seem_to_indicate_setup("set_up")).to.be.true
    expects(seem_to_indicate_setup("setUp")).to.be.true
    expects(seem_to_indicate_setup("test_set_up")).to.be.false
    expects(seem_to_indicate_setup("test_setup")).to.be.false
    expects(seem_to_indicate_setup("setup_test")).to.be.false
    expects(seem_to_indicate_setup("set_up_test")).to.be.false
    expects(seem_to_indicate_setup("set_test_up")).to.be.false
    expects(seem_to_indicate_setup("SetUp")).to.be.false
    expects(seem_to_indicate_setup("SETUP")).to.be.false
    expects(seem_to_indicate_setup("teardown")).to.be.false


def test_seem_to_indicate_teardown():
    """sure.runtime.seem_to_indicate_teardown() should return ``True`` if the given name matches a certain pattern"""

    expects(seem_to_indicate_teardown("teardown")).to.be.true
    expects(seem_to_indicate_teardown("tear_down")).to.be.true
    expects(seem_to_indicate_teardown("teardown")).to.be.true
    expects(seem_to_indicate_teardown("test_tear_down")).to.be.false
    expects(seem_to_indicate_teardown("test_teardown")).to.be.false
    expects(seem_to_indicate_teardown("teardown_test")).to.be.false
    expects(seem_to_indicate_teardown("tear_down_test")).to.be.false
    expects(seem_to_indicate_teardown("tear_test_down")).to.be.false
    expects(seem_to_indicate_teardown("Teardown")).to.be.false
    expects(seem_to_indicate_teardown("TEARDOWN")).to.be.false
    expects(seem_to_indicate_teardown("setup")).to.be.false


def test_seem_to_indicate_test():
    """sure.runtime.seem_to_indicate_test() should return ``True`` if the given name matches a certain pattern"""

    expects(seem_to_indicate_test("test_null_hypothesis")).to.be.true
    expects(seem_to_indicate_test("spec_method_of_investigation")).to.be.true
    expects(seem_to_indicate_test("scenario_of_epistomological_inquiry")).to.be.true


def test_appears_to_be_runnable():
    """sure.runtime.appears_to_be_runnable() should return ``True`` if the given name seems to indicate setup, teardown or test"""
    expects(appears_to_be_runnable("setup")).to.be.true
    expects(appears_to_be_runnable("set_up")).to.be.true
    expects(appears_to_be_runnable("setUp")).to.be.true
    expects(appears_to_be_runnable("teardown")).to.be.true
    expects(appears_to_be_runnable("tear_down")).to.be.true
    expects(appears_to_be_runnable("teardown")).to.be.true
    expects(appears_to_be_runnable("test_null_hypothesis")).to.be.true
    expects(appears_to_be_runnable("spec_method_of_investigation")).to.be.true
    expects(appears_to_be_runnable("scenario_of_epistomological_inquiry")).to.be.true


def test_test_location_function():
    """TestLocation() with a function"""

    def dummy_function():
        pass

    location = TestLocation(dummy_function)

    expects(location.name).to.equal("dummy_function")
    expects(location.filename).to.equal(collapse_path(__file__))
    expects(location.line).to.equal(124)
    expects(location.kind).to.equal(types.FunctionType)


def test_test_location_unittest_testcase_subclass():
    """TestLocation() with a unittest.TestCase subclass"""

    class DummyTestCaseA(unittest.TestCase):
        """Dummy Test Case A"""
        def test(self):
            pass

    location = TestLocation(DummyTestCaseA, sys.modules[__name__])

    expects(location.name).to.equal("DummyTestCaseA")
    expects(location.filename).to.equal(collapse_path(__file__))
    expects(location.line).to.equal(138)
    expects(location.kind).to.equal(unittest.TestCase)
    expects(location.description).to.equal("Dummy Test Case A")
    expects(location.ancestral_description).to.equal("tests for :mod:`sure.runtime`")
    expects(repr(location)).to.equal(f'<TestLocation DummyTestCaseA at {collapse_path(__file__)}:138>')
    expects(str(location)).to.equal(f'scenario "Dummy Test Case A" \ndefined at {collapse_path(__file__)}:138')


def test_test_location_unittest_testcase_instance():
    """TestLocation() with a unittest.TestCase instance"""

    class DummyTestCaseB(unittest.TestCase):
        description = "Dummy Test Case B"

        def test(self):
            pass

    location = TestLocation(DummyTestCaseB('test'), sys.modules[__name__])

    expects(location.name).to.equal("DummyTestCaseB")
    expects(location.filename).to.equal(collapse_path(__file__))
    expects(location.line).to.equal(158)
    expects(location.kind).to.equal(unittest.TestCase)
    expects(location.ancestral_description).to.equal("tests for :mod:`sure.runtime`")
    expects(location.description).to.equal("Dummy Test Case B")
    expects(repr(location)).to.equal(f'<TestLocation DummyTestCaseB at {collapse_path(__file__)}:158>')
    expects(str(location)).to.equal(f'scenario "Dummy Test Case B" \ndefined at {collapse_path(__file__)}:158')


def test_test_location_with_user_defined_class():
    """TestLocation() with an instance of user-defined class"""

    class DummyTestCaseY:
        """Dummy Test Case Y"""

    location = TestLocation(DummyTestCaseY(), sys.modules[__name__])

    expects(location.name).to.equal("DummyTestCaseY")
    expects(location.filename).to.equal(collapse_path(__file__))
    expects(location.line).to.equal(179)
    expects(location.kind).to.equal(DummyTestCaseY)
    expects(location.ancestral_description).to.equal("tests for :mod:`sure.runtime`")
    expects(location.description).to.equal("Dummy Test Case Y")
    expects(repr(location)).to.equal(f'<TestLocation DummyTestCaseY at {collapse_path(__file__)}:179>')
    expects(str(location)).to.equal(f'scenario "Dummy Test Case Y" \ndefined at {collapse_path(__file__)}:179')


def test_test_location_nonsupported_types():
    """TestLocation() with builtin types"""

    expects(TestLocation).when.called_with({}).to.throw(
        TypeError,
        f"{{}} of type {dict} is not supported by {TestLocation}"
    )

    expects(TestLocation).when.called_with(set()).to.throw(
        TypeError,
        f"{set()} of type {set} is not supported by {TestLocation}"
    )

    expects(TestLocation).when.called_with([]).to.throw(
        TypeError,
        f"{[]} of type {list} is not supported by {TestLocation}"
    )
