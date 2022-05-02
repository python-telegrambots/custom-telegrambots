from typing import Any, Callable, Coroutine, final

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
    ) -> None:
        super().__init__(_filter)
        self._processor = _processor

    @final
    def __extractor__(self, update: Update):
        return update.message

    @final
    async def _process(self, context: GenericContext[Message]):
        return await self._processor(
            MessageContext(context.bot, context.wrapper_update)
        )


class CallbackQueryHandler(GenericHandler[CallbackQuery]):
    def __init__(
        self,
        _processor: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]],
        _filter: Filter[CallbackQuery],
    ) -> None:
        super().__init__(_filter)
        self._processor = _processor

    @final
    def __extractor__(self, update: Update):
        return update.callback_query

    @final
    async def _process(self, context: GenericContext[CallbackQuery]):
        return await self._processor(
            CallbackQueryContext(context.bot, context.wrapper_update)
        )
