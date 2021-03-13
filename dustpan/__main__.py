import argparse
from pathlib import Path
from sys import exit


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("directories", type=Path, help="Root directories to search")
    parser.add_argument("-a", "--additional", type=Path, nargs="+", help="Additional path patterns to remove")

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("-q", "--quiet", type=bool, default=False, help="Be quiet")
    verbosity.add_argument("-v", "--verbose", type=bool, default=False, help="Be more verbose")

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    # TODO

    return 0


if __name__ == "__main__":
    exit(main())
