#!/usr/bin/env python3

from argparse import ArgumentParser


def call_diagram(args):
    print(f'call_diagram {args=}')


def parse_args_and_call_main():
    arg_parser = ArgumentParser(
        description="Analyze Python source code",
    )
    subparsers = arg_parser.add_subparsers(
        help='sub-command help',
    )

    call_diagram_parser = subparsers.add_parser(
        'call_diagram',
        help='generate diagram of calls'
    )
    call_diagram_parser.set_defaults(func=call_diagram)
    call_diagram_parser.add_argument(
        '-f', '--forward',
        type=int,
        help="Generate diagram with functions called from "
             "target for specified number of levels",
        metavar='LEVELS',
    )
    call_diagram_parser.add_argument(
        '-b', '--backward',
        type=int,
    )
    call_diagram_parser.add_argument(
        '-r', '--radius',
        type=int,
    )
    call_diagram_parser.add_argument(
        metavar='TARGET_FUNCTION_OR_METHOD'
    )

    args = arg_parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    parse_args_and_call_main()
