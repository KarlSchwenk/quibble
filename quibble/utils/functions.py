"""Utils for quibble."""
from __future__ import annotations  # noqa T484

from math import inf
from typing import Union, Any


def replace_inf(value: Any,
                replace_value: float = 10 ** 10) -> Union[Any, float]:
    """Function to replace inf with numeric value.

    Args:
        value: inf value to replace
        replace_value: value to return instead

    Returns:
        value, if if value is not +- inf, +- replace_value else.
    """
    if value == inf:
        return replace_value
    if value == -inf:
        return -1 * replace_value

    return value


def cprint(text: str,
           style: str = "",
           end: bool = True) -> None:
    """Function to print formatted text.

    Args:
        text: text to print formatted
        style: style annotation
        end: flag to indicate whether to stop formatting with end of command or not
    """
    if end:
        suffix = "\033[0m"
    else:
        suffix = ""

    if style.lower() in ['p', 'pink']:
        print(f"\033[95m{text}{suffix}")

    elif style.lower() in ['b', 'blue']:
        print(f"\033[94m{text}{suffix}")

    elif style.lower() in ['g', 'green']:
        print(f"\033[92m{text}{suffix}")

    elif style.lower() in ['y', 'yellow']:
        print(f"\033[93m{text}{suffix}")

    elif style.lower() in ['r', 'red']:
        print(f"\033[91m{text}{suffix}")

    elif style.lower() in ['bold']:
        print(f"\033[1m{text}{suffix}")

    elif style.lower() in ['underline', 'u']:
        print(f"\033[4m{text}{suffix}")

    else:
        print(f"{text}")
