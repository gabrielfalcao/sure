#!/usr/bin/env python3
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
import sys
import logging
from glob import glob
from itertools import chain as flatten
from functools import reduce
from pathlib import Path

import click
import coverage
import threading
import sure.reporters

from sure.loader import resolve_path
from sure.runner import Runner
from sure.runtime import RuntimeOptions
from sure.reporters import gather_reporter_names
from sure.errors import ExitError, ExitFailure, InternalRuntimeError, treat_error


@click.command(no_args_is_help=True)
@click.argument("paths", nargs=-1)
@click.option("-c", "--with-coverage", is_flag=True)
@click.option("-s", "--special-syntax", is_flag=True)
@click.option("-f", "--log-file", help="path to a log file. Default to SURE_LOG_FILE")
@click.option(
    "-l",
    "--log-level",
    type=click.Choice(["debug", "info", "warning", "error"]),
    help="default='info'",
)
@click.option(
    "-x",
    "--immediate",
    is_flag=True,
    help="quit test execution immediately at first failure",
)
@click.option("-i", "--ignore", help="paths to ignore", multiple=True)
@click.option(
    "-r",
    "--reporter",
    default="feature",
    help="default=feature",
    type=click.Choice(gather_reporter_names()),
)
@click.option("--cover-branches", is_flag=True)
@click.option("--cover-module", multiple=True, help="specify module names to cover")
@click.option("--reap-warnings", is_flag=True, help="reaps warnings during runtime and report only at the end of test session")
def entrypoint(
    paths,
    reporter,
    immediate,
    ignore,
    log_level,
    log_file,
    special_syntax,
    with_coverage,
    cover_branches,
    cover_module,
    reap_warnings,
):
    if not paths:
        paths = glob("test*/**")
    else:
        paths = flatten(*list(map(glob, paths)))

    configure_logging(log_level, log_file)
    coverageopts = {
        "auto_data": True,
        "cover_pylib": False,
        "source": cover_module,
        "branch": cover_branches,
        "config_file": True,
    }

    cov = with_coverage and coverage.Coverage(**coverageopts) or None
    if cov:
        cov.erase()
        cov.load()
        cov.start()

    if special_syntax:
        sure.enable_special_syntax()

    options = RuntimeOptions(immediate=immediate, ignore=ignore, reap_warnings=reap_warnings)
    runner = Runner(resolve_path(os.getcwd()), reporter, options)
    try:
        result = runner.run(paths)
    except Exception as e:
        raise InternalRuntimeError(runner.context, treat_error(e))

    if result:
        if result.is_failure:
            raise ExitFailure(runner.context, result)

        elif result.is_error:
            raise ExitError(runner.context, result)

        elif cov:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            cov.stop()
            cov.save()
            cov.report()


def configure_logging(log_level: str, log_file: str):
    if not log_level:
        log_level = "none"

    if not isinstance(log_level, str):
        raise TypeError(
            f"log_level should be a string but is {log_level}({type(log_level)}) instead"
        )
    log_level = log_level.lower() == "none" and "info" or log_level

    level = getattr(logging, log_level.upper())

    if log_file:
        log_directory = Path(log_file).parent()
        if log_directory.exists():
            raise RuntimeError(
                f"the log path {log_directory} exists but is not a directory"
            )
        log_directory.mkdir(parents=True, exists_ok=True)

        handler = logging.FileHandler(log_file)
    else:
        handler = logging.NullHandler()

    handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
