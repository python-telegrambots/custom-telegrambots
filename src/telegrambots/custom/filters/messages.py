import re
from typing import Literal, overload

from ..filters import Filter
from telegrambots.wrapper.types.objects import Message

from ._filters.message_filters import message_filter_factory


text_message = message_filter_factory(lambda message: message.text is not None)
""" Allows only text messages. """


def chat_type(chat_type: Literal["private", "group", "supergroup", "channel"]):
    """
    Allows only messages from a certain chat type.

    Args:
        chat_type (`str`): The chat type to allow.

    Returns:
        `Filter`: A filter that allows only messages from a certain chat type.
    """
    return message_filter_factory(lambda message: message.chat.type == chat_type)


private = chat_type("private")
""" Allows only messages from private chats. """


@overload
def regex(pattern: str) -> Filter[Message]:
    """
    Allows only messages that match a regular expression.

    Args:
        pattern (`str`): The regular expression to match.

    Returns:
        `Filter`: A filter that allows only messages that match a regular expression.
    """
    ...


@overload
def regex(pattern: re.Pattern[str]) -> Filter[Message]:
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

    return message_filter_factory(
        lambda message: message.text is not None and ap.match(message.text) is not None
    )
