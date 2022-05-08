from abc import ABC, ABCMeta
from typing import (
    Any,
    Callable,
    Generic,
    NoReturn,
    Optional,
    Sequence,
    final,
    TYPE_CHECKING,
    Coroutine,
)

from telegrambots.wrapper.types.objects import Update, Message, CallbackQuery

from ...client import TelegramBot
from ...general import Exctractable, TUpdate
from ...exceptions.propagations import BreakPropagation, ContinuePropagation
from ._continuously_handler import ContinuouslyHandler, ContinueWithInfo
from ...key_resolvers.key_resolver import AbstractKeyResolver


if TYPE_CHECKING:
    from ...dispatcher import Dispatcher, TUpdate
    from .callback_query_context import CallbackQueryContext
    from .message_context import MessageContext
    from ...filters import Filter


class ContextTemplate(metaclass=ABCMeta):
    def __init__(
        self, dp: "Dispatcher", update: Update, update_type: type[Any], handler_tag: str
    ):
        self.__dp = dp
        self.__update = update
        self.__update_type = update_type
        self.__handler_tag = handler_tag

    @final
    @property
    def dp(self) -> "Dispatcher":
        """Returns the dispatcher."""
        return self.__dp

    @final
    @property
    def bot(self) -> TelegramBot:
        """`TelegramBot`: Bot instance"""
        return self.__dp.bot

    @final
    @property
    def update_type(self) -> type[Any]:
        """`type`: Type of the update."""
        return self.__update_type

    @final
    @property
    def handler_tag(self) -> str:
        """`str`: Handler tag."""
        return self.__handler_tag

    @final
    @property
    def wrapper_update(self) -> Update:
        return self.__update

    def stop_propagation(self) -> NoReturn:
        """Stops the propagation of the current context."""
        raise BreakPropagation()

    def continue_propagation(self) -> NoReturn:
        """Continues the propagation of the current context."""
        raise ContinuePropagation()

    def continue_with(
        self,
        target_tag: str,
        update_type: type[TUpdate],
        keys: Sequence[AbstractKeyResolver[TUpdate, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:
        """
        Continues the propagation of the current context, with another handler.

        Args:
            target_tag (`str`): Tag of the target handler.
            update_type (`type`): Type of the update.
            keys (`list[AbstractKeyResolver[TUpdate, Any]]`): Keys to resolve.
            priority (`int`): Priority of the handler.
            args (`Any`): Arguments to pass to the handler.
            kwargs (`Any`): Keyword arguments to pass to the handler.
        """
        self.dp.add_continuously_handler(
            ContinuouslyHandler(
                target_tag,
                self.handler_tag,
                update_type,
                keys,
                priority,
                *args,
                **kwargs,
            )
        )
        self.stop_propagation()

    def continue_with_many(self, *continue_with_info: ContinueWithInfo[Any]):
        """Continues the propagation of the current context, with another handler."""
        self.dp.add_continuously_handler(
            tuple(  # type: ignore
                ContinuouslyHandler(
                    info.target_tag,
                    self.handler_tag,
                    info.update_type,
                    info.keys,
                    info.priority,
                    *info.args,
                    **info.kwargs,
                )
                for info in continue_with_info
            )
        )
        self.stop_propagation()

    def continue_with_message(
        self,
        target_tag: str,
        keys: Sequence[AbstractKeyResolver[Message, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:
        self.continue_with(
            target_tag,
            Message,
            keys,
            priority,
            *args,
            **kwargs,
        )

    def continue_with_callback_query(
        self,
        target_tag: str,
        keys: Sequence[AbstractKeyResolver[CallbackQuery, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:
        self.continue_with(
            target_tag,
            CallbackQuery,
            keys,
            priority,
            *args,
            **kwargs,
        )

    def continue_with_this_callback_query(
        self,
        keys: Sequence[AbstractKeyResolver[CallbackQuery, Any]],
        filter: "Filter[CallbackQuery]",
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[["CallbackQueryContext"], Coroutine[Any, Any, None]]
        ):
            _tag = tag or _function.__name__
            if not self.dp.handler_tag_exists(_tag, CallbackQuery):
                self.dp.add_callback_query_handler(
                    _tag, _function, filter, [self.handler_tag]  # type: ignore
                )
            self.continue_with_callback_query(_tag, keys, *args, **kwargs)

        return decorator

    def continue_with_this_message(
        self,
        keys: list[AbstractKeyResolver[Message, Any]],
        filter: "Filter[Message]",
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[["MessageContext"], Coroutine[Any, Any, None]]
        ):
            _tag = tag or _function.__name__
            if not self.dp.handler_tag_exists(_tag, Message):
                self.dp.add_message_handler(_tag, _function, filter, [self.handler_tag])  # type: ignore
            self.continue_with_message(_tag, keys, *args, **kwargs)

        return decorator


class GenericContext(Generic[TUpdate], Exctractable[TUpdate], ABC, ContextTemplate):
    def __init__(
        self, dp: "Dispatcher", update: Update, update_type: type[Any], handler_tag: str
    ) -> None:
        super().__init__(dp, update, update_type, handler_tag)

    @final
    @property
    def update(self) -> TUpdate:
        """`TUpdate`: Update instance"""
        inner = self.__extractor__(self.wrapper_update)
        if inner is None:
            raise ValueError(f"Cannot exctract inner update.")
        return inner


class Context(Generic[TUpdate], GenericContext[TUpdate]):
    def __init__(
        self,
        _exctractor: Callable[[Update], Optional[TUpdate]],
        dp: "Dispatcher",
        update: Update,
        update_type: type[Any],
        handler_tag: str,
    ) -> None:
        super().__init__(dp, update, update_type, handler_tag)
        self.__extractor = _exctractor

    @final
    def __extractor__(self, update: Update) -> TUpdate:
        r = self.__extractor(update)
        if r is None:
            raise ValueError(f"Cannot exctract inner update.")
        return r
