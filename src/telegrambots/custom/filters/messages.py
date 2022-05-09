import re
from typing import Literal, overload

from ..filters import Filter
from telegrambots.wrapper.types.objects import Message

from ._filters.message_filters import message_filter_factory


any_message = message_filter_factory(lambda _: True)


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


class Regex(Filter[Message]):
    @overload
    def __init__(self, pattern: str):
        """
        Allows only messages that match a regular expression.

        Args:
            pattern (`str`): The regular expression to match.

        Returns:
            `Filter`: A filter that allows only messages that match a regular expression.
        """
        ...

    @overload
    def __init__(self, pattern: re.Pattern[str]):
        """
        Allows only messages that match a regular expression.

        Args:
            pattern (`str`): The regular expression to match.

        Returns:
            `Filter`: A filter that allows only messages that match a regular expression.
        """
        ...

    def __init__(self, pattern: str | re.Pattern[str]):
        if isinstance(pattern, str):
            self._ap = re.compile(pattern)
        else:
            self._ap = pattern
        super().__init__()

    def __check__(self, message: Message) -> bool:
        if message.text is not None:
            matches = self._ap.match(message.text)
            if matches is not None:
                self._set_metadata("matches", matches)
                return True
        return False
