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

import os
import sys
import logging
from glob import glob
from itertools import chain as flatten
from functools import reduce
from pathlib import Path

import click
import sure.reporters

from sure.importer import resolve_path
from sure.runner import Runner
from sure.reporters import gather_reporter_names
from sure.errors import ExitError, ExitFailure


@click.command(no_args_is_help=True)
@click.argument("paths", nargs=-1)
@click.option("-r", "--reporter", default="feature", help='default=feature', type=click.Choice(gather_reporter_names()))
@click.option("-R", "--reporters", multiple=True, help=f"options=[{','.join(gather_reporter_names())}]")
@click.option("-i", "--immediate", is_flag=True)
@click.option("-l", "--log-level", type=click.Choice(['none', 'debug', 'info', 'warning', 'error']), help="default='none'")
@click.option("-F", "--log-file", help='path to a log file. Default to SURE_LOG_FILE')
@click.option("-v", "--verbose", is_flag=True, multiple=True)
@click.option("-q", "--quiet", is_flag=True, multiple=True)
def entrypoint(paths, reporter, reporters, immediate, log_level, log_file, verbose, quiet):
    if not paths:
        paths = glob('test*/**')
    else:
        paths = flatten(*list(map(glob, paths)))

    reporters = reporters and list(reporters) or None
    verbosity_level = sum(verbose)
    quietness_level = sum(quiet)
    verbosity = verbosity_level - quietness_level
    quietness = quietness_level - verbosity_level

    configure_logging(log_level, log_file)
    runner = Runner(resolve_path(os.getcwd()), reporter, reporters)
    result = runner.run(paths, immediate=immediate)

    if result:
        if result.is_failure:
            raise ExitFailure(runner.context, result)

        if result.is_error:
            raise ExitError(runner.context, result)


def configure_logging(log_level: str, log_file: str):
    if not isinstance(log_level, str) or log_level.lower() == 'none':
        return

    level = getattr(logging, log_level.upper())

    if log_file:
        log_directory = Path(log_file).parent()
        if log_directory.exists():
            raise RuntimeError(f'the log path {log_directory} exists but is not a directory')
        log_directory.mkdir(parents=True, exists_ok=True)

        handler = logging.FileHandler(log_file)
    else:
        handler = logging.NullHandler()

    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
