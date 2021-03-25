import os
from pathlib import Path
from sys import exit
from typing import Iterable, Set

from colorama import Style

from . import DEFAULT_EXCLUDE, DEFAULT_INCLUDE, remove, search
from .config import CONFIG


def output(message: str, *args, verbose: bool = False, **kwargs):
    if not verbose:
        print(message, *args, **kwargs)
    elif verbose and CONFIG.verbose:
        print(f"{Style.DIM}{message}{Style.RESET_ALL}", *args, **kwargs)


def paths_to_remove(patterns: Iterable[str], ignore: Iterable[str]) -> Set[Path]:
    paths = set()

    for path in search(*CONFIG.directories, patterns=patterns, ignore=[]):
        paths.add(path)
        output(f"Found: {path}", verbose=True)

    for path in search(*CONFIG.directories, patterns=ignore, ignore=[]):
        if path in paths:
            paths.remove(path)
        output(f"Ignored: {path}", verbose=True)

    return paths


def empty_directories() -> Set[Path]:
    paths = set()
    for path in search(*CONFIG.directories, patterns=["*"], ignore=DEFAULT_EXCLUDE | CONFIG.exclude):
        if path.exists() and path.is_dir():
            with os.scandir(path) as scan:
                if next(scan, None) is None:
                    paths.add(path)
                    output(f"Found: {path}", verbose=True)
    return paths


def remove_paths(paths: Iterable[Path]) -> int:
    paths = set(paths)
    for path in paths:
        remove(path)
        output(f"Removing: {path}", verbose=True)
    return len(paths)


def main() -> int:
    num_removed = 0

    paths = set()

    output("Default search...", verbose=True)
    paths |= paths_to_remove(DEFAULT_INCLUDE, DEFAULT_EXCLUDE)

    output("Custom search...", verbose=True)
    paths |= paths_to_remove(CONFIG.include, CONFIG.exclude)

    output("Removing paths...", verbose=True)
    num_removed += remove_paths(paths)

    if CONFIG.remove_empty_directories:
        output("Empty directory search...", verbose=True)
        empty = empty_directories()

        output("Empty directory search...", verbose=True)
        num_removed += remove_paths(empty)

    output(f"{num_removed} paths removed")

    return 0


if __name__ == "__main__":
    exit(main())
