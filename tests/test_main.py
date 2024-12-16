
from argparse import (
    ArgumentError,
    ArgumentParser,
    Namespace,
)
from itertools import chain
from os import pathsep
from os.path import abspath, dirname, join

from sys import path as sys_path

from pytest import raises
from pytest import mark

from astroid_miner.commands import CallDiagramCommand, Command
from astroid_miner.main import build_path_option_group









