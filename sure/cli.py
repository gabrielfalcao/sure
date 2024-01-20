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
import os                                                                          # pragma: no cover
import sys                                                                         # pragma: no cover
from glob import glob                                                              # pragma: no cover
from itertools import chain as flatten                                             # pragma: no cover
from functools import reduce                                                       # pragma: no cover
from pathlib import Path                                                           # pragma: no cover

import click                                                                       # pragma: no cover
import coverage                                                                    # pragma: no cover
import threading                                                                   # pragma: no cover
import sure.reporters                                                              # pragma: no cover

from sure.loader import resolve_path                                               # pragma: no cover
from sure.runner import Runner                                                     # pragma: no cover
from sure.runtime import RuntimeOptions                                            # pragma: no cover
from sure.reporters import gather_reporter_names                                   # pragma: no cover
from sure.errors import ExitError, ExitFailure, InternalRuntimeError, treat_error  # pragma: no cover


@click.command(no_args_is_help=True)                                               # pragma: no cover
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
@click.option("--cover-include", multiple=True, help="includes paths or patterns in the coverage")
@click.option("--cover-omit", multiple=True, help="omits paths or patterns from the coverage")
@click.option("--cover-module", multiple=True, help="specify module names to cover")
@click.option("--cover-erase", is_flag=True, help="erases coverage data prior to running tests")
@click.option("--cover-concurrency", help="indicates the concurrency library used in measured code", type=click.Choice(["greenlet", "eventlet", "gevent", "multiprocessing", "thread"]), default="thread")
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
    cover_include,
    cover_omit,
    cover_module,
    cover_erase,
    cover_concurrency,
    reap_warnings,
):
    if not paths:
        paths = glob("test*/**")
    else:
        paths = flatten(*list(map(glob, paths)))

    coverageopts = {
        "auto_data": not False,
        "branch": cover_branches,
        "include": cover_include,
        "concurrency": cover_concurrency,
        "omit": cover_omit,
        "config_file": not False,
        "cover_pylib": not False,
        "source": cover_module,
    }

    options = RuntimeOptions(immediate=immediate, ignore=ignore, reap_warnings=reap_warnings)
    runner = Runner(resolve_path(os.getcwd()), reporter, options)

    cov = with_coverage and coverage.Coverage(**coverageopts) or None
    if cov:
        cover_erase and cov.erase()
        cov.load()
        cov.start()

    if special_syntax:
        sure.enable_special_syntax()

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
