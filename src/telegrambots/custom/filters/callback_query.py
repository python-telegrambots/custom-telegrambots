from typing import Callable, overload
from ._filters.filter_template import Filter, filter_factory
import re
from telegrambots.wrapper.types.objects import CallbackQuery


def callback_query_filter_factory(
    _check: Callable[[CallbackQuery], bool]
) -> Filter[CallbackQuery]:
    """
    Factory function to create a callback_query filter.

    Args:
        _check (`Callable[[CallbackQuery], bool]`): A function that takes a callback_query and returns a boolean.

    Returns:
        `Filter`: A filter that checks if a callback_query passes the filter.
    """

    return filter_factory(_check)


@overload
def regex(pattern: str) -> Filter[CallbackQuery]:
    """
    Allows only messages that match a regular expression.

    Args:
        pattern (`str`): The regular expression to match.

    Returns:
        `Filter`: A filter that allows only messages that match a regular expression.
    """
    ...


@overload
def regex(pattern: re.Pattern[str]) -> Filter[CallbackQuery]:
    """
    Allows only messages that match a regular expression.

    Args:
        pattern (`str`): The regular expression to match.

    Returns:
        `Filter`: A filter that allows only messages that match a regular expression.
    """
    ...


def regex(pattern: str | re.Pattern[str]):
    if isinstance(pattern, str):
        ap = re.compile(pattern)
    else:
        ap = pattern

    return callback_query_filter_factory(
        lambda callback: callback.data is not None
        and ap.match(callback.data) is not None
    )


any_callback = callback_query_filter_factory(lambda _: True)
""" Allows any callback_query. """
