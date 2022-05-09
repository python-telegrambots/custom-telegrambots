from abc import ABC, ABCMeta, abstractmethod
from typing import (
    Any,
    Callable,
    Coroutine,
    Generic,
    Mapping,
    Optional,
    final,
    TYPE_CHECKING,
)

from telegrambots.wrapper.types.objects import Update

from ...contexts._contexts.context_template import Context, GenericContext
from ...filters._filters.filter_template import Filter
from ...general import Exctractable, TUpdate, check, extract, ContainedResult

if TYPE_CHECKING:
    from ...dispatcher import Dispatcher


class HandlerTemplate(metaclass=ABCMeta):
    @abstractmethod
    async def __process__(
        self,
        dp: "Dispatcher",
        update: Update,
        handler_tag: str,
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        ...

    @abstractmethod
    def should_process(self, update: Update) -> ContainedResult:
        ...

    @property
    @abstractmethod
    def update_type(self) -> type[Any]:
        ...

    @property
    def continue_after(self) -> Optional[list[str]]:
        return None

    @property
    def priority(self) -> int:
        return 0

    async def process(
        self,
        dp: "Dispatcher",
        update: Update,
        handler_tag: str,
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        return await self.__process__(
            dp,
            update,
            handler_tag,
            filter_data,
            *args,
            **kwargs,
        )


class GenericHandler(Generic[TUpdate], Exctractable[TUpdate], ABC, HandlerTemplate):
    def __init__(
        self,
        _filter: Filter[TUpdate],
    ) -> None:
        super().__init__()
        self._filter = _filter

    @abstractmethod
    async def __process__(
        self,
        dp: "Dispatcher",
        update: Update,
        handler_tag: str,
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        ...

    @final
    def should_process(self, update: Update) -> ContainedResult:
        checked = check(self._filter, extract(self, update))
        return ContainedResult(checked, self._filter)


class Handler(Generic[TUpdate], GenericHandler[TUpdate]):
    def __init__(
        self,
        update_type: type[TUpdate],
        exctractor: Callable[[Update], Optional[TUpdate]],
        processor: Callable[[GenericContext[TUpdate]], Coroutine[Any, Any, None]],
        filter: Filter[TUpdate],
        continue_after: Optional[list[str]] = None,
        priority: int = 0,
    ) -> None:
        super().__init__(filter)
        self._exctractor = exctractor
        self._processor = processor
        self._update_type = update_type
        self._continue_after = continue_after
        self._priority = priority

    @final
    @property
    def continue_after(self) -> Optional[list[str]]:
        return self._continue_after

    @final
    def __extractor__(self, update: Update) -> TUpdate:
        d = self._exctractor(update)
        if d is None:
            raise ValueError("Can't resolve actual update.")
        return d

    async def __process__(
        self,
        dp: "Dispatcher",
        update: Update,
        handler_tag: str,
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        return await self._processor(
            Context(
                self.__extractor__,
                dp,
                update,
                self.update_type,
                handler_tag,
                **filter_data,
            ),
            *args,
            **kwargs,
        )

    @property
    def update_type(self) -> type[TUpdate]:
        return self._update_type

    @property
    def priority(self) -> int:
        return self._priority
