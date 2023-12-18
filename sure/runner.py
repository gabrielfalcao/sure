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
import os
import re
import sys
import types
import inspect
import unittest
import traceback

import coverage

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
from sure.importer import importer
from sure.reporter import Reporter


class Runner(object):
    """Manages I/O operations in regards to finding tests and executing them"""

    def __init__(self, base_path: Path, reporter: str, reporters: Optional[List[str]] = None, plugin_paths=None, **kwargs):
        self.base_path = base_path
        if isinstance(reporters, list) and len(reporters) > 0:
            self.reporter = CoReporter(map(self.get_reporter, reporters))
        else:
            self.reporter = self.get_reporter(reporter)

        for k in kwargs:
            setattr(self, k, kwargs.get(k))

    def __repr__(self):
        return "<Runner: {} {}>".format(self.base_path, self.reporter)

    def get_reporter(self, name):
        return Reporter.from_name_and_runner(name, self)

    def find_candidates(self, lookup_paths):
        candidate_modules = []
        for path in lookup_paths:
            modules = importer.load_recursive(path, glob_pattern="test*.py")
            candidate_modules.extend(modules)

        return candidate_modules

    def is_runnable_test(self, item):
        if isinstance(item, type):
            if not issubclass(item, unittest.TestCase):
                return
            if item == unittest.TestCase:
                return

        elif not isinstance(item, types.FunctionType):
            return

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

    def runin(self, lookup_paths, immediate: bool = False, with_coverage: bool = False, cover_branches: bool = False, cover_module: Optional[List[str]] = None):
        results = []
        self.reporter.on_start()

        coverageopts = {
            'auto_data': True,
            'cover_pylib': False,
            'source': cover_module,
            'branch': cover_branches,
            'config_file': True,
        }
        cov = with_coverage and coverage.Coverage(**coverageopts) or None

        if cov:
            cov.load()
            cov.start()

        for feature in self.load_features(lookup_paths):
            self.reporter.on_feature(feature)
            runtime = RuntimeOptions(immediate=immediate)
            context = RuntimeContext(self.reporter, runtime)

            result = feature.run(self.reporter, runtime=runtime)
            try:
                if runtime.immediate:
                    if result.is_failure:
                        raise ExitFailure(context, result)

                    if result.is_error:
                        raise ExitError(context, result)
            finally:
                if cov and runtime.immediate and (result.is_error or result.is_failure):
                    cov.stop()
                    cov.save()
                    cov.report()

            results.append(result)
            self.reporter.on_feature_done(feature, result)

        if cov:
            cov.stop()
            cov.save()
        self.reporter.on_finish()
        if cov:
            cov.report()

        return FeatureResultSet(results)

    def run(self, *args, **kwargs):
        try:
            return self.runin(*args, **kwargs)
        except ImmediateFailure as failure:
            # self.reporter.on_failure(failure.scenario, failure)
            return failure.result

        except ImmediateError as error:
            # self.reporter.on_error(failure.scenario, error)
            return error.result

    @cached_property
    def runtime(self, immediate: bool = False):
        return RuntimeOptions(immediate=immediate)

    @cached_property
    def context(self):
        return RuntimeContext(self.reporter, self.runtime)
