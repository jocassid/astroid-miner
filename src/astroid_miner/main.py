#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from itertools import chain
from logging import basicConfig, getLogger, INFO
from os import pathsep
from os.path import abspath
from sys import exit, path as sys_path, stderr
from typing import Set

from commands import CallDiagramCommand


logger = getLogger(__name__)


def build_path_option_group(parser: ArgumentParser):
    group = parser.add_mutually_exclusive_group(required=False)
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

    parser.add_argument(
        '-l',
        '--list-path',
        action='store_true',
        help="Show path and exit"
    )


def call_diagram(args: Namespace):
    CallDiagramCommand().run(args)


class SubParserBuilder:

    def build(self, sub_parsers) -> None:
        return None


class CallDiagramSubParserBuilder(SubParserBuilder):

    def build(self, sub_parsers):
        sub_parser = sub_parsers.add_parser(
            'call_diagram',
            help='generate diagram of calls'
        )

        self.build_levels_option_group(sub_parser)
        build_path_option_group(sub_parser)

        sub_parser.add_argument(
            'target',
            nargs='?',
            help="Starting point for the call diagram.  This may be a "
                 "function or a method.  Specify module and function or "
                 "method.  When the target is a function, this argument takes "
                 "the form of MODULE.FUNCTION.  For methods this argument "
                 "takes the form of MODULE.CLASS.FUNCTION",
            metavar='TARGET',
        )
        sub_parser.set_defaults(func=call_diagram)

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


def main():
    basicConfig(filename='astroid_miner.log', level=INFO)

    arg_parser = ArgumentParserBuilder().build()
    args = arg_parser.parse_args()
    python_path = get_python_path(args)

    print(f"{args=}")

    if args.list_path:
        for path in python_path:
            print(path)
        exit(1)

    if not hasattr(args, 'func'):
        print("No sub-command given", stderr)
        return
    args.func(args, python_path)


if __name__ == '__main__':
    main()
