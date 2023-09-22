#!/usr/bin/env python3
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
from typing import Iterable

from couleur import Shell

import sure
from sure.agents import Agent
from sure.reporter import Reporter

sh = Shell()


class CoReporter(Reporter):
    name = '__meta__'

    def __init__(self, runner, liaison_with: Iterable[Reporter]):
        for possible_liaison in liaison_with:
            if not isinstance(possible_liaison, Reporter):
                raise TypeError(f'CoReporter takes a set of reporters to broadcast data to, but got {possible_liaison:r} instead')

        self.liaisons = liaison_with
        super().__init__(runner)

    def on_start(self):
        for liaison in self.liaisons:
            liaison.on_start()

    def on_feature(self, feature):
        for liaison in self.liaisons:
            liaison.on_feature(feature)

    def on_feature_done(self, feature, result):
        for liaison in self.liaisons:
            liaison.on_feature_done(feature, result)

    def on_scenario(self, test):
        for liaison in self.liaisons:
            liaison.on_scenario(test)

    def on_scenario_done(self, test, result):
        for liaison in self.liaisons:
            liaison.on_scenario_done(test, result)

    def on_failure(self, test, error):
        for liaison in self.liaisons:
            liaison.on_failure(test, result)

    def on_success(self, test):
        for liaison in self.liaisons:
            liaison.on_success(test)

    def on_error(self, test, error):
        for liaison in self.liaisons:
            liaison.on_error(test, error)

    def on_finish(self):
        for liaison in self.liaisons:
            liaison.on_finish()
