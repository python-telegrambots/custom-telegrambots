from abc import ABC
from typing import Callable, Generic

from telegrambots.wrapper.types.objects import CallbackQuery, Message

from ..general import TKey, TUpdate
from .key_resolver import AbstractKeyResolver, KeyResolver


def create_key(
    choose_key: Callable[[TUpdate], TKey],
    key_value: TKey,
) -> AbstractKeyResolver[TUpdate, TKey]:
    """Create a key resolver.

    Args:
        `choose_update`: A function that takes an update and returns the actual update
            that should be used to resolve the key.
        `choose_key`: A function that takes the actual update and returns the key.
        `key_value`: The value of the key to compare with extracted key.
    """
    return KeyResolver(choose_key, key_value)


def create_callback_query_key(
    choose_key: Callable[[CallbackQuery], TKey], key_value: TKey
) -> AbstractKeyResolver[CallbackQuery, TKey]:
    """Create a key resolver for callback queries.

    Args:
        `choose_key`: A function that takes the actual callback query and returns the key.
        `key_value`: The value of the key to compare with extracted key.
    """
    return create_key(
        choose_key,
        key_value,
    )


def create_message_key(
    choose_key: Callable[[Message], TKey], key_value: TKey
) -> AbstractKeyResolver[Message, TKey]:
    """Create a key resolver for messages.

    Args:
        `choose_key`: A function that takes the actual message and returns the key.
        `key_value`: The value of the key to compare with extracted key.
    """
    return create_key(choose_key, key_value)


class CallbackQueryKeyResolver(Generic[TKey], AbstractKeyResolver[CallbackQuery, TKey]):
    def __init__(self, key: TKey):
        super().__init__(key)


class MessageKeyResolver(Generic[TKey], AbstractKeyResolver[Message, TKey], ABC):
    def __init__(self, key: TKey):
        super().__init__(key)


class MessageSenderId(MessageKeyResolver[int]):
    def __init__(self, key: int):
        super().__init__(key)

    def _resolve(self, update: Message) -> int:
        user = update.from_user
        if user is not None:
            return user.id
        raise ValueError("Message has no sender")


class CallbackQuerySenderId(CallbackQueryKeyResolver[int]):
    def __init__(self, key: int):
        super().__init__(key)

    def _resolve(self, update: CallbackQuery) -> int:
        user = update.from_user
        if user is not None:
            return user.id
        raise ValueError("CallbackQuery has no sender")


class CallbackQueryMessageId(CallbackQueryKeyResolver[int]):
    def __init__(self, key: int):
        super().__init__(key)

    def _resolve(self, update: CallbackQuery):
        message = update.message
        if message is None:
            raise ValueError("Can't find message from callback query.")
        return message.message_id
