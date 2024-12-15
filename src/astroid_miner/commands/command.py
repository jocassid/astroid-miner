
from argparse import Namespace
from itertools import chain
from os import pathsep
from os.path import abspath
from sys import path as sys_path
from typing import List, Set


class Command:
    def run(self, args: Namespace) -> int:
        python_path = self.get_python_path(args)
        return self.run_inner(args, python_path)

    def run_inner(self, args: Namespace, python_path: List[str]) -> int:
        raise NotImplemented("Sub-classes should implement this")

    @staticmethod
    def get_python_path(args: Namespace):
        append_path: str = args.append_path or ''
        substitute_path: str = args.substitute_path or ''
        python_path = []
        path_set: Set[str] = set()

        if substitute_path:
            path_collection = [substitute_path.split(pathsep)]
        else:
            path_collection = [sys_path]
            if append_path:
                path_collection.insert(0, append_path.split(pathsep))
            else:
                return sys_path

        for path_item in chain(*path_collection):
            path_item = abspath(path_item)
            if path_item in path_set:
                continue
            path_set.add(path_item)
            python_path.append(path_item)

        return python_path
