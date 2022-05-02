from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Callable, Coroutine, Generic, Optional, final

from ...client import TelegramBot
from telegrambots.wrapper.types.objects import Update

from ...contexts._contexts.context_template import (
    Context,
    ContextTemplate,
    GenericContext,
)
from ...filters._filters.filter_template import Filter
from ...general import Exctractable, TUpdate, check, extract


class HandlerTemplate(metaclass=ABCMeta):
    @abstractmethod
    async def __process__(self, context: ContextTemplate):
        ...

    @abstractmethod
    def should_process(self, update: Update) -> bool:
        ...

    async def process(self, bot: TelegramBot, update: Update) -> None:
        return await self.__process__(ContextTemplate(bot, update))


class GenericHandler(Generic[TUpdate], Exctractable[TUpdate], ABC, HandlerTemplate):
    def __init__(
        self,
        _filter: Filter[TUpdate],
    ) -> None:
        super().__init__()
        self._filter = _filter

    @final
    async def __process__(self, context: ContextTemplate):
        return await self._process(
            Context(self.__extractor__, context.bot, context.wrapper_update)
        )

    @final
    def should_process(self, update: Update) -> bool:
        return check(self._filter, extract(self, update))

    @abstractmethod
    async def _process(self, context: GenericContext[TUpdate]):
        ...


class Handler(Generic[TUpdate], GenericHandler[TUpdate]):
    def __init__(
        self,
        _exctractor: Callable[[Update], Optional[TUpdate]],
        _processor: Callable[[GenericContext[TUpdate]], Coroutine[Any, Any, None]],
        _filter: Filter[TUpdate],
    ) -> None:
        super().__init__(_filter)
        self._exctractor = _exctractor
        self._processor = _processor

    @final
    def __extractor__(self, update: Update) -> Optional[TUpdate]:
        return self._exctractor(update)

    @final
    async def _process(self, context: GenericContext[TUpdate]):
        return await self._processor(context)
