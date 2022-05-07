from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Callable, Coroutine, Generic, Optional, final, TYPE_CHECKING

from telegrambots.wrapper.types.objects import Update

from ...contexts._contexts.context_template import (
    Context,
    ContextTemplate,
    GenericContext,
)
from ...filters._filters.filter_template import Filter
from ...general import Exctractable, TUpdate, check, extract

if TYPE_CHECKING:
    from ...dispatcher import Dispatcher


class HandlerTemplate(metaclass=ABCMeta):
    @abstractmethod
    async def __process__(
        self, context: ContextTemplate, *args: Any, **kwargs: Any
    ) -> None:
        ...

    @abstractmethod
    def should_process(self, update: Update) -> bool:
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
        update_type: type[Any],
        handler_tag: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        return await self.__process__(
            ContextTemplate(
                dp, update=update, update_type=update_type, handler_tag=handler_tag
            ),
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

    @final
    async def __process__(
        self, context: ContextTemplate, *args: Any, **kwargs: Any
    ) -> None:
        return await self._process(
            Context(
                self.__extractor__,
                context.dp,
                context.wrapper_update,
                context.update_type,
                context.handler_tag,
            ),
            *args,
            **kwargs,
        )

    @final
    def should_process(self, update: Update) -> bool:
        return check(self._filter, extract(self, update))

    @abstractmethod
    async def _process(
        self, context: GenericContext[TUpdate], *args: Any, **kwargs: Any
    ) -> None:
        ...


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

    @final
    async def _process(
        self, context: GenericContext[TUpdate], *args: Any, **kwargs: Any
    ) -> None:
        return await self._processor(context, *args, **kwargs)

    @property
    def update_type(self) -> type[TUpdate]:
        return self._update_type

    @property
    def priority(self) -> int:
        return self._priority
