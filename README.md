# `dustpan`

[![pypi version](https://img.shields.io/pypi/v/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)
[![downloads](https://pepy.tech/badge/dustpan)](https://pepy.tech/project/dustpan)
[![build status](https://github.com/dawsonbooth/dustpan/workflows/build/badge.svg)](https://github.com/dawsonbooth/dustpan/actions?workflow=build)
[![python versions](https://img.shields.io/pypi/pyversions/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)
[![format](https://img.shields.io/pypi/format/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)
[![license](https://img.shields.io/pypi/l/dustpan.svg?style=flat)](https://github.com/dawsonbooth/dustpan/blob/master/LICENSE)

## Description

Clean up your workspace by removing extraneous files and directories.

## Installation

With [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.

```bash
python -m pip install dustpan
```

## Usage

This is a command-line program, and can be executed as follows:

```bash
dustpan [-h] [-p PATTERNS [PATTERNS ...]] [-i IGNORE [IGNORE ...]] [--remove-empty-directories] [-q | -v | -vv] directories [directories ...]
```

Positional arguments:

```txt
  directories           Root directories to search
```

Optional arguments:

```txt
  -h, --help            show this help message and exit
  -p PATTERNS [PATTERNS ...], --patterns PATTERNS [PATTERNS ...]
                        Additional path patterns to queue for removal
  -i IGNORE [IGNORE ...], --ignore IGNORE [IGNORE ...]
                        Path patterns to exclude from removal
  --remove-empty-directories
                        Remove all childless directories
  -q, --quiet           Be quiet
  -v, --verbose         Be more verbose
  -vv, --very-verbose   Be very verbose
```

Feel free to [check out the docs](https://dawsonbooth.github.io/dustpan/) for more information on how to use this package.

## License

This software is released under the terms of [MIT license](LICENSE).
