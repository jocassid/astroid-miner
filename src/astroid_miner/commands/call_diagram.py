
from argparse import Namespace
from importlib.machinery import ModuleSpec, PathFinder
from logging import getLogger
from os.path import basename
from pathlib import Path
from typing import List, Optional, Set, Tuple

from astroid import parse

from .command import Command


logger = getLogger(__name__)


class CallDiagramCommand(Command):

    def run_inner(self, args: Namespace, python_path: List[str]) -> int:
        target: str = args.target
        print(f"{target=}")

        module_spec, remaining_pieces = self.find_module_spec(
            target,
            [str(p) for p in python_path],
        )

        if not module_spec:
            print(f"Unable to locate module containing {target}")
            return 1

        starting_module_path, remaining_pieces = self.locate_starting_module(
            module_spec.origin,
            remaining_pieces
        )
        print(f"{starting_module_path=}")
        print(f"{remaining_pieces=}")

        with open(starting_module_path, 'r') as in_file:
            module = parse(
                in_file.read(),
                # module_name=target,
                path=str(starting_module_path)
            )

        print(module)

    @staticmethod
    def get_module_name(target: str, remaining_pieces: List[str]) -> str:
        target_pieces = target.split('.')
        remaining_pieces = remaining_pieces.copy()


    @staticmethod
    def locate_starting_module(
            origin: str,
            remaining_pieces: List[str],
    ) -> Tuple[Path, List[str]]:
        origin_base = basename(origin)
        if origin_base != '__init__.py':
            return Path(origin), remaining_pieces
        if not remaining_pieces:
            raise ValueError("No remaining pieces")

        module_path = Path(origin).parent / f"{remaining_pieces.pop(0)}.py"
        if not module_path.exists():
            raise ValueError(f"{module_path} not found")
        return module_path, remaining_pieces

    @staticmethod
    def find_module_spec(
            target: str,
            python_path: List[str],
    ) -> Tuple[Optional[ModuleSpec], List[str]]:
        module_name = ''
        path_finder = PathFinder()

        target_pieces = target.split('.')
        output_data: Tuple[Optional[ModuleSpec], List[str]] = (None, [])
        while len(target_pieces) > 1:
            target_piece = target_pieces.pop(0)
            if module_name:
                module_name = f"{module_name}.{target_piece}"
            else:
                module_name = target_piece

            spec = path_finder.find_spec(module_name, path=python_path)
            if not spec:
                continue

            if output_data != (None, []):
                logger.warning(
                    f"Multiple ModuleSpecs found.  Prior spec and remaining "
                    f"target pieces are {output_data[0]} and {output_data[1]} "
                    f"respectively."
                )

            output_data = (spec, target_pieces.copy())

        return output_data
