from abc import ABC, abstractmethod
import dataclasses
from typing import Any, Callable, Generic, Optional

from telegrambots.wrapper.types.objects import Update, CallbackQuery, Message

from ...general import Exctractable, TUpdate
from ...key_resolvers.key_resolver import AbstractKeyResolver


@dataclasses.dataclass(init=True, frozen=True, slots=True)
class ContinueWithInfo(Generic[TUpdate]):
    target_tag: str
    update_type: type[TUpdate]
    resolve_update: Callable[[Update], Optional[TUpdate]]
    key_resolver: AbstractKeyResolver[TUpdate, Any]
    priority: int = 0
    args: tuple[Any, ...] = dataclasses.field(default_factory=tuple)  # type: ignore
    kwargs: dict[str, Any] = dataclasses.field(default_factory=dict)

    @staticmethod
    def with_callback_query(
        target_tag: str,
        key_resolver: AbstractKeyResolver[CallbackQuery, Any],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ):
        return ContinueWithInfo(
            target_tag=target_tag,
            update_type=CallbackQuery,
            resolve_update=lambda x: x.callback_query,
            key_resolver=key_resolver,
            priority=priority,
            args=args,
            kwargs=kwargs,
        )

    @staticmethod
    def with_message(
        target_tag: str,
        key_resolver: AbstractKeyResolver[Message, Any],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ):
        return ContinueWithInfo(
            target_tag=target_tag,
            update_type=Message,
            resolve_update=lambda x: x.message,
            key_resolver=key_resolver,
            priority=priority,
            args=args,
            kwargs=kwargs,
        )


class ContinuouslyHandlerTemplate:
    def check_key(self, update: Update):
        return self.key_resolver.is_key(update)

    @property
    @abstractmethod
    def key_resolver(self) -> AbstractKeyResolver[Any, Any]:
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


class GenericContinuouslyHandler(
    Generic[TUpdate], Exctractable[TUpdate], ABC, ContinuouslyHandlerTemplate
):
    def _resolve_key_form_tupdate(self, update: TUpdate) -> Any:
        ...

    def _resolve_key(self, update: Update) -> Any:
        actual_update = self.__extractor__(update)
        if actual_update is None:
            raise ValueError("Can't resolve actual update.")

        return self._resolve_key_form_tupdate(actual_update)


class ContinuouslyHandler(Generic[TUpdate], GenericContinuouslyHandler[TUpdate]):
    def __init__(
        self,
        target_tag: str,
        start_tag: str,
        update_type: type[TUpdate],
        resolve_update: Callable[[Update], Optional[TUpdate]],
        key_resolver: AbstractKeyResolver[TUpdate, Any],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        self._target_tag = target_tag
        self._start_tag = start_tag
        self._update_type = update_type
        self._resolve_update = resolve_update
        self._key_resolver = key_resolver
        self._priority = priority
        self._args = args
        self._kwargs = kwargs

    def __extractor__(self, update: Update):
        r = self._resolve_update(update)
        if r is None:
            raise ValueError("Can't resolve actual update.")
        return r

    def _resolve_key_form_tupdate(self, update: TUpdate) -> Any:
        return self._key_resolver.resolver(update)

    @property
    def key_resolver(self) -> AbstractKeyResolver[TUpdate, Any]:
        return self._key_resolver

    @property
    def key(self) -> Any:
        return self._key_resolver.key

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
