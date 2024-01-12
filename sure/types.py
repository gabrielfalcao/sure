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
from typing import TypeVar


Runner = TypeVar('sure.runner.Runner')
BaseContainer = TypeVar('sure.runtime.BaseContainer')
RuntimeRole = TypeVar('sure.runtime.RuntimeRole')
TestLocation = TypeVar('sure.runtime.TestLocation')
ErrorStack = TypeVar('sure.runtime.ErrorStack')
RuntimeOptions = TypeVar('sure.runtime.RuntimeOptions')
RuntimeContext = TypeVar('sure.runtime.RuntimeContext')
BaseResult = TypeVar('sure.runtime.BaseResult')
Container = TypeVar('sure.runtime.Container')
ScenarioArrangement = TypeVar('sure.runtime.ScenarioArrangement')
Feature = TypeVar('sure.runtime.Feature')
Scenario = TypeVar('sure.runtime.Scenario')
ExceptionManager = TypeVar('sure.runtime.ExceptionManager')
ScenarioResult = TypeVar('sure.runtime.ScenarioResult')
ScenarioResultSet = TypeVar('sure.runtime.ScenarioResultSet')
FeatureResult = TypeVar('sure.runtime.FeatureResult')
FeatureResultSet = TypeVar('sure.runtime.FeatureResultSet')
