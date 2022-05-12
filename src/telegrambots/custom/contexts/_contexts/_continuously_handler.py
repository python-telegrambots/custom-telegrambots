from abc import ABC, abstractmethod
import dataclasses
from typing import Any, Callable, Generic, Optional, Sequence

from telegrambots.wrapper.types.objects import Update, CallbackQuery, Message

from ...general import TUpdate
from ...key_resolvers.key_resolver import AbstractKeyResolver
from ...key_resolvers import (
    CallbackQueryMessageId,
    MessageSenderId,
    CallbackQuerySenderId,
)


@dataclasses.dataclass(init=True, frozen=True, slots=True)
class ContinueWithInfo(Generic[TUpdate]):
    target_tag: str
    update_type: type[TUpdate]
    resolve_update: Callable[[Update[TUpdate]], Optional[TUpdate]]
    keys: Sequence[AbstractKeyResolver[TUpdate, Any]]
    priority: int = 0
    args: tuple[Any, ...] = dataclasses.field(default_factory=tuple)  # type: ignore
    kwargs: dict[str, Any] = dataclasses.field(default_factory=dict)

    @staticmethod
    def with_callback_query(
        target_tag: str,
        keys: Sequence[AbstractKeyResolver[CallbackQuery, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ):
        return ContinueWithInfo(
            target_tag=target_tag,
            update_type=CallbackQuery,
            resolve_update=lambda x: x.callback_query,
            keys=keys,
            priority=priority,
            args=args,
            kwargs=kwargs,
        )

    @staticmethod
    def with_callback_query_from(
        target_tag: str,
        user_id: int,
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ):
        return ContinueWithInfo(
            target_tag=target_tag,
            update_type=CallbackQuery,
            resolve_update=lambda x: x.callback_query,
            keys=[CallbackQuerySenderId(user_id)],
            priority=priority,
            args=args,
            kwargs=kwargs,
        )

    @staticmethod
    def with_callback_query_same_message_from(
        target_tag: str,
        message_id: int,
        user_id: int,
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ):
        return ContinueWithInfo(
            target_tag=target_tag,
            update_type=CallbackQuery,
            resolve_update=lambda x: x.callback_query,
            keys=[CallbackQuerySenderId(user_id), CallbackQueryMessageId(message_id)],
            priority=priority,
            args=args,
            kwargs=kwargs,
        )

    @staticmethod
    def with_message(
        target_tag: str,
        keys: Sequence[AbstractKeyResolver[Message, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ):
        return ContinueWithInfo(
            target_tag=target_tag,
            update_type=Message,
            resolve_update=lambda x: x.message,
            keys=keys,
            priority=priority,
            args=args,
            kwargs=kwargs,
        )

    @staticmethod
    def with_message_from(
        target_tag: str,
        user_id: int,
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ):
        return ContinueWithInfo(
            target_tag=target_tag,
            update_type=Message,
            resolve_update=lambda x: x.message,
            keys=[MessageSenderId(user_id)],
            priority=priority,
            args=args,
            kwargs=kwargs,
        )


class ContinuouslyHandlerTemplate:
    def check_keys(self, update: Update[Any]):
        return all(key.is_key(update) for key in self.keys)

    @property
    @abstractmethod
    def keys(self) -> Sequence[AbstractKeyResolver[Any, Any]]:
        ...

    @property
    @abstractmethod
    def target_tag(self) -> str:
        ...

    @property
    @abstractmethod
    def start_tag(self) -> str:
        ...

    @property
    @abstractmethod
    def update_type(self) -> type[Any]:
        ...

    @property
    @abstractmethod
    def args(self) -> tuple[Any, ...]:
        ...

    @property
    @abstractmethod
    def kwargs(self) -> dict[str, Any]:
        ...

    @property
    def priority(self) -> int:
        return 0


class GenericContinuouslyHandler(Generic[TUpdate], ABC, ContinuouslyHandlerTemplate):
    @property
    @abstractmethod
    def keys(self) -> Sequence[AbstractKeyResolver[TUpdate, Any]]:
        ...


class ContinuouslyHandler(Generic[TUpdate], GenericContinuouslyHandler[TUpdate]):
    def __init__(
        self,
        target_tag: str,
        start_tag: str,
        update_type: type[TUpdate],
        keys: Sequence[AbstractKeyResolver[TUpdate, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        self._target_tag = target_tag
        self._start_tag = start_tag
        self._update_type = update_type
        self._keys = keys
        self._priority = priority
        self._args = args
        self._kwargs = kwargs

    @property
    def keys(self) -> Sequence[AbstractKeyResolver[TUpdate, Any]]:
        return self._keys

    @property
    def target_tag(self) -> str:
        return self._target_tag

    @property
    def start_tag(self) -> str:
        return self._start_tag

    @property
    def update_type(self) -> type[Any]:
        return self._update_type

    @property
    def args(self) -> tuple[Any, ...]:
        return self._args

    @property
    def kwargs(self) -> dict[str, Any]:
        return self._kwargs

    @property
    def priority(self) -> int:
        return self._priority
