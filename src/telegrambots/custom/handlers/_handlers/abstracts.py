from abc import ABC
from typing import TYPE_CHECKING, Any, Optional, final

from telegrambots.wrapper.types.objects import CallbackQuery, Message

from ...contexts import CallbackQueryContext, MessageContext
from .handler_template import AbstractHandler


if TYPE_CHECKING:
    from telegrambots.wrapper.types.objects import Update

    from ...filters._filters.filter_template import Filter


class MessageHandler(AbstractHandler[MessageContext, Message], ABC):
    def __init__(
        self,
        tag: str,
        filter: Optional["Filter[Message]"] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            tag,
            Message,
            None,
            filter,
            continue_after,
            allow_continue_after_self,
            priority,
        )

    @final
    def _build_context(
        self, update: "Update[Message]", *args: Any, **kwargs: Any
    ) -> MessageContext:
        return MessageContext(
            self.dp,
            update,
            self.tag,
            *args,
            **kwargs,
        )


class CallbackQueryHandler(AbstractHandler[CallbackQueryContext, CallbackQuery], ABC):
    def __init__(
        self,
        tag: str,
        filter: Optional["Filter[CallbackQuery]"] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            tag,
            CallbackQuery,
            None,
            filter,
            continue_after,
            allow_continue_after_self,
            priority,
        )

    @final
    def _build_context(
        self, update: "Update[CallbackQuery]", *args: Any, **kwargs: Any
    ) -> CallbackQueryContext:
        return CallbackQueryContext(
            self.dp,
            update,
            self.tag,
            *args,
            **kwargs,
        )
