# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2023>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from sure.reporter import Reporter


events = defaultdict(list)


class TestReporter(Reporter):
    """Reporter intented exclusively for testing sure itself"""
    name = "test"

    def on_start(self):
        events['on_start'].append((time.time(), ))

    def on_feature(self, feature):
        events['on_feature'].append((time.time(), feature))

    def on_feature_done(self, feature, result):
        events['on_feature_done'].append((time.time(), feature, result))

    def on_scenario(self, test):
        events['on_scenario'].append((time.time(), test))

    def on_scenario_done(self, test, result):
        events['on_scenario_done'].append((time.time(), test, result))

    def on_failure(self, test, result):
        events['on_failure'].append((time.time(), test, result))

    def on_success(self, test):
        events['on_test'].append((time.time(), test))

    def on_error(self, test, result):
        events['on_error'].append((time.time(), test, result))

    def on_internal_runtime_error(self, context, error):
        events['on_internal_runtime_error'].append((time.time(), context, error))

    def on_finish(self):
        events['on_finish'].append((time.time(), ))
