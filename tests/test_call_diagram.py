
from os.path import dirname, join
from pathlib import Path

from pytest import mark

from astroid_miner.commands import CallDiagramCommand


TESTS_ROOT = dirname(__file__)
APP1_PATH = join('test_apps', 'app1')


class TestCallDiagramCommand:

    @mark.parametrize(
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

    @mark.parametrize(
        'target, remaining_pieces, expected',
        [
            ('main.main', ['main'], 'main'),
        ]
    )
    def test_get_module_name(self, target, remaining_pieces, expected):
        pass

