
from typing import List, Union

from astroid import extract_node
from astroid.nodes import Dict as AstroidDict
from astroid.nodes import NodeNG

def dict_to_kwargs(expr: str) -> str:
    """
    Convert a a 'key=value' argument string.
    Example: '{"a": 1, "b": 2}' -> 'a=1, b=2'
    """
    # Parse the expression using astroid
    node: Union[NodeNG, List[NodeNG]] = extract_node(expr.strip())

    if not isinstance(node, AstroidDict):
        raise ValueError("Input is not a valid dictionary expression.")
    node: AstroidDict = node

    pieces = []
    for key_node, value_node in node.items:
        pieces.append(
            f"{key_node.value}={value_node.as_string()},"
        )
    return "\n".join(pieces)

def kwargs_to_dict(expr: str) -> str:
    """
    Converts a string key=value function arguments into a dict.
    Example 'a=1, b=2' -> {'a': 1, 'b': 2}
    """
    raise NotImplementedError()
