import json
import os
import re

import click
from dgctl.commands import InitCommand


@click.group()
def cli():
    pass


@click.command()
@click.option("--region", prompt="AWS region", default="us-east-1")
def init(region):
    try:
        InitCommand(region)
    except RuntimeError as err:
        raise click.UsageError(err)


cli.add_command(init)
