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
    @abstractmethod
    def tag(self) -> str:
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
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        return await self.__process__(
            dp,
            update,
            filter_data,
            *args,
            **kwargs,
        )


class GenericHandler(Generic[TUpdate], Exctractable[TUpdate], ABC, HandlerTemplate):
    def __init__(
        self,
        tag: str,
        _filter: Filter[TUpdate],
        update_type: type[TUpdate],
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__()
        self._tag = tag
        self._filter = _filter
        self._update_type = update_type
        self._priority = priority

        if allow_continue_after_self:
            if continue_after:
                if tag not in continue_after:
                    continue_after = continue_after + [tag]
            else:
                continue_after = [tag]

        self._continue_after = continue_after

    @abstractmethod
    async def __process__(
        self,
        dp: "Dispatcher",
        update: Update,
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        ...

    @final
    def should_process(self, update: Update) -> ContainedResult:
        checked = check(self._filter, extract(self, update))
        return ContainedResult(checked, self._filter)

    @final
    @property
    def tag(self) -> str:
        return self._tag

    @final
    @property
    def continue_after(self) -> Optional[list[str]]:
        return self._continue_after

    @final
    @property
    def update_type(self) -> type[TUpdate]:
        return self._update_type

    @final
    @property
    def priority(self) -> int:
        return self._priority


class Handler(Generic[TUpdate], GenericHandler[TUpdate]):
    def __init__(
        self,
        tag: str,
        update_type: type[TUpdate],
        exctractor: Callable[[Update], Optional[TUpdate]],
        processor: Callable[[GenericContext[TUpdate]], Coroutine[Any, Any, None]],
        filter: Filter[TUpdate],
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            tag,
            filter,
            update_type,
            continue_after,
            allow_continue_after_self,
            priority,
        )
        self._exctractor = exctractor
        self._processor = processor

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
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        kwargs.update(**filter_data)
        return await self._processor(
            Context(
                self.__extractor__,
                dp,
                update,
                self.update_type,
                self.tag,
                *args,
                **kwargs,
            )
        )
