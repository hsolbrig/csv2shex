"""Generate ShEx schemas from CSV-formatted application profiles."""

import os
from pathlib import Path
import click
from .config import write_starter_prefixfile

# pylint: disable=unused-argument
#         During development, unused arguments here.

@click.group()
@click.version_option("0.1", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(config):
    """Generate ShEx schemas from CSV-formatted application profiles."""


@cli.command()
@click.argument("csvfile", type=click.File('r'))
@click.help_option(help="Show help and exit")
@click.pass_context
def parse(config, csvfile):
    """Parse and display CSV file for debugging."""
    print(f"csvfile: {csvfile}")


@cli.command()
@click.argument("csvfile", type=click.File('r'))
@click.help_option(help="Show help and exit")
@click.pass_context
def prefixes(config, csvfile):
    """Write config file in working directory."""

    print(f"Writing {prefixfile} - edit at will.")
    write_starter_prefixfile()

