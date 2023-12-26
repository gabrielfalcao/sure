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
import coverage

import sure.reporters

from sure.loader import resolve_path
from sure.runner import Runner
from sure.reporters import gather_reporter_names
from sure.errors import ExitError, ExitFailure, InternalRuntimeError


@click.command(no_args_is_help=True)
@click.argument("paths", nargs=-1)
@click.option("-r", "--reporter", default="feature", help='default=feature', type=click.Choice(gather_reporter_names()))
@click.option("-i", "--immediate", is_flag=True)
@click.option("-l", "--log-level", type=click.Choice(['none', 'debug', 'info', 'warning', 'error']), help="default='none'")
@click.option("-F", "--log-file", help='path to a log file. Default to SURE_LOG_FILE')
@click.option("-s", "--syntax-magic", is_flag=True)
@click.option("-c", "--with-coverage", is_flag=True)
@click.option("--cover-branches", is_flag=True)
@click.option("--cover-module", multiple=True, help="specify module names to cover")
def entrypoint(paths, reporter, immediate, log_level, log_file, syntax_magic, with_coverage, cover_branches, cover_module):
    if not paths:
        paths = glob('test*/**')
    else:
        paths = flatten(*list(map(glob, paths)))

    configure_logging(log_level, log_file)

    coverageopts = {
        'auto_data': True,
        'cover_pylib': False,
        'source': cover_module,
        'branch': cover_branches,
        'config_file': True,
    }
    cov = with_coverage and coverage.Coverage(**coverageopts) or None
    if cov:
        cov.erase()
        cov.load()
        cov.start()

    if syntax_magic:
        sure.enable_magic_syntax()

    runner = Runner(resolve_path(os.getcwd()), reporter)
    try:
        result = runner.run(paths, immediate=immediate)
    except Exception as e:
        raise InternalRuntimeError(runner.context, e)

    if result:
        if cov:
            cov.stop()
            cov.save()
            cov.report()

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
