from typing import Any, Callable, Coroutine, Mapping, Optional, final, TYPE_CHECKING

from telegrambots.wrapper.types.objects import CallbackQuery, Message, Update

from ...contexts import CallbackQueryContext, MessageContext
from .handler_template import GenericHandler

if TYPE_CHECKING:
    from ...filters._filters.filter_template import Filter
    from ...dispatcher import Dispatcher


class MessageHandler(GenericHandler[Message]):
    def __init__(
        self,
        tag: str,
        _processor: Callable[[MessageContext], Coroutine[Any, Any, None]],
        _filter: "Filter[Message]",
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            tag, _filter, Message, continue_after, allow_continue_after_self, priority
        )
        self._processor = _processor

    @final
    def __extractor__(self, update: Update):
        v = update.message
        if v is None:
            raise ValueError("Update is not a message")
        return v

    @final
    async def __process__(
        self,
        dp: "Dispatcher",
        update: Update,
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any
    ) -> None:
        kwargs.update(**filter_data)
        return await self._processor(
            MessageContext(
                dp,
                update,
                self.tag,
                *args,
                **kwargs,
            )
        )


class CallbackQueryHandler(GenericHandler[CallbackQuery]):
    def __init__(
        self,
        tag: str,
        _processor: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]],
        _filter: "Filter[CallbackQuery]",
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            tag,
            _filter,
            CallbackQuery,
            continue_after,
            allow_continue_after_self,
            priority,
        )
        self._processor = _processor

    @final
    def __extractor__(self, update: Update):
        c = update.callback_query
        if c is None:
            raise ValueError("Update is not a callback query")
        return c

    @final
    async def __process__(
        self,
        dp: "Dispatcher",
        update: Update,
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any
    ) -> None:
        kwargs.update(**filter_data)
        return await self._processor(
            CallbackQueryContext(
                dp,
                update,
                self.tag,
                *args,
                **kwargs,
            )
        )
