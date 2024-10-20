#!/usr/bin/env python3

from argparse import ArgumentParser
from importlib.machinery import ModuleSpec, PathFinder
from itertools import chain
from logging import basicConfig, getLogger, INFO
from os import pathsep
from os.path import abspath, basename
from pathlib import Path
from sys import path as sys_path, stderr
from typing import List, Optional, Set, Tuple


logger = getLogger(__name__)


class Command:
    def run(self, args):
        return 0


class CallDiagramCommand(Command):

    def run(self, args):
        print(f'CallDiagramCommand.run({args=})\n')

        target: str = args.target

        python_path = self.get_python_path(
            args.append_path or '',
            args.substitute_path or '',
        )

        module_spec, remaining_pieces = self.find_module_spec(
            target,
            [str(p) for p in python_path],
        )

        if not module_spec:
            print(f"Unable to locate module containing {target}")
            return

        starting_module_path, remaining_pieces = self.locate_starting_module(
            module_spec.origin,
            remaining_pieces
        )
        print(f"{starting_module_path=}")
        print(f"{remaining_pieces=}")


    @staticmethod
    def locate_starting_module(
            origin: str,
            remaining_pieces: List[str],
    ) -> Tuple[Path, List[str]]:
        origin_base = basename(origin)
        if origin_base != '__init__.py':
            return Path(origin), remaining_pieces
        if not remaining_pieces:
            raise ValueError("No remaining pieces")

        module_path = Path(origin).parent / f"{remaining_pieces.pop(0)}.py"
        if not module_path.exists():
            raise ValueError(f"{module_path} not found")
        return module_path, remaining_pieces

    @staticmethod
    def find_module_spec(
            target: str,
            python_path: List[str],
    ) -> Tuple[Optional[ModuleSpec], List[str]]:
        module_name = ''
        path_finder = PathFinder()

        target_pieces = target.split('.')
        output_data: Tuple[Optional[ModuleSpec], List[str]] = (None, [])
        while len(target_pieces) > 1:
            target_piece = target_pieces.pop(0)
            if module_name:
                module_name = f"{module_name}.{target_piece}"
            else:
                module_name = target_piece

            spec = path_finder.find_spec(module_name, path=python_path)
            if not spec:
                continue

            if output_data != (None, []):
                logger.warning(
                    f"Multiple ModuleSpecs found.  Prior spec and remaining "
                    f"target pieces are {output_data[0]} and {output_data[1]} "
                    f"respectively."
                )

            output_data = (spec, target_pieces.copy())

        return output_data

    @staticmethod
    def get_python_path(append_path: str, substitute_path: str) -> List[str]:
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


def call_diagram(args):
    CallDiagramCommand().run(args)


class SubParserBuilder:
    pass


class CallDiagramSubParserBuilder(SubParserBuilder):

    def build(self, sub_parsers):
        sub_parser = sub_parsers.add_parser(
            'call_diagram',
            help='generate diagram of calls'
        )

        self.build_path_option_group(sub_parser)
        self.build_levels_option_group(sub_parser)

        sub_parser.add_argument(
            'target',
            help="Starting point for the call diagram.  This may be a "
                 "function or a method.  Specify module and function or "
                 "method.  When the target is a function, this argument takes "
                 "the form of MODULE.FUNCTION.  For methods this argument "
                 "takes the form of MODULE.CLASS.FUNCTION",
            metavar='TARGET',
        )
        sub_parser.set_defaults(func=call_diagram)

    @staticmethod
    def build_path_option_group(sub_parser):
        group = sub_parser.add_mutually_exclusive_group(required=False)
        metavar = 'PATH'

        group.add_argument(
            '-a',
            '--append-path',
            help="A colon-separated list of directories to search in addition "
                 "to those in sys.path",
            metavar=metavar,
        )

        group.add_argument(
            '-s',
            '--substitute-path',
            help="A colon-separated list of directories to search instead of "
                 "those in sys.path",
            metavar=metavar
        )

    @staticmethod
    def build_levels_option_group(sub_parser):
        group = sub_parser.add_mutually_exclusive_group(required=True)

        def add_group_argument(flag1, flag2, help_text):
            group.add_argument(
                flag1,
                flag2,
                type=int,
                help=help_text,
                metavar='LEVELS',
            )

        add_group_argument(
            '-f',
            '--forward',
            "Show calls from target function forward specified number of levels",
        )
        add_group_argument(
            '-b',
            '--backward',
            "Shows calls to target function backward specified number of levels",
        )
        add_group_argument(
            '-r',
            '--radius',
            "Shows calls to and calls from target function forward and "
            "backward specified number of levels"
        )


class ArgumentParserBuilder:

    def build(self):
        parser = ArgumentParser(
            description="Analyze Python source code",
        )
        sub_parsers = parser.add_subparsers(
            help='sub-command help',
        )

        for sub_parser_builder in (
                CallDiagramSubParserBuilder(),
        ):
            sub_parser_builder.build(sub_parsers)

        return parser


def main():
    basicConfig(filename='astroid_miner.log', level=INFO)

    arg_parser = ArgumentParserBuilder().build()
    args = arg_parser.parse_args()
    if not hasattr(args, 'func'):
        print("No sub-command given", stderr)
        return
    args.func(args)


if __name__ == '__main__':
    main()
