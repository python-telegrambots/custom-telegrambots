from abc import ABC
from typing import Generic
from .key_resolver import AbstractKeyResolver
from telegrambots.wrapper.types.objects import CallbackQuery, Message, Update
from ..general import TKey


class CallbackQueryKeyResolver(Generic[TKey], AbstractKeyResolver[CallbackQuery, TKey]):
    def __init__(self, key: TKey):
        super().__init__(key)

    def __extractor__(self, update: Update):
        c = update.callback_query
        if c is not None:
            return c
        raise ValueError("Update has no callback query")


class MessageKeyResolver(Generic[TKey], AbstractKeyResolver[Message, TKey], ABC):
    def __init__(self, key: TKey):
        super().__init__(key)

    def __extractor__(self, update: Update):
        m = update.message
        if m is not None:
            return m
        raise ValueError("Update has no message")


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


__all__ = ["MessageSenderId", "CallbackQuerySenderId", "CallbackQueryMessageId"]
