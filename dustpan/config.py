from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Set

import toml

# TODO: Refine these
DEFAULT_PATTERNS = {"__pycache__", "*.pyc", ".mypy_cache", ".pytest_cache"}
DEFAULT_IGNORE = {".venv/**/*"}

CWD = Path.cwd()


class Configuration:
    directories: Set[Path]
    patterns: Set[str]
    ignore: Set[str]
    quiet: bool
    verbose: bool

    def __init__(
        self,
        directories: Iterable[Path] = {CWD},
        patterns: Iterable[str] = set(),
        ignore: Iterable[str] = set(),
        quiet: bool = False,
        verbose: bool = False,
    ) -> None:
        self.directories = set(map(lambda p: Path(p).resolve(), directories))
        self.patterns = set(patterns) | DEFAULT_PATTERNS
        self.ignore = set(ignore)
        self.patterns -= self.ignore
        self.quiet = quiet
        self.verbose = verbose


def parse_pyproject() -> dict:
    pyproject = toml.load(CWD / "pyproject.toml")
    section: dict = pyproject["tool"]["dustpan"]

    return {"patterns": section.get("patterns", []), "ignore": section.get("ignore", [])}


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("directories", type=Path, nargs="+", help="Root directories to search")

    parser.add_argument("-p", "--patterns", type=str, nargs="+", help="Additional path patterns to queue for removal")
    parser.add_argument("-i", "--ignore", type=str, nargs="+", help="Path patterns to exclude from removal")

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("-q", "--quiet", action="store_true", help="Be quiet")
    verbosity.add_argument("-v", "--verbose", action="store_true", help="Be more verbose")

    args = parser.parse_args()
    return {k: v for k, v in vars(args).items() if v is not None}


CONFIG = Configuration(**{**parse_pyproject(), **parse_arguments()})
