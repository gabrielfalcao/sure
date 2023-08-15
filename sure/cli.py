import os
from pathlib import Path
import click

from sure.runner import Runner
from sure.importer import resolve_path


@click.command()
@click.argument("paths", nargs=-1)
@click.option("-r", "--reporter", default="feature")
@click.option("-i", "--immediate", is_flag=True)
def entrypoint(paths, reporter, immediate):
    runner = Runner(resolve_path(os.getcwd()), reporter)
    runner.run(paths, immediate=immediate)
