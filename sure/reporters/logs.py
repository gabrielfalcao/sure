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
import sys
import logging

import sure
from sure.reporter import Reporter


class LogsReporter(Reporter):
    name = "logger"
    logger = logging.getLogger(__name__)

    def initialize(self, logger: logging.Logger = None):
        if not logger:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
        elif isinstance(logger, logging.Logger):
            self.logger = logger
        else:
            raise TypeError(
                f"expeted {logger} to be a {logging.Logger} but got a {type(logger)} instead"
            )

    def on_start(self):
        self.logger.info("test session started")

    def on_feature(self, feature):
        self.logger.info("testing feature: {feature.name}...")

    def on_feature_done(self, feature, result):
        self.logger.info("testing feature: {feature.name}: {result.label}")

    def on_scenario(self, test):
        self.logger.info("testing scenario: {test.name}...")

    def on_scenario_done(self, test, result):
        self.logger.info("testing scenario: {test.name}: {result.label}")

    def on_failure(self, test, error):
        self.logger.warning("failed scenario: {test.name}: {error}")

    def on_success(self, test):
        self.logger.warning("succeeded scenario: {test.name}: {error}")

    def on_error(self, test, error):
        self.logger.error("error scenario: {test.name}: {error}")

    def on_finish(self):
        self.logger.info("test session completed")
