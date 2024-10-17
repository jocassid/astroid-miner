#!/usr/bin/env python3

from argparse import ArgumentParser
from copy import deepcopy
# find_spec allows us to find the file path to a module
from importlib.util import find_spec
from itertools import chain
from pathlib import Path
from sys import path as sys_path
from typing import Set


class Command:
    def run(self, args):
        return 0


class CallDiagramCommand(Command):

    def run(self, args):
        print(f'CallDiagramCommand.run({args=})')

        target = args.target
        append_path = args.append_path or ''

        all_paths = []
        path_set: Set[Path] = set()

        for path_item in chain(sys_path, append_path.split(':')):
            path_item = Path(path_item).absolute()
            if path_item in path_set:
                continue
            all_paths.append(path_item)
            path_set.add(path_item)

        for path_item in all_paths:
            modules = self.find_modules(
                target.split('.'),
                path_item,
            )
            print(modules)
            break

    def get_path(self, append_path, ):
        pass

    def find_modules(self, target_pieces, directory, depth=0):
        if depth > 5:
            return

        pass












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
        pass


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

    def add_call_diagram_subparser(self, sub_parsers):
        sub_parser = sub_parsers.add_parser(
            'call_diagram',
            help='generate diagram of calls'
        )

        group = sub_parser.add_mutually_exclusive_group(required=False)


        sub_parser.add_argument(
            '-a', '--append-path',
            help="A colon separated lists of directories to search in "
                 "addition to those in sys.path",
            metavar='PATH'
        )

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


def parse_args_and_call_main():

    arg_parser = ArgumentParserBuilder().build()
    args = arg_parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    parse_args_and_call_main()
