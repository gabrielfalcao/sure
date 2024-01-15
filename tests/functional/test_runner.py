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
"functional tests for :mod:`sure.runner`"

import os
import unittest
from pathlib import Path
from sure import expects
from sure.doubles.dummies import anything_of_type
from sure.errors import collapse_path
from sure.runner import Runner
from sure.runtime import (
    Feature,
    FeatureResult,
    RuntimeOptions,
    Scenario,
    ScenarioResult,
    ScenarioResultSet,
    TestLocation,
    FeatureResultSet, RuntimeContext
)
from sure.reporters import test

modules_path = Path(__file__).parent.joinpath("modules")
success_modules_path = modules_path.joinpath("success")
failure_modules_path = modules_path.joinpath("failure")
error_modules_path = modules_path.joinpath("error")


def test_runner_load_features_from_module_containing_unittest_cases():
    "sure.runner.Runner.load_features(path) where `path' points to a python file should return a list of :class:`~sure.runtime.Feature` instances"

    runner = Runner(
        base_path=Path(os.getcwd()),
        reporter="test",
        options=RuntimeOptions(immediate=False, glob_pattern="**module_with*.py"),
    )

    unittest_testcases_module_path = success_modules_path.joinpath(
        "module_with_unittest_test_cases.py"
    )
    features = runner.load_features([unittest_testcases_module_path])

    expects(features).to.be.a(list)
    expects(features).to.have.length_of(1)

    (feature,) = features

    expects(feature).to.be.a(Feature)
    expects(feature).to.have.property("description").being.equal(
        "Module with :class:`unittest.TestCase` subclasses"
    )
    expects(feature).to.have.property("name").being.equal(
        "tests.functional.modules.success.module_with_unittest_test_cases"
    )
    expects(feature).to.have.property("ready").being.equal(True)
    expects(feature).to.have.property("scenarios").being.a(list)
    expects(feature.scenarios).to.have.length_of(2)
    (scenarioA, scenarioB) = feature.scenarios
    expects(scenarioA).to.be.a(Scenario)
    expects(scenarioB).to.be.a(Scenario)

    expects(scenarioA.name).to.equal("TestCaseA")
    expects(scenarioA.description).to.equal("Description of TestCaseA")
    expects(scenarioA.location).to.be.a(TestLocation)
    expects(scenarioA.location.path_and_lineno).to.equal(
        f"{collapse_path(unittest_testcases_module_path)}:23"
    )

    expects(scenarioB.name).to.equal("TestCaseB")
    expects(scenarioB.description).to.be.empty
    expects(scenarioB.location).to.be.a(TestLocation)
    expects(scenarioB.location.path_and_lineno).to.equal(
        f"{collapse_path(unittest_testcases_module_path)}:35"
    )


def test_runner_load_features_from_module_path_recursively():
    "sure.runner.Runner.load_features(path) where `path' points to a directory containing valid python files should return a list of :class:`~sure.runtime.Feature` instances"

    runner = Runner(
        base_path=Path(os.getcwd()),
        reporter="test",
        options=RuntimeOptions(immediate=False, glob_pattern="**module_with*.py"),
    )

    features = runner.load_features([success_modules_path])

    expects(features).to.be.a(list)
    expects(features).to.have.length_of(4)

    (featureA, featureB, featureC, featureX) = features

    expects(featureA).to.equal
    expects(featureA).to.be.a(Feature)
    expects(featureA).to.have.property("name").being.equal(
        "tests.functional.modules.success.module_with_function_members"
    )
    expects(featureA).to.have.property("ready").being.equal(True)
    expects(featureA).to.have.property("scenarios").being.a(list)
    expects(featureA.scenarios).to.have.length_of(6)

    expects(featureB).to.equal
    expects(featureB).to.be.a(Feature)
    expects(featureB).to.have.property("name").being.equal(
        "tests.functional.modules.success.module_with_members"

    )
    expects(featureB).to.have.property("ready").being.equal(True)
    expects(featureB).to.have.property("scenarios").being.a(list)
    expects(featureB.scenarios).to.have.length_of(5)

    expects(featureC).to.equal
    expects(featureC).to.be.a(Feature)
    expects(featureC).to.have.property("name").being.equal(
        "tests.functional.modules.success.module_with_nonunittest_test_cases"
    )
    expects(featureC).to.have.property("ready").being.equal(True)
    expects(featureC).to.have.property("scenarios").being.a(list)
    expects(featureC.scenarios).to.have.length_of(2)

    expects(featureX).to.equal
    expects(featureX).to.be.a(Feature)
    expects(featureX).to.have.property("name").being.equal(
        "tests.functional.modules.success.module_with_unittest_test_cases"
    )
    expects(featureX).to.have.property("ready").being.equal(True)
    expects(featureX).to.have.property("scenarios").being.a(list)
    expects(featureX.scenarios).to.have.length_of(2)


def test_runner_load_features_from_directory_with_python_files():
    "sure.runner.Runner.load_features(path) where `path' points to a python file should return a list of :class:`~sure.runtime.Feature` instances"

    runner = Runner(
        base_path=Path(os.getcwd()),
        reporter="test",
        options=RuntimeOptions(immediate=False, glob_pattern="**module_with*.py"),
    )

    unittest_testcases_module_path = success_modules_path.joinpath(
        "module_with_unittest_test_cases.py"
    )
    features = runner.load_features([unittest_testcases_module_path])

    expects(features).to.be.a(list)
    expects(features).to.have.length_of(1)

    (feature,) = features

    expects(feature).to.be.a(Feature)
    expects(feature).to.have.property("description").being.equal(
        "Module with :class:`unittest.TestCase` subclasses"
    )
    expects(feature).to.have.property("name").being.equal(
        "tests.functional.modules.success.module_with_unittest_test_cases"
    )
    expects(feature).to.have.property("ready").being.equal(True)
    expects(feature).to.have.property("scenarios").being.a(list)
    expects(feature.scenarios).to.have.length_of(2)
    (scenarioA, scenarioB) = feature.scenarios
    expects(scenarioA).to.be.a(Scenario)
    expects(scenarioB).to.be.a(Scenario)

    expects(scenarioA.name).to.equal("TestCaseA")
    expects(scenarioA.description).to.equal("Description of TestCaseA")
    expects(scenarioA.location).to.be.a(TestLocation)
    expects(scenarioA.location.path_and_lineno).to.equal(
        f"{collapse_path(unittest_testcases_module_path)}:23"
    )

    expects(scenarioB.name).to.equal("TestCaseB")
    expects(scenarioB.description).to.be.empty
    expects(scenarioB.location).to.be.a(TestLocation)
    expects(scenarioB.location.path_and_lineno).to.equal(
        f"{collapse_path(unittest_testcases_module_path)}:35"
    )


def test_runner_execute_success_tests():
    "sure.runner.Runner.execute(path) where `path' points to a directory containing valid python files should run tests"

    runner = Runner(
        base_path=Path(os.getcwd()),
        reporter="test",
        options=RuntimeOptions(immediate=False, glob_pattern="**module_with*.py"),
    )

    feature_result_set = runner.execute([success_modules_path])
    expects(feature_result_set).to.be.a(FeatureResultSet)
    expects(feature_result_set).to.have.property("feature_results").being.length_of(4)
    expects(feature_result_set).to.have.property("failed_features").being.empty
    expects(feature_result_set).to.have.property("errored_scenarios").being.empty

    expects(dict(test.events)).to.equal(
        {
            "on_start": [(anything_of_type(float),)],
            "on_feature": [
                (
                    anything_of_type(float),
                    "tests.functional.modules.success.module_with_function_members",
                ),
                (
                    anything_of_type(float),
                    "tests.functional.modules.success.module_with_members",
                ),
                (
                    anything_of_type(float),
                    "tests.functional.modules.success.module_with_nonunittest_test_cases",
                ),
                (
                    anything_of_type(float),
                    "tests.functional.modules.success.module_with_unittest_test_cases",
                ),
            ],
            "on_scenario": [
                (anything_of_type(float), "test_function_A"),
                (anything_of_type(float), "test_function_B"),
                (anything_of_type(float), "test_function_C"),
                (anything_of_type(float), "test_function_X"),
                (anything_of_type(float), "test_function_Y"),
                (anything_of_type(float), "test_function_Z"),
                (anything_of_type(float), "TestCase"),
                (anything_of_type(float), "UnitCase"),
                (anything_of_type(float), "test_function_A"),
                (anything_of_type(float), "test_function_B"),
                (anything_of_type(float), "test_function_C"),
                (anything_of_type(float), "TestCaseA"),
                (anything_of_type(float), "TestCaseA"),
                (anything_of_type(float), "TestCaseA"),
                (anything_of_type(float), "TestCaseA"),
                (anything_of_type(float), "TestCaseB"),
                (anything_of_type(float), "TestCaseB"),
                (anything_of_type(float), "TestCaseB"),
                (anything_of_type(float), "TestCaseB"),
                (anything_of_type(float), "TestCaseA"),
                (anything_of_type(float), "TestCaseA"),
                (anything_of_type(float), "TestCaseA"),
                (anything_of_type(float), "TestCaseA"),
                (anything_of_type(float), "TestCaseB"),
                (anything_of_type(float), "TestCaseB"),
                (anything_of_type(float), "TestCaseB"),
                (anything_of_type(float), "TestCaseB"),
            ],
            "on_scenario_done": [
                (anything_of_type(float), "test_function_A", "ok"),
                (anything_of_type(float), "test_function_B", "ok"),
                (anything_of_type(float), "test_function_C", "ok"),
                (anything_of_type(float), "test_function_X", "ok"),
                (anything_of_type(float), "test_function_Y", "ok"),
                (anything_of_type(float), "test_function_Z", "ok"),
                (anything_of_type(float), "TestCase", "ok"),
                (anything_of_type(float), "UnitCase", "ok"),
                (anything_of_type(float), "test_function_A", "ok"),
                (anything_of_type(float), "test_function_B", "ok"),
                (anything_of_type(float), "test_function_C", "ok"),
                (anything_of_type(float), "TestCaseA", "ok"),
                (anything_of_type(float), "TestCaseA", "ok"),
                (anything_of_type(float), "TestCaseA", "ok"),
                (anything_of_type(float), "TestCaseA", "ok"),
                (anything_of_type(float), "TestCaseB", "ok"),
                (anything_of_type(float), "TestCaseB", "ok"),
                (anything_of_type(float), "TestCaseB", "ok"),
                (anything_of_type(float), "TestCaseB", "ok"),
                (anything_of_type(float), "TestCaseA", "ok"),
                (anything_of_type(float), "TestCaseA", "ok"),
                (anything_of_type(float), "TestCaseA", "ok"),
                (anything_of_type(float), "TestCaseA", "ok"),
                (anything_of_type(float), "TestCaseB", "ok"),
                (anything_of_type(float), "TestCaseB", "ok"),
                (anything_of_type(float), "TestCaseB", "ok"),
                (anything_of_type(float), "TestCaseB", "ok"),
            ],
            "on_feature_done": [
                (
                    anything_of_type(float),
                    "tests.functional.modules.success.module_with_function_members",
                    "ok",
                ),
                (
                    anything_of_type(float),
                    "tests.functional.modules.success.module_with_members",
                    "ok",
                ),
                (
                    anything_of_type(float),
                    "tests.functional.modules.success.module_with_nonunittest_test_cases",
                    "ok",
                ),
                (
                    anything_of_type(float),
                    "tests.functional.modules.success.module_with_unittest_test_cases",
                    "ok",
                ),
            ],
            "on_finish": [(anything_of_type(float), anything_of_type(RuntimeContext))],
        }
    )
