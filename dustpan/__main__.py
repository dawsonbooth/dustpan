import os
from pathlib import Path
from sys import exit
from typing import Iterable, Set

from colorama import Style

from . import DEFAULT_EXCLUDE, DEFAULT_INCLUDE, remove, search
from .config import CONFIG, Verbosity


def output(message: str, *args, verbosity: Verbosity = Verbosity.NORMAL, **kwargs):
    if verbosity <= CONFIG.verbosity:
        if verbosity >= Verbosity.VERBOSE:
            message = f"{Style.DIM}{message}{Style.RESET_ALL}"
        print(message, *args, **kwargs)


def paths_to_remove(patterns: Iterable[str], ignore: Iterable[str]) -> Set[Path]:
    paths = set()

    for path in search(*CONFIG.directories, patterns=patterns, ignore=[]):
        paths.add(path)
        output(f"Found {path}", verbosity=Verbosity.VERY_VERBOSE)

    for path in search(*CONFIG.directories, patterns=ignore, ignore=[]):
        if path in paths:
            paths.remove(path)
        output(f"Ignored {path}", verbosity=Verbosity.VERY_VERBOSE)

    return paths


def empty_directories() -> Set[Path]:
    paths = set()
    for path in search(*CONFIG.directories, patterns=["*"], ignore=DEFAULT_EXCLUDE | CONFIG.exclude):
        if path.exists() and path.is_dir():
            with os.scandir(path) as scan:
                if next(scan, None) is None:
                    paths.add(path)
                    output(f"Found {path}", verbosity=Verbosity.VERY_VERBOSE)
    return paths


def remove_paths(paths: Iterable[Path]) -> int:
    paths = set(paths)
    for path in paths:
        remove(path)
        output(f"Removing {path}", verbosity=Verbosity.VERBOSE)
    return len(paths)


def main() -> int:
    paths = paths_to_remove(DEFAULT_INCLUDE, DEFAULT_EXCLUDE) | paths_to_remove(CONFIG.include, CONFIG.exclude)
    num_removed = remove_paths(paths)

    if CONFIG.remove_empty_directories:
        empty = empty_directories()
        num_removed += remove_paths(empty)

    output(f"{num_removed} paths removed.")

    return 0


if __name__ == "__main__":
    exit(main())
