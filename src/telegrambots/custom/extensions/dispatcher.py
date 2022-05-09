from abc import ABC
from typing import TYPE_CHECKING, Any, Optional, final, Coroutine, Callable
from ..filters import Filter
from ..contexts import CallbackQueryContext, MessageContext
from ..contexts._contexts.context_template import GenericContext
from ..handlers._handlers.update_handler import CallbackQueryHandler, MessageHandler
from ..handlers._handlers.handler_template import Handler
from ..general import TUpdate

from telegrambots.wrapper.types.objects import CallbackQuery, Message, Update


if TYPE_CHECKING:
    from .. import Dispatcher


class DispatcherExtensions(ABC):
    def __init__(self, dp: "Dispatcher") -> None:
        self.__dp = dp

    @final
    @property
    def _dp(self) -> "Dispatcher":
        return self.__dp


class AddHandlerViaDecoratorExtension(DispatcherExtensions):
    def __init__(self, dp: "Dispatcher") -> None:
        super().__init__(dp)

    def any(
        self,
        type_of_update: type[TUpdate],
        extractor: Callable[[Update], Optional[TUpdate]],
        filter: Filter[TUpdate],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for updates.

        Args:
            type_of_update (`type[TUpdate]`): The type of update to handle.
            extractor (`Callable[[Update], Optional[TUpdate]]`): A function that extracts the update from an update.
            filter (`Filter[TUpdate]`): A filter that checks if the update passes the filter.
            tag (`Optional[str]`, optional): A tag for the handler. Should be unique. Defaults to None.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
        """

        def decorator(
            _function: Callable[[GenericContext[TUpdate]], Coroutine[Any, Any, None]]
        ):
            self._dp.add_handler(
                tag or _function.__name__,
                Handler(type_of_update, extractor, _function, filter, continue_after),
            )

        return decorator

    def message(
        self,
        filter: Filter[Message],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for messages.

        Args:
            filter (`Filter[Message]`): A filter that checks if the message passes the filter.
            tag (`str`): A tag for the handler. Should be unique.
        """

        def decorator(_function: Callable[[MessageContext], Coroutine[Any, Any, None]]):
            self._dp.add.handlers.message(
                tag or _function.__name__, _function, filter, continue_after
            )

        return decorator

    def callback_query(
        self,
        filter: Filter[CallbackQuery],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for callback queries.

        Args:
            filter (`Filter[CallbackQuery]`): A filter that checks if the callback query passes the filter.
            tag (`str`): A tag for the handler. Should be unique.
        """

        def decorator(
            _function: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]]
        ):
            self._dp.add.handlers.callback_query(
                tag or _function.__name__, _function, filter, continue_after
            )

        return decorator


class AddHandlersExtensions(DispatcherExtensions):
    def __init__(self, dp: "Dispatcher") -> None:
        super().__init__(dp)

        # extension
        self._via_decorator: Optional[AddHandlerViaDecoratorExtension] = None

    @final
    @property
    def via_decorator(self) -> AddHandlerViaDecoratorExtension:
        """Returns the extension for adding handlers via decorator."""
        if self._via_decorator is None:
            self._via_decorator = AddHandlerViaDecoratorExtension(self._dp)
        return self._via_decorator

    def callback_query(
        self,
        tag: str,
        function: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]],
        filter: Filter[CallbackQuery],
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for callback queries.

        Args:
            tag (`str`): A tag for the handler. Should be unique.
            function (`Callable[[CallbackQueryContext], Coroutine[Any, Any, None]]`): The function to call.
            filter (`Filter[CallbackQuery]`): A filter that checks if the callback query passes the filter.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
        """

        self._dp.add_handler(
            tag, CallbackQueryHandler(function, filter, continue_after)
        )

    def message(
        self,
        tag: str,
        function: Callable[[MessageContext], Coroutine[Any, Any, None]],
        filter: Filter[Message],
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for messages.

        Args:
            tag (`str`): A tag for the handler. Should be unique.
            function (`Callable[[MessageContext], Coroutine[Any, Any, None]]`): The function to call.
            filter (`Filter[Message]`): A filter that checks if the message passes the filter.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
        """

        self._dp.add_handler(tag, MessageHandler(function, filter, continue_after))


class AddExtensions(DispatcherExtensions):
    def __init__(self, dp: "Dispatcher") -> None:
        super().__init__(dp)

        # extensions
        self.__add_handlers: Optional[AddHandlersExtensions] = None

    @final
    @property
    def handlers(self) -> AddHandlersExtensions:
        """Use this extension to add different type of handlers to the dispatcher."""
        if self.__add_handlers is None:
            self.__add_handlers = AddHandlersExtensions(self._dp)
        return self.__add_handlers
