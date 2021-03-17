from sys import exit

from colorama import Style

from . import remove
from .config import CONFIG


def print_verbose(message: str, *args, **kwargs) -> None:
    print(f"{Style.DIM}{message}{Style.RESET_ALL}", *args, **kwargs)


def main() -> int:
    paths = set()
    for directory in CONFIG.directories:
        for pattern in CONFIG.patterns:
            for path in directory.rglob(pattern):
                if path.exists():
                    paths.add(path)
                    if CONFIG.verbose:
                        print_verbose(f"Found: {path}")

        for pattern in CONFIG.ignore:
            for path in directory.rglob(pattern):
                if path in paths:
                    paths.remove(path)
                if CONFIG.verbose:
                    print_verbose(f"Ignored: {path}")

    for path in paths:
        remove(path)
        if CONFIG.verbose:
            print_verbose(f"Removing: {path}")

    # TODO: Optionally remove all blank directories

    if not CONFIG.quiet:
        print(f"{len(paths)} paths removed")

    return 0


if __name__ == "__main__":
    exit(main())
