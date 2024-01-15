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
from mock import patch
from sure import expects
from sure.doubles import stub
from sure.runtime import RuntimeContext, RuntimeOptions
from sure.reporter import Reporter


description = "tests for :class:`sure.runtime.RuntimeContext`"


@patch('sure.runtime.WarningReaper')
def test_runtime_context(WarningReaper):
    """sure.runtime.RuntimeContext"""

    options_dummy = RuntimeOptions(immediate=False, reap_warnings=True)
    reporter_stub = stub(Reporter)

    context = RuntimeContext(reporter_stub, options_dummy, "dummy_test_name")

    expects(context).to.have.property("reporter").being.equal(reporter_stub)
    expects(context).to.have.property("options").being.equal(options_dummy)
    expects(context).to.have.property("unittest_testcase_method_name").being.equal(
        "dummy_test_name"
    )

    expects(repr(context)).to.equal(
        "<RuntimeContext reporter=<ReporterStub> options=<RuntimeOptions immediate=False glob_pattern='**test*.py' reap_warnings=True>>"
    )
    WarningReaper.assert_called_once_with()
    WarningReaper.return_value.enable_capture.assert_called_once_with()
