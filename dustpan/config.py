from __future__ import annotations

import argparse
import enum
from pathlib import Path
from typing import Set

DEFAULT_PATTERNS = {"**/*.pyc"}


class Verbosity(enum.Enum):
    QUIET = enum.auto()
    NORMAL = enum.auto()
    VERBOSE = enum.auto()


class Configuration:
    directories: Set[Path]
    patterns: Set[Path]
    verbosity: Verbosity

    def __init__(
        self,
        directories: Set[Path],
        additional: Set[Path] = set(),
        protect: Set[Path] = set(),
        quiet: bool = False,
        verbose: bool = False,
    ) -> None:
        self.directories = set(map(lambda p: p.resolve(), directories))
        self.patterns = (DEFAULT_PATTERNS | additional) - protect

        self.verbosity = Verbosity.NORMAL
        if quiet:
            self.verbosity = Verbosity.QUIET
        elif verbose:
            self.verbosity = Verbosity.VERBOSE

    def __or__(self, o: Configuration) -> Configuration:
        self.__dict__.update(o.__dict__)
        return self


def parse_pyproject() -> Configuration:
    # TODO
    return Configuration({Path.cwd()})


def parse_arguments() -> Configuration:

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("directories", type=Path, nargs="+", default=[Path.cwd()], help="Root directories to search")
    parser.add_argument(
        "-a", "--additional", type=str, nargs="+", default=[], help="Additional path patterns for removal"
    )
    parser.add_argument(
        "-p", "--protect", type=str, nargs="+", default=[], help="Path patterns to protect from removal"
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("-q", "--quiet", type=bool, default=False, help="Be quiet")
    verbosity.add_argument("-v", "--verbose", type=bool, default=False, help="Be more verbose")

    args = parser.parse_args()

    return Configuration(set(args.directories), set(args.additional), set(args.protect), args.quiet, args.verbose)


def get_configuration() -> Configuration:
    return parse_pyproject() | parse_arguments()
