
from itertools import chain
from os import pathsep
from os.path import abspath, dirname, join
from pathlib import Path
from sys import path as sys_path

import pytest

from astroid_miner.main import CallDiagramCommand


TESTS_ROOT = dirname(__file__)
APP1_PATH = join('test_apps', 'app1')


class TestCallDiagramCommand:

    def test_get_path__no_append_or_substitute(self):
        command = CallDiagramCommand()
        python_path = command.get_python_path('', '')
        assert python_path == sys_path

    def test_get_path__append(self):
        command = CallDiagramCommand()
        path_items = ['/opt/project1', 'foo']
        append_path = pathsep.join(path_items)
        python_path = command.get_python_path(append_path, '')
        expected = chain(
            path_items,
            sys_path,
        )
        expected = [abspath(p) for p in expected]
        assert python_path == expected

    def test_get_path__substitute(self):
        command = CallDiagramCommand()
        path_items = ['/opt/project1', 'foo']
        substitute_path = pathsep.join(path_items)
        python_path = command.get_python_path('', substitute_path)
        assert python_path == [abspath(p) for p in path_items]

    def test_get_path__append_and_substitute(self):
        """If append and substitute are both supplied (argument parser
        should prevent this) append is ignored"""
        command = CallDiagramCommand()
        path_items = ['/opt/project1', 'foo']
        substitute_path = pathsep.join(path_items)
        python_path = command.get_python_path('foo:bar', substitute_path)
        assert python_path == [abspath(p) for p in path_items]

    @pytest.mark.parametrize(
        'origin_path_parts, remaining_pieces, expected',
        [
            (
                ('parsers', '__init__.py'),
                ['json_parser', 'JsonParser', 'parse'],
                (
                    Path(TESTS_ROOT) / APP1_PATH / 'parsers' / 'json_parser.py',
                    ['JsonParser', 'parse'],
                ),
            ),
            (
                ('main.py',),
                ['main'],
                (
                    Path(TESTS_ROOT) / APP1_PATH / 'main.py',
                    ['main'],
                ),
            ),
        ]
    )
    def test_locate_starting_module(self, origin_path_parts, remaining_pieces, expected):
        origin = join(TESTS_ROOT, APP1_PATH, *origin_path_parts)
        actual = CallDiagramCommand.locate_starting_module(
            str(origin),
            remaining_pieces,
        )
        assert actual == expected

