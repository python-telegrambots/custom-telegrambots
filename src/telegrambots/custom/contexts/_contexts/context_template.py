from abc import ABC, ABCMeta
from typing import (
    Any,
    Callable,
    Generic,
    NoReturn,
    Optional,
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
        resolve_update: Callable[[Update], Optional[TUpdate]],
        key_resolver: AbstractKeyResolver[TUpdate, Any],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:
        """
        Continues the propagation of the current context, with another handler.

        Args:
            target_tag (`str`): The tag of the handler to continue with.
            update_type (`type`): The type of the update.
            resolve_update (`Callable[[Update], TUpdate]`): A function that resolves the update.
            resolve_key (`Callable[[TUpdate], TKey]`): A function that resolves the key.
            priority (`int`): The priority of the handler.
            key (`TKey`): The key to use.
        """
        self.dp.add_continuously_handler(
            ContinuouslyHandler(
                target_tag,
                self.handler_tag,
                update_type,
                resolve_update,
                key_resolver,
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
                    info.resolve_update,
                    info.key_resolver,
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
        key_resolver: AbstractKeyResolver[Message, Any],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:
        self.continue_with(
            target_tag,
            Message,
            lambda x: x.message,
            key_resolver,
            priority,
            *args,
            **kwargs,
        )

    def continue_with_callback_query(
        self,
        target_tag: str,
        key_resolver: AbstractKeyResolver[CallbackQuery, Any],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:
        self.continue_with(
            target_tag,
            CallbackQuery,
            lambda x: x.callback_query,
            key_resolver,
            priority,
            *args,
            **kwargs,
        )

    def continue_with_this_callback_query(
        self,
        key_resolver: AbstractKeyResolver[CallbackQuery, Any],
        filter: "Filter[CallbackQuery]",
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[
                ["CallbackQueryContext", Any, Any], Coroutine[Any, Any, None]
            ]
        ):
            _tag = tag or _function.__name__
            if not self.dp.handler_tag_exists(_tag, CallbackQuery):
                self.dp.add_callback_query_handler(
                    _tag, _function, filter, [self.handler_tag]  # type: ignore
                )
            self.continue_with_callback_query(_tag, key_resolver, *args, **kwargs)

        return decorator

    def continue_with_this_message(
        self,
        key_resolver: AbstractKeyResolver[Message, Any],
        filter: "Filter[Message]",
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[["MessageContext", Any, Any], Coroutine[Any, Any, None]]
        ):
            _tag = tag or _function.__name__
            if not self.dp.handler_tag_exists(_tag, Message):
                self.dp.add_message_handler(_tag, _function, filter, [self.handler_tag])  # type: ignore
            self.continue_with_message(_tag, key_resolver, *args, **kwargs)

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
