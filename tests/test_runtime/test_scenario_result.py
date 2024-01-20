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
"""tests for :class:`sure.runtime.ScenarioResult`"""

import sys
from sure import expects
from sure.doubles import stub
from sure.loader import collapse_path
from sure.runtime import (
    ScenarioResult,
    Scenario,
    TestLocation,
    RuntimeContext,
    ErrorStack,
)


description = "tests for :class:`sure.runtime.ScenarioResult`"


def test_scenario_result_printable():
    "meth:`ScenarioResult.printable` returns its location as string"

    location = TestLocation(test_scenario_result_printable)
    scenario = stub(Scenario)
    context = stub(RuntimeContext)
    scenario_result = ScenarioResult(
        scenario=scenario, location=location, context=context, error=None
    )

    expects(scenario_result.printable()).to.equal(
        (
            'scenario "meth:`ScenarioResult.printable` returns its location as string" \n'
            "defined at "
            f"{collapse_path(__file__)}:35"
        )
    )
