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
import os
import re
import sys
import types
import inspect
import unittest
import traceback

from pathlib import Path
from typing import List, Optional
from functools import lru_cache, cached_property

from sure.errors import ExitError, ExitFailure, ImmediateError, ImmediateFailure
from sure.runtime import (
    Feature,
    Scenario,
    BaseResult,
    ErrorStack,
    RuntimeContext,
    FeatureResult,
    RuntimeOptions,
    ScenarioResult,
    FeatureResultSet,
    ScenarioResultSet,
    stripped,
    seem_to_indicate_test,
)
from sure.loader import loader
from sure.reporter import Reporter


class Runner(object):
    """Manages I/O operations in regards to finding tests and executing them"""

    def __init__(self, base_path: Path, reporter: str, options: RuntimeOptions, **kwds):
        self.base_path = base_path
        self.reporter = self.get_reporter(reporter)
        self.options = options
        self.kwds = kwds

    def __repr__(self):
        return "<Runner: {} {}>".format(self.base_path, self.reporter)

    def get_reporter(self, name):
        return Reporter.from_name_and_runner(name, self)

    def find_candidates(self, lookup_paths):
        candidate_modules = []
        for path in lookup_paths:
            modules = loader.load_recursive(
                path, glob_pattern="test*.py", excludes=self.options.ignore
            )
            candidate_modules.extend(modules)

        return candidate_modules

    def is_runnable_test(self, item) -> bool:
        if isinstance(item, type):
            if not issubclass(item, unittest.TestCase):
                return False
            if item == unittest.TestCase:
                return False

        elif not isinstance(item, types.FunctionType):
            return False

        name = getattr(item, "__name__", None)
        return seem_to_indicate_test(name)

    def extract_members(self, candidate):
        all_members = [m[1] for m in inspect.getmembers(candidate)]
        members = list(filter(self.is_runnable_test, all_members))
        return candidate, members

    def load_features(self, lookup_paths):
        features = []
        cases = []
        candidates = self.find_candidates(lookup_paths)
        for module, executables in map(self.extract_members, candidates):
            feature = Feature(module)
            cases.extend(feature.read_scenarios(executables))
            features.append(feature)

        return features

    def execute(self, lookup_paths):
        results = []
        self.reporter.on_start()

        for feature in self.load_features(lookup_paths):
            self.reporter.on_feature(feature)
            context = RuntimeContext(self.reporter, self.options)

            result = feature.run(self.reporter, runtime=self.options)
            if self.options.immediate:
                if result.is_failure:
                    raise ExitFailure(context, result)

                if result.is_error:
                    raise ExitError(context, result)

            results.append(result)
            self.reporter.on_feature_done(feature, result)

        self.reporter.on_finish()
        return FeatureResultSet(results)

    def run(self, *args, **kwargs):
        try:
            return self.execute(*args, **kwargs)
        except ImmediateFailure as failure:
            self.reporter.on_failure(failure.scenario, failure.result)
            return failure.result

        except ImmediateError as error:
            self.reporter.on_error(error.scenario, error.result)
            return error.result

    @cached_property
    def context(self):
        return RuntimeContext(self.reporter, self.options)
