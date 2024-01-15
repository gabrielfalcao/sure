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
from mock import patch
from collections import OrderedDict
from sure.loader import collapse_path
from sure.runner import Runner
from sure.reporter import Reporter
from sure.runtime import (
    RuntimeContext,
    TestLocation,
    ScenarioArrangement,
    Scenario,
    RuntimeOptions,
    ScenarioResult,
    RuntimeRole
)
from sure.doubles import Dummy, stub, anything_of_type


description = "tests for :class:`sure.runtime.ScenarioArrangement`"


@patch("sure.runtime.send_runtime_warning")
@patch("sure.runtime.TestLocation")
def test_scenario_arrangement_unexpected_type(TestLocationMock, send_runtime_warning):
    "sure.runtime.ScenarioArrangement should raise TypeError when receiving an unexpected type"

    test_location_stub = stub(
        TestLocation,
        name="test-location-name-dummy",
        filename="dummy-filename.py",
        line=42,
    )
    TestLocationMock.return_value = test_location_stub
    params = dict(
        source=[],
        context=stub(RuntimeContext),
        scenario=stub(Scenario),
        setup_methods=[],
        teardown_methods=[],
        test_methods=[],
        nested_containers=[],
    )

    scenario_arrangement = ScenarioArrangement(**params)

    expects(scenario_arrangement).to.have.property("location").being.equal(
        test_location_stub
    )
    expects(scenario_arrangement).to.have.property("name").being.equal(
        "test-location-name-dummy"
    )
    send_runtime_warning.assert_called_once_with(
        "ScenarioArrangement received unexpected type: [] (<class 'list'>)",
    )


def test_scenario_arrangement_nonunittest_testcase_test():
    "sure.runtime.ScenarioArrangement should accept a non-:class:`unittest.TestCase` test class"

    class TestCaseA:
        def test_method_Z(self):
            pass

    scenario_arrangement = ScenarioArrangement(
        source=TestCaseA,
        context=stub(RuntimeContext),
        scenario=stub(Scenario),
        setup_methods=[],
        teardown_methods=[],
        test_methods=[],
        nested_containers=[],
    )

    expects(scenario_arrangement.name).to.equal("TestCaseA")
    expects(scenario_arrangement).to.have.property("source_instance").being.a(TestCaseA)

    expects(repr(scenario_arrangement)).to.equal(
        f'<ScenarioArrangement:TestCaseA scenario "" \ndefined at {collapse_path(__file__)}:76>'
    )


def test_scenario_arrangement_from_generic_object_receiving_a_class_with_constructor_arguments():
    'sure.runtime.ScenarioArrangement.from_generic_object() when receiving a class whose constructor takes arguments should return an "empty" ScenarioArrangement in terms of runnable methods'

    class TestComplicatedConstructor:
        def __init__(self, param_a, param_b):
            pass

        def test_method_A(self):
            pass

    scenario_arrangement = ScenarioArrangement.from_generic_object(
        TestComplicatedConstructor,
        context=anything_of_type(RuntimeContext),
        scenario=anything_of_type(Scenario),
    )

    expects(scenario_arrangement.name).to.equal("TestComplicatedConstructor")
    expects(scenario_arrangement.test_methods).to.be.empty
    expects(scenario_arrangement.nested_containers).to.be.empty
    expects(scenario_arrangement).to.have.property("runnable").being.a(bool)
    expects(scenario_arrangement.runnable).to.equal(False)


@patch("sure.runtime.send_runtime_warning")
@patch("sure.runtime.TestLocation")
def test_scenario_arrangement_from_generic_object_receiving_an_unexpected_type(
    TestLocationMock, send_runtime_warning
):
    'sure.runtime.ScenarioArrangement.from_generic_object() when receiving an unexpected type should display a warning return an "empty" ScenarioArrangement in terms of runnable methods'

    test_location_stub = stub(
        TestLocation,
        name="test-location-name-dummy",
        filename="dummy-filename.py",
        line=42,
    )
    TestLocationMock.return_value = test_location_stub
    scenario_arrangement = ScenarioArrangement.from_generic_object(
        [],
        context=anything_of_type(RuntimeContext),
        scenario=anything_of_type(Scenario),
    )

    expects(scenario_arrangement.name).to.equal("test-location-name-dummy")
    expects(scenario_arrangement.test_methods).to.be.empty
    expects(scenario_arrangement.nested_containers).to.be.empty
    expects(scenario_arrangement).to.have.property("runnable").being.a(bool)
    expects(scenario_arrangement.runnable).to.equal(False)


def test_scenario_arrangement_from_generic_object_receiving_valid_nonunittest_testcase_testcase_with_nested_cases():
    "sure.runtime.ScenarioArrangement.from_generic_object() should accept a non-:class:`unittest.TestCase` test class"

    class TestCaseC:
        test_attribute = Dummy("test_attribute")

        def test_method_A(self):
            pass

        def test_method_M(self):
            pass

        class TestCaseM:
            def test_method_A(self):
                pass

            def test_method_C(self):
                pass

    scenario_arrangement = ScenarioArrangement.from_generic_object(
        TestCaseC,
        context=stub(RuntimeContext),
        scenario=stub(Scenario),
    )

    expects(scenario_arrangement.name).to.equal("TestCaseC")
    expects(scenario_arrangement.test_methods).to.have.length_of(2)
    expects(scenario_arrangement.nested_containers).to.have.length_of(1)
    expects(scenario_arrangement).to.have.property("runnable").being.a(bool)
    expects(scenario_arrangement.runnable).to_not.be.false


def test_scenario_arrangement_uncollapse_nested():
    "sure.runtime.ScenarioArrangement.uncollapse_nested() should accept a non-:class:`unittest.TestCase` test class"

    class TestCaseD:
        def test_method_B(self):
            pass

        def test_method_N(self):
            pass

        class TestCaseN:
            def test_method_B(self):
                pass

            def test_method_D(self):
                pass

    scenario_arrangements = ScenarioArrangement.from_generic_object(
        TestCaseD,
        context=stub(RuntimeContext),
        scenario=stub(Scenario),
    ).uncollapse_nested()

    expects(scenario_arrangements).to.be.a(list)
    expects(scenario_arrangements).to.have.length_of(2)
    (arrangementA, arrangementZ) = scenario_arrangements

    expects(arrangementA).should.be.a(ScenarioArrangement)
    expects(arrangementA).should.have.property("source_instance").being.a(TestCaseD)
    expects(arrangementZ).should.be.a(ScenarioArrangement)
    expects(arrangementZ).should.have.property("source_instance").being.a(
        TestCaseD.TestCaseN
    )


def test_scenario_arrangement_run_container_success():
    "sure.runtime.ScenarioArrangement.run_container() on success should return a tuple with the result and the RuntimeRole"

    class TestCaseRunContainerSuccess:
        def test_method_A(self):
            assert not False

        def test_method_Z(self):
            assert not False

    runner = stub(Runner)
    reporter = Reporter.from_name_and_runner("test", runner)
    context = RuntimeContext(
        reporter=reporter,
        options=RuntimeOptions(
            immediate=False,
        )
    )
    scenario_arrangement = ScenarioArrangement.from_generic_object(
        TestCaseRunContainerSuccess,
        context=context,
        scenario=stub(Scenario),
    )

    container = scenario_arrangement.test_methods[0]
    return_value = next(scenario_arrangement.run_container(container, context))
    expects(return_value).should.be.a(tuple)
    expects(return_value).should.have.length_of(2)
    scenario_result, role = return_value
    expects(scenario_result).to.be.a(ScenarioResult)
    expects(role).to.equal(RuntimeRole.Unit)
