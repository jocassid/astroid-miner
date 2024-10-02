#!/usr/bin/env python3

from argparse import ArgumentParser
from copy import deepcopy
# find_spec allows us to find the file path to a module
from importlib.util import find_spec
from pathlib import Path
from sys import path as sys_path


class Command:
    def run(self, args):
        return 0


class CallDiagramCommand(Command):

    def run(self, args):
        print(f'CallDiagramCommand.run({args=})')

        all_paths = deepcopy(sys_path)

        append_path = args.append_path or ''
        for path_item in append_path.split(':'):
            path_item = Path(path_item)
            print(path_item)

        print('-' * 20)
        for path_item in all_paths:
            print(path_item)


        # target_pieces = args.target.split('.')
        # print(target_pieces)
        #
        # python_path = environ.get('PYTHONPATH') or []
        # for path_item in python_path.split(':'):
        #     print(path_item)






def call_diagram(args):
    CallDiagramCommand().run(args)


class ArgumentParserBuilder:
    def build(self):
        parser = ArgumentParser(
            description="Analyze Python source code",
        )
        sub_parsers = parser.add_subparsers(
            help='sub-command help',
        )
        self.add_call_diagram_subparser(sub_parsers)
        return parser

    @staticmethod
    def add_call_diagram_subparser(sub_parsers):
        sub_parser = sub_parsers.add_parser(
            'call_diagram',
            help='generate diagram of calls'
        )

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
