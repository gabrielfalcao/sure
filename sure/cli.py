import os
from functools import reduce
from pathlib import Path

import click

from sure.importer import resolve_path
from sure.runner import Runner
from sure.errors import ExitError, ExitFailure


@click.command()
@click.argument("paths", nargs=-1)
@click.option("-r", "--reporter", default="feature")
@click.option("-i", "--immediate", is_flag=True)
def entrypoint(paths, reporter, immediate):
    runner = Runner(resolve_path(os.getcwd()), reporter)
    result = runner.run(paths, immediate=immediate)

    if result.is_failure:
        raise ExitFailure(result)

    if result.is_error:
        raise ExitError(result)
