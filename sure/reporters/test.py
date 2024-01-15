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

import time
from collections import defaultdict
from typing import Union
from sure.reporter import Reporter
from sure.runtime import (
    Feature,
    FeatureResult,
    Scenario,
    ScenarioResult,
    ScenarioResultSet,
    TestLocation,
    ErrorStack,
    RuntimeContext,
)


events = defaultdict(list)


class TestReporter(Reporter):
    """Reporter intented exclusively for testing sure itself"""

    name = "test"

    def on_start(self):
        events["on_start"].append((time.time(),))

    def on_feature(self, feature: Feature):
        events["on_feature"].append((time.time(), feature.name))

    def on_feature_done(self, feature: Feature, result: FeatureResult):
        events["on_feature_done"].append(
            (time.time(), feature.name, result.label.lower())
        )

    def on_scenario(self, scenario: Scenario):
        events["on_scenario"].append((time.time(), scenario.name))

    def on_scenario_done(
        self, scenario: Scenario, result: Union[ScenarioResult, ScenarioResultSet]
    ):
        events["on_scenario_done"].append(
            (time.time(), scenario.name, result.label.lower())
        )

    def on_failure(self, test: Scenario, result: ScenarioResult):
        events["on_failure"].append((time.time(), test.name, result.label.lower()))

    def on_success(self, test: Scenario):
        events["on_success"].append((time.time(), test.name))

    def on_error(self, test: Scenario, result: ScenarioResult):
        events["on_error"].append((time.time(), test.name, result.label.lower()))

    def on_internal_runtime_error(self, context: RuntimeContext, error: ErrorStack):
        events["on_internal_runtime_error"].append((time.time(), context, error))

    def on_finish(self, context: RuntimeContext):
        events["on_finish"].append((time.time(), context))
