from __future__ import annotations

import argparse
import enum
from pathlib import Path
from typing import Iterable, Set

import toml

DEFAULT_PATTERNS = {"*.pyc", ".mypy_cache", ".pytest_cache"}
CWD = Path.cwd()


class Verbosity(enum.Enum):
    QUIET = enum.auto()
    NORMAL = enum.auto()
    VERBOSE = enum.auto()


class Configuration:
    directories: Set[Path]
    include: Set[str]
    exclude: Set[str]
    quiet: bool
    verbose: bool

    def __init__(
        self,
        directories: Iterable[Path] = {CWD},
        include: Iterable[str] = set(),
        exclude: Iterable[str] = set(),
        quiet: bool = False,
        verbose: bool = False,
    ) -> None:
        self.directories = set(map(lambda p: Path(p).resolve(), directories))
        self.include = set(include)
        self.exclude = set(exclude)
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
    def patterns(self) -> Set[str]:
        return (DEFAULT_PATTERNS | self.include) - self.exclude


def parse_pyproject() -> dict:
    pyproject = toml.load(CWD / "pyproject.toml")

    return pyproject["tool"]["dustpan"]


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("directories", type=Path, nargs="+", help="Root directories to search")
    parser.add_argument("-i", "--include", type=str, nargs="+", help="Additional path patterns to queue for removal")
    parser.add_argument("-e", "--exclude", type=str, nargs="+", help="Path patterns to exclude from removal")

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("-q", "--quiet", type=bool, help="Be quiet")
    verbosity.add_argument("-v", "--verbose", type=bool, help="Be more verbose")

    args = parser.parse_args()
    return {k: v for k, v in vars(args).items() if v is not None}


CONFIG = Configuration(**{**parse_pyproject(), **parse_arguments()})
