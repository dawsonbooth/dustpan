from __future__ import annotations

import argparse
import enum
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Set, Union

import toml

CWD = Path.cwd()


class Verbosity(enum.IntEnum):
    QUIET = 0
    NORMAL = 1
    VERBOSE = 2
    VERY_VERBOSE = 3


@dataclass
class Configuration:
    directories: Set[Path]
    include: Set[str]
    exclude: Set[str]
    remove_empty_directories: bool
    verbosity: Verbosity

    def __init__(
        self,
        directories: Iterable[Union[os.PathLike, str]] = {CWD},
        include: Iterable[str] = set(),
        exclude: Iterable[str] = set(),
        remove_empty_directories: bool = False,
        quiet: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
    ) -> None:
        self.directories = set(map(lambda p: Path(p).resolve(), directories))
        self.include = set(include)
        self.exclude = set(exclude)
        self.remove_empty_directories = remove_empty_directories

        if quiet:
            self.verbosity = Verbosity.QUIET
        elif verbose:
            self.verbosity = Verbosity.VERBOSE
        elif very_verbose:
            self.verbosity = Verbosity.VERY_VERBOSE
        else:
            self.verbosity = Verbosity.NORMAL


def parse_pyproject_toml() -> dict:
    pyproject_toml = toml.load(CWD / "pyproject.toml")
    config: dict = pyproject_toml.get("tool", {}).get("dustpan", {})
    return {k.replace("-", "_"): v for k, v in config.items()}


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("directories", type=Path, nargs="+", help="Root directories to search")

    parser.add_argument("-p", "--patterns", type=str, nargs="+", help="Additional path patterns to queue for removal")
    parser.add_argument("-i", "--ignore", type=str, nargs="+", help="Path patterns to exclude from removal")

    parser.add_argument("--remove-empty-directories", action="store_true", help="Remove all childless directories")

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("-q", "--quiet", action="store_true", help="Be quiet")
    verbosity.add_argument("-v", "--verbose", action="store_true", help="Be more verbose")
    verbosity.add_argument("-vv", "--very-verbose", action="store_true", help="Be very verbose")

    args = parser.parse_args()
    return {k: v for k, v in vars(args).items() if bool(v)}


CONFIG = Configuration(**{**parse_pyproject_toml(), **parse_arguments()})
