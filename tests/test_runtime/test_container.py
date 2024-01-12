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
from collections import OrderedDict
from sure.loader import collapse_path
from sure.runtime import Container, TestLocation, Scenario
from sure.doubles import Dummy, stub


description = "tests for :class:`sure.runtime.Container`"


def test_container_unit():
    "sure.runtime.Container.unit returns the given runnable"

    def dynamic():
        return "balance"

    module_dummy = Dummy("module_or_instance")
    scenario_stub = stub(Scenario, name="Scenario Stub")
    container = Container(
        "test", dynamic, scenario=scenario_stub, module_or_instance=module_dummy
    )

    expects(container.unit()).to.equal("balance")
    expects(container.name).to.equal("test")
    expects(container.runnable).to.equal(dynamic)
    expects(container.module_or_instance).to.equal(module_dummy)
    expects(container.location).to.be.a(TestLocation)
    expects(repr(container)).to.equal(
        f"<Container of {dynamic} at {collapse_path(__file__)}:30>"
    )
