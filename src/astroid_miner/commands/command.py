
from argparse import Namespace
from typing import List


class Command:
    def run(self, args: Namespace, python_path: List[str]) -> int:
        return 0
