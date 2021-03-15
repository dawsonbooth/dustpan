from __future__ import annotations

import argparse
from pathlib import Path
from typing import Set

DEFAULT_CLEAN = {"**/*.pyc"}


class Configuration:
    directories: Set[Path]
    additional: Set[Path]
    protect: Set[Path]

    quiet: bool
    verbose: bool

    def __or__(self, o: Configuration) -> Configuration:
        return self.__dict__.update(o.__dict__)


def parse_pyproject(self) -> Configuration:
    # TODO
    pass


def parse_arguments() -> Configuration:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("directories", type=Path, nargs="+", help="Root directories to search")
    parser.add_argument("-a", "--additional", type=Path, nargs="+", help="Additional path patterns for removal")
    parser.add_argument("-p", "--protect", type=Path, nargs="+", help="Path patterns to protect from removal")

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("-q", "--quiet", type=bool, default=False, help="Be quiet")
    verbosity.add_argument("-v", "--verbose", type=bool, default=False, help="Be more verbose")

    args = parser.parse_args()

    config = Configuration()

    config.directories = args.directories
    config.additional = args.additional
    config.protect = args.protect
    config.quiet = args.quiet
    config.verbose = args.verbose


def get_configuration() -> Configuration:

    config_toml = parse_pyproject()
    config_cli = parse_arguments()
