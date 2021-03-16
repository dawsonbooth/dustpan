import shutil
from pathlib import Path


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


__all__ = ["remove", "remove_file", "remove_directory"]
