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
from unittest.mock import patch, call
from unittest.mock import Mock as Spy
from sure import expects
from sure.runner import Runner
from sure.runtime import Feature
from sure.reporters import FeatureReporter
from sure.doubles import stub


def test_feature_reporter_on_start():
    "FeatureReporter.on_start"

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_start()

    expects(sh.mock_calls).to.equal([call.reset("\n")])


def test_feature_reporter_on_feature():
    "FeatureReporter.on_feature"

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_feature(stub(Feature, name="stubbed feature"))

    expects(sh.mock_calls).to.equal(
        [
            call.reset("  "),
            call.bold_blue("Feature: "),
            call.yellow("'"),
            call.green("stubbed feature"),
            call.yellow("'"),
            call.reset(" "),
        ]
    )


def test_feature_reporter_on_feature_done():
    "FeatureReporter.on_feature_done"

    sh = Spy(name="Shell")
    reporter = FeatureReporter(stub(Runner))
    reporter.sh = sh
    reporter.on_feature_done(
        stub(Feature, name="stubbed feature"),
        Spy(name='feature_result'),
    )

    expects(sh.mock_calls).to.equal(
        [
            call.reset("\n\n"),
        ]
    )
