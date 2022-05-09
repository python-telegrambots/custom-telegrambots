from abc import ABC
from typing import Any, Generic

from telegrambots.wrapper.types.objects import CallbackQuery, Message

from ..general import TUpdate
from .custom_resolvers import (
    CallbackQueryMessageId,
    CallbackQuerySenderId,
    MessageSenderId,
)
from .key_resolver import AbstractKeyResolver


class AbstractKeyBuilder(Generic[TUpdate], ABC):
    def __init__(self) -> None:
        self._keys: list[AbstractKeyResolver[TUpdate, Any]] = []

    def __call__(self) -> Any:
        return self.build()

    def add_key(self, key: AbstractKeyResolver[TUpdate, Any]):
        self._keys.append(key)
        return self

    def build(self):
        return self._keys


class MessageKeyBuilder(AbstractKeyBuilder[Message]):
    def __init__(self) -> None:
        super().__init__()

    def from_user(self, user_id: int):
        return self.add_key(MessageSenderId(user_id))


class CallbackQueryKeyBuilder(AbstractKeyBuilder[CallbackQuery]):
    def __init__(self) -> None:
        super().__init__()

    def from_user(self, user_id: int):
        return self.add_key(CallbackQuerySenderId(user_id))

    def from_message(self, message_id: int):
        return self.add_key(CallbackQueryMessageId(message_id))


class KeyBuilder:
    @staticmethod
    def for_message() -> MessageKeyBuilder:
        return MessageKeyBuilder()

    @staticmethod
    def for_callback_query() -> CallbackQueryKeyBuilder:
        return CallbackQueryKeyBuilder()
