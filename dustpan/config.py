from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Set

import attr
import toml

CWD = Path.cwd()


def _set_of_paths(paths: Iterable[str]) -> Set[Path]:
    return set(map(lambda p: Path(p).resolve(), paths))


@attr.s
class Configuration:
    directories: Set[Path] = attr.ib(default={CWD}, converter=_set_of_paths)
    include: Set[str] = attr.ib(default=set(), converter=set)
    exclude: Set[str] = attr.ib(default=set(), converter=set)
    remove_empty_directories: bool = attr.ib(default=False)
    quiet: bool = attr.ib(default=False)
    verbose: bool = attr.ib(default=False)


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

    args = parser.parse_args()
    return {k: v for k, v in vars(args).items() if bool(v)}


CONFIG = Configuration(**{**parse_pyproject_toml(), **parse_arguments()})
