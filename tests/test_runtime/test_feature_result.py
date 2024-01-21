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
"""tests for :class:`sure.runtime.FeatureResult`"""

import sys
from sure import expects
from sure.doubles import stub
from sure.loader import collapse_path
from sure.runtime import (
    ErrorStack,
    RuntimeContext,
    Scenario,
    ScenarioResult,
    ScenarioResultSet,
    FeatureResult,
    TestLocation,
)

description = "tests for :class:`sure.runtime.FeatureResult`"


def test_feature_result():
    "FeatureResult discerns types of :class:`sure.runtime.ScenarioResult` instances"

    context = stub(RuntimeContext)
    scenario_result_sets = [
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=None)], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=AssertionError('dummy'))], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=ValueError('dummy'), __failure__=None)], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=AssertionError('dummy'))], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=ValueError('dummy'), __failure__=None)], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=AssertionError('dummy'))], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=ValueError('dummy'), __failure__=None)], context=context),
    ]

    feature_result = FeatureResult(scenario_result_sets)

    expects(feature_result).to.have.property('failed_scenarios').being.length_of(3)
    expects(feature_result).to.have.property('errored_scenarios').being.length_of(3)
    expects(feature_result).to.have.property('scenario_results').being.length_of(7)


def test_feature_result_printable_with_failure():
    "Feature.printable presents reference to first failure occurrence"

    context = stub(RuntimeContext)
    scenario_result_sets = [
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=None)], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=AssertionError('dummy'))], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=ValueError('dummy'), __failure__=None)], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=AssertionError('dummy'))], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=ValueError('dummy'), __failure__=None)], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=AssertionError('dummy'))], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=ValueError('dummy'), __failure__=None)], context=context),
    ]

    feature_result = FeatureResult(scenario_result_sets)

    expects(feature_result.printable()).to.equal("AssertionError: dummy")


def test_feature_result_printable_with_error():
    "Feature.printable presents reference to first error occurrence"

    context = stub(RuntimeContext)
    scenario_result_sets = [
        ScenarioResultSet([stub(ScenarioResult, __error__=None, __failure__=None)], context=context),
        ScenarioResultSet([stub(ScenarioResult, __error__=ValueError('dummy'), __failure__=None)], context=context),
    ]

    feature_result = FeatureResult(scenario_result_sets)

    expects(feature_result.printable()).to.equal("ValueError: dummy")
