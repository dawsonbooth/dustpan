import shutil
from pathlib import Path
from typing import Iterable, Set

DEFAULT_INCLUDE = {"__pycache__", "*.pyc", "*.pyo"}
DEFAULT_EXCLUDE = {".venv/**/*"}


def remove_file(file: Path) -> None:
    """Remove a file

    Args:
        path (Path): The path to the file
    """
    if file.exists():
        file.unlink()


def remove_directory(directory: Path) -> None:
    """Remove a directory

    Args:
        path (Path): The path to the directory
    """
    if directory.exists():
        shutil.rmtree(directory)


def remove(path: Path) -> None:
    """Remove a file or directory

    Args:
        path (Path): The path to the file or directory
    """
    if path.exists():
        if path.is_dir():
            remove_directory(path)
        else:
            remove_file(path)


def search(
    *directories: Path, patterns: Iterable[str] = DEFAULT_INCLUDE, ignore: Iterable[str] = DEFAULT_EXCLUDE
) -> Set[Path]:
    """Search for path patterns within directories

    Args:
        patterns (Iterable[str], optional): Patterns to glob recursively. Defaults to DEFAULT_PATTERNS.
        ignore (Iterable[str], optional): Patterns to ignore. Defaults to DEFAULT_IGNORE.

    Returns:
        Set[Path]: [description]
    """
    paths = set()
    for directory in directories:
        for pattern in patterns:
            for path in directory.rglob(pattern):
                if path.exists():
                    paths.add(path)

        for pattern in ignore:
            for path in directory.rglob(pattern):
                if path in paths:
                    paths.remove(path)

    return paths


__all__ = ["remove", "remove_file", "remove_directory", "search"]
