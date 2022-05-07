from typing import Any, Callable, Coroutine, Optional, final

from telegrambots.wrapper.types.objects import CallbackQuery, Message, Update

from ...contexts._contexts.context_template import GenericContext
from ...contexts import CallbackQueryContext, MessageContext
from ...filters._filters.filter_template import Filter
from .handler_template import GenericHandler


class MessageHandler(GenericHandler[Message]):
    def __init__(
        self,
        _processor: Callable[[MessageContext], Coroutine[Any, Any, None]],
        _filter: Filter[Message],
        continue_after: Optional[list[str]] = None,
        priority: int = 0,
    ) -> None:
        super().__init__(_filter)
        self._processor = _processor
        self._continue_after = continue_after
        self._priority = priority

    @final
    def __extractor__(self, update: Update):
        v = update.message
        if v is None:
            raise ValueError("Update is not a message")
        return v

    @final
    async def _process(
        self, context: GenericContext[Message], *args: Any, **kwargs: Any
    ):
        return await self._processor(
            MessageContext(
                context.dp,
                context.wrapper_update,
                context.handler_tag,
            ),
            *args,
            **kwargs,
        )

    @property
    def update_type(self) -> type[Any]:
        return Message

    @final
    @property
    def continue_after(self) -> Optional[list[str]]:
        return self._continue_after

    @property
    def priority(self) -> int:
        return self._priority


class CallbackQueryHandler(GenericHandler[CallbackQuery]):
    def __init__(
        self,
        _processor: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]],
        _filter: Filter[CallbackQuery],
        continue_after: Optional[list[str]] = None,
        priority: int = 0,
    ) -> None:
        super().__init__(_filter)
        self._processor = _processor
        self._continue_after = continue_after
        self._priority = priority

    @final
    def __extractor__(self, update: Update):
        c = update.callback_query
        if c is None:
            raise ValueError("Update is not a callback query")
        return c

    @final
    async def _process(
        self, context: GenericContext[CallbackQuery], *args: Any, **kwargs: Any
    ):
        return await self._processor(
            CallbackQueryContext(
                context.dp, context.wrapper_update, context.handler_tag
            ),
            *args,
            **kwargs,
        )

    @property
    def update_type(self) -> type[Any]:
        return CallbackQuery

    @final
    @property
    def continue_after(self) -> Optional[list[str]]:
        return self._continue_after

    @property
    def priority(self) -> int:
        return self._priority
