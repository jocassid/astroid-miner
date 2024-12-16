
from argparse import ArgumentParser, Namespace
from itertools import chain
from os.path import abspath
from sys import path as sys_path

from pytest import raises

from astroid_miner.commands import Command
from astroid_miner.main import build_path_option_group


class TestCommand:

    @staticmethod
    def get_args(*args) -> Namespace:
        arg_parser = ArgumentParser()
        build_path_option_group(arg_parser)
        return arg_parser.parse_args(args)

    def test_get_path__no_append_or_substitute(self):
        python_path = Command.get_python_path(self.get_args())
        assert python_path == sys_path

    def test_get_path__append(self):
        path_items = ['/opt/project1', 'foo']
        python_path = Command.get_python_path(
            self.get_args('-a', ':'.join(path_items))
        )
        expected = chain(
            path_items,
            sys_path,
        )
        expected = [abspath(p) for p in expected]
        assert python_path == expected

    def test_get_path__substitute(self):
        path_items = ['/opt/project1', 'foo']
        python_path = Command.get_python_path(
            self.get_args('-s', ':'.join(path_items))
        )
        assert python_path == [abspath(p) for p in path_items]

    def test_get_path__append_and_substitute(self):
        """If append and substitute are both supplied (argument parser
        should prevent this) append is ignored"""
        path_items = ['/opt/project1', 'foo']
        with raises(SystemExit) as execinfo:
            Command.get_python_path(
                self.get_args('-a', 'foo:bar', '-s', ':'.join(path_items))
            )
        assert execinfo.type == SystemExit
        assert execinfo.value.code == 2
