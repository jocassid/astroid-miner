#!/usr/bin/env python3

from argparse import ArgumentParser
from importlib.machinery import PathFinder
from itertools import chain
from os import pathsep
from os.path import abspath
from sys import path as sys_path, stderr
from typing import List, Set


class Command:
    def run(self, args):
        return 0


class CallDiagramCommand(Command):

    def run(self, args):
        print(f'CallDiagramCommand.run({args=})')

        target = args.target

        python_path = self.get_python_path(
            args.append_path or '',
            args.substitute_path or '',
        )
        python_path = [str(p) for p in python_path]

        module_name = ''
        path_finder = PathFinder()

        target_pieces = target.split('.')
        target_piece_count = len(target_pieces)
        for i, target_piece in enumerate(target_pieces):
            if module_name:
                module_name = f"{module_name}.{target_piece}"
            else:
                module_name = target_piece
            spec = path_finder.find_spec(module_name, path=python_path)
            if not spec:
                continue

            next_index = i + 1
            if next_index >= target_piece_count:
                continue

            print(
                "module_name={} spec.origin={} remaining_target_piece={}".format(
                    module_name,
                    spec.origin,
                    target_pieces[next_index:]
                )
            )

    @staticmethod
    def get_python_path(append_path, substitute_path) -> List[str]:
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

        def add_group_argument(flag, help_text):
            group.add_argument(
                flag,
                type=int,
                help=help_text,
                metavar='LEVELS',
            )

        add_group_argument(
            '--calls',
            "Show calls from target function forward specified number of levels",
        )
        add_group_argument(
            '--callers',
            "Shows calls to target function backward specified number of levels",
        )
        add_group_argument(
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


def parse_args_and_call_main():

    arg_parser = ArgumentParserBuilder().build()
    args = arg_parser.parse_args()
    if not hasattr(args, 'func'):
        print("No sub-command given")
        return
    args.func(args)


if __name__ == '__main__':
    parse_args_and_call_main()
