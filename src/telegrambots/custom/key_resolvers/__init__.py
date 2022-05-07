from .key_resolver import AbstractKeyResolver
from telegrambots.wrapper.types.objects import CallbackQuery, Message, Update


class MessageSenderId(AbstractKeyResolver[Message, int]):
    def __init__(self, key: int):
        self._key = key

    def _resolve(self, update: Message) -> int:
        user = update.from_user
        if user is not None:
            return user.id
        raise ValueError("Message has no sender")

    @property
    def key(self):
        return self._key

    def __extractor__(self, update: Update):
        m = update.message
        if m is not None:
            return m
        raise ValueError("Update has no message")


class CallbackQuerySenderId(AbstractKeyResolver[CallbackQuery, int]):
    def __init__(self, key: int):
        self._key = key

    def _resolve(self, update: CallbackQuery) -> int:
        user = update.from_user
        if user is not None:
            return user.id
        raise ValueError("CallbackQuery has no sender")

    @property
    def key(self):
        return self._key

    def __extractor__(self, update: Update):
        c = update.callback_query
        if c is not None:
            return c
        raise ValueError("Update has no callback query")


__all__ = ["MessageSenderId", "CallbackQuerySenderId"]
