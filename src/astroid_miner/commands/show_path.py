from argparse import Namespace
from logging import getLogger
from typing import List

from .command import Command


logger = getLogger(__name__)


class ShowPathCommand(Command):

    def run_inner(self, args: Namespace, python_path: List[str]) -> int:
        for item in python_path:
            print(item)
        return 0
