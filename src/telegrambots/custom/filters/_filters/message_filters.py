from typing import Callable

from telegrambots.wrapper.types.objects import Message

from .filter_template import Filter, filter_factory


def message_filter_factory(_check: Callable[[Message], bool]) -> Filter[Message]:
    """
    Factory function to create a message filter.

    Args:
        _check (`Callable[[Message], bool]`): A function that takes a message and returns a boolean.

    Returns:
        `Filter`: A filter that checks if a message passes the filter.
    """

    return filter_factory(_check)
