#!/usr/bin/env python3

from datetime import datetime
from importlib.machinery import FileFinder, PathFinder
from os import getcwd
from pathlib import Path
from sys import path as sys_path


def show_path():
    print("sys.path is:")
    for item in sys_path:
        print(f"   {item}")
    print()


def find_spec(finder, *args, **kwargs):
    spec = finder.find_spec(*args, **kwargs)
    pieces = [
        finder.__class__.__name__,
        '.find_spec(',
        ",".join(repr(a) for a in args),
    ]
    for key, value in kwargs.items():
        pieces.append(f", {key}={value!r}")
    pieces.append(')')
    print("".join(pieces))
    print(f"   {spec}\n")


def main():
    show_path()

    fullnames_and_paths = (
        ('alpha', []),
        ('alpha.bravo', []),
        ('main', ['src/astroid_miner/']),
        ('alpha', ['.']),
    )

    finder = PathFinder()
    for fullname, path in fullnames_and_paths:
        kwargs = {}
        if path:
            kwargs['path'] = path
        find_spec(finder, fullname, **kwargs)

    print('\n', '-' * 60, '\n')
    for fullname, path in fullnames_and_paths:
        if not path:
            continue
        finder = FileFinder(path[0])
        find_spec(finder, fullname)



    print(f"finished at {datetime.now()}")


if __name__ == '__main__':
    main()
