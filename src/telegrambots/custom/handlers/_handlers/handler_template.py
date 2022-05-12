from abc import ABC, ABCMeta, abstractmethod
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Mapping,
    Optional,
    final,
    TYPE_CHECKING,
)

from telegrambots.wrapper.types.objects import Update

from ...contexts._contexts.context_template import Context
from ...filters._filters.filter_template import Filter
from ...general import (
    Exctractable,
    TUpdate,
    check,
    extract,
    ContainedResult,
    general_extractor,
)

if TYPE_CHECKING:
    from ...dispatcher import Dispatcher


class HandlerTemplate(metaclass=ABCMeta):
    @abstractmethod
    async def __process__(
        self,
        update: Update[Any],
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        ...

    @abstractmethod
    def should_process(self, update: Update[Any]) -> ContainedResult:
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
    @abstractmethod
    def dp(self) -> "Dispatcher":
        ...

    @property
    def continue_after(self) -> Optional[list[str]]:
        return None

    @property
    def priority(self) -> int:
        return 0

    async def process(
        self,
        update: Update[Any],
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        return await self.__process__(
            update,
            filter_data,
            *args,
            **kwargs,
        )


class GenericHandler(Generic[TUpdate], Exctractable[TUpdate], ABC, HandlerTemplate):
    def __init__(
        self,
        dp: "Dispatcher",
        tag: str,
        _filter: Filter[TUpdate],
        update_type: type[TUpdate],
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__()
        self._dp = dp
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

    @final
    def __extractor__(self, update: Update[TUpdate]) -> TUpdate:
        return general_extractor(update)

    @abstractmethod
    async def __process__(
        self,
        update: Update[TUpdate],
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        ...

    @final
    def should_process(self, update: Update[TUpdate]) -> ContainedResult:
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

    @final
    @property
    def dp(self) -> "Dispatcher":
        return self._dp


class AbstractHandler(Generic[TUpdate], GenericHandler[TUpdate]):
    def __init__(
        self,
        dp: "Dispatcher",
        tag: str,
        update_type: type[TUpdate],
        processor: Callable[[Context[TUpdate]], Awaitable[None]],
        filter: Filter[TUpdate],
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            dp,
            tag,
            filter,
            update_type,
            continue_after,
            allow_continue_after_self,
            priority,
        )
        self._processor = processor

    @final
    async def __process__(
        self,
        update: Update[TUpdate],
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        kwargs.update(**filter_data)
        return await self._processor(self._build_context(update, *args, **kwargs))

    @abstractmethod
    def _build_context(
        self,
        update: Update[TUpdate],
        *args: Any,
        **kwargs: Any,
    ) -> Context[TUpdate]:
        ...


class Handler(Generic[TUpdate], AbstractHandler[TUpdate]):
    def __init__(
        self,
        dp: "Dispatcher",
        tag: str,
        update_type: type[TUpdate],
        processor: Callable[[Context[TUpdate]], Awaitable[None]],
        filter: Filter[TUpdate],
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            dp,
            tag,
            update_type,
            processor,
            filter,
            continue_after,
            allow_continue_after_self,
            priority,
        )

    @final
    def _build_context(self, update: Update[TUpdate], *args: Any, **kwargs: Any):
        return Context(
            self.dp,
            update,
            self.update_type,
            self.tag,
            *args,
            **kwargs,
        )
