from __future__ import annotations

import argparse
import enum
from pathlib import Path
from typing import Iterable, Set

import toml

DEFAULT_PATTERNS = {"*.pyc"}
CWD = Path.cwd()


class Verbosity(enum.Enum):
    QUIET = enum.auto()
    NORMAL = enum.auto()
    VERBOSE = enum.auto()


class Configuration:
    directories: Set[Path]
    additional: Set[str]
    protect: Set[str]
    quiet: bool
    verbose: bool

    def __init__(
        self,
        directories: Iterable[Path] = {CWD},
        additional: Iterable[str] = set(),
        protect: Iterable[str] = set(),
        quiet: bool = False,
        verbose: bool = False,
    ) -> None:
        self.directories = set(map(lambda p: Path(p).resolve(), directories))
        self.additional = set(additional)
        self.protect = set(protect)
        self.quiet = quiet
        self.verbose = verbose

    @property
    def verbosity(self) -> Verbosity:
        if self.quiet:
            return Verbosity.QUIET
        elif self.verbose:
            return Verbosity.VERBOSE
        return Verbosity.NORMAL

    @property
    def patterns(self) -> Set[Path]:
        return (DEFAULT_PATTERNS | self.additional) - self.protect

    def __or__(self, o: Configuration) -> Configuration:
        self.__dict__.update(o.__dict__)
        return self


def parse_pyproject() -> Configuration:
    pyproject = toml.load(CWD / "pyproject.toml")

    return Configuration(**pyproject["tool"]["dustpan"])


def parse_arguments() -> Configuration:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("directories", type=Path, nargs="+", default=[CWD], help="Root directories to search")
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

    return Configuration(**vars(args))


def get_configuration() -> Configuration:
    return parse_pyproject() | parse_arguments()
