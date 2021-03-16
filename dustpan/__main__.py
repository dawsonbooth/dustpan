from sys import exit

from . import remove
from .config import CONFIG


def main() -> int:
    paths = set()
    for directory in CONFIG.directories:
        for pattern in CONFIG.patterns:
            for path in directory.rglob(pattern):
                if path.exists():
                    paths.add(path)
                    if CONFIG.verbose:
                        print(f"Found: {path}")

        for pattern in CONFIG.ignore:
            for path in directory.rglob(pattern):
                if path in paths:
                    paths.remove(path)
                if CONFIG.verbose:
                    print(f"Ignored: {path}")  # TODO: Print muted

    for path in paths:
        remove(path)
        if CONFIG.verbose:
            print(f"Removing: {path}")

    # TODO: Optionally remove all blank directories

    if not CONFIG.quiet:
        print(f"{len(paths)} paths removed")

    return 0


if __name__ == "__main__":
    exit(main())
