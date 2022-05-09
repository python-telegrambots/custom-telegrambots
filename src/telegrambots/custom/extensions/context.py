from abc import ABC
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    NoReturn,
    Optional,
    Sequence,
    Coroutine,
    final,
)

from telegrambots.wrapper.types.objects import CallbackQuery, Message

from ..contexts._contexts._continuously_handler import (
    ContinueWithInfo,
    ContinuouslyHandler,
)
from ..exceptions.propagations import BreakPropagation, ContinuePropagation
from ..general import TUpdate
from ..key_resolvers.key_resolver import AbstractKeyResolver
from ..key_resolvers import (
    MessageSenderId,
    CallbackQueryMessageId,
    CallbackQuerySenderId,
)
from ..filters import Filter

if TYPE_CHECKING:
    from .. import ContextTemplate
    from ..contexts import CallbackQueryContext, MessageContext


class ContextExtensions(ABC):
    def __init__(self, context: "ContextTemplate") -> None:
        self.__context = context

    @final
    @property
    def _context(self) -> "ContextTemplate":
        return self.__context


class PropagationExtension(ContextExtensions):
    def __init__(self, context: "ContextTemplate") -> None:
        super().__init__(context)

    def stop(self) -> NoReturn:
        """Stops the propagation of the current context."""
        raise BreakPropagation()

    def resume(self) -> NoReturn:
        """Continues the propagation of the current context."""
        raise ContinuePropagation()


class ContinueWithThisExtensions(ContextExtensions):
    def __init__(self, context: "ContextTemplate") -> None:
        super().__init__(context)

    def callback_query(
        self,
        keys: Sequence[AbstractKeyResolver[CallbackQuery, Any]],
        filter: Filter[CallbackQuery],
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[["CallbackQueryContext"], Coroutine[Any, Any, None]]
        ):
            _tag = tag or _function.__name__
            if not self._context.dp.handler_tag_exists(_tag, CallbackQuery):
                self._context.dp.add.handlers.callback_query(
                    _tag, _function, filter, [self._context.handler_tag]
                )
            self._context.continue_with.callback_query(_tag, keys, *args, **kwargs)

        return decorator

    def callback_query_form(
        self,
        user_id: int,
        filter: Filter[CallbackQuery],
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[["CallbackQueryContext"], Coroutine[Any, Any, None]]
        ):
            _tag = tag or _function.__name__
            if not self._context.dp.handler_tag_exists(_tag, CallbackQuery):
                self._context.dp.add.handlers.callback_query(
                    _tag, _function, filter, [self._context.handler_tag]
                )
            self._context.continue_with.callback_query(
                _tag, [CallbackQuerySenderId(user_id)], *args, **kwargs
            )

        return decorator

    def callback_query_same_message_form(
        self,
        message_id: int,
        user_id: int,
        filter: Filter[CallbackQuery],
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[["CallbackQueryContext"], Coroutine[Any, Any, None]]
        ):
            _tag = tag or _function.__name__
            if not self._context.dp.handler_tag_exists(_tag, CallbackQuery):
                self._context.dp.add.handlers.callback_query(
                    _tag, _function, filter, [self._context.handler_tag]
                )
            self._context.continue_with.callback_query(
                _tag,
                [CallbackQuerySenderId(user_id), CallbackQueryMessageId(message_id)],
                *args,
                **kwargs,
            )

        return decorator

    def callback_query_same_message(
        self,
        message_id: int,
        filter: Filter[CallbackQuery],
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[["CallbackQueryContext"], Coroutine[Any, Any, None]]
        ):
            _tag = tag or _function.__name__
            if not self._context.dp.handler_tag_exists(_tag, CallbackQuery):
                self._context.dp.add.handlers.callback_query(
                    _tag, _function, filter, [self._context.handler_tag]
                )
            self._context.continue_with.callback_query(
                _tag,
                [CallbackQueryMessageId(message_id)],
                *args,
                **kwargs,
            )

        return decorator

    def message(
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
            if not self._context.dp.handler_tag_exists(_tag, Message):
                self._context.dp.add.handlers.message(
                    _tag, _function, filter, [self._context.handler_tag]
                )
            self._context.continue_with.message(_tag, keys, *args, **kwargs)

        return decorator

    def message_from(
        self,
        user_id: int,
        filter: "Filter[Message]",
        tag: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ):
        def decorator(
            _function: Callable[["MessageContext"], Coroutine[Any, Any, None]]
        ):
            _tag = tag or _function.__name__
            if not self._context.dp.handler_tag_exists(_tag, Message):
                self._context.dp.add.handlers.message(
                    _tag, _function, filter, [self._context.handler_tag]
                )
            self._context.continue_with.message(
                _tag, [MessageSenderId(user_id)], *args, **kwargs
            )

        return decorator


class ContinueWithExtensions(ContextExtensions):
    def __init__(self, context: "ContextTemplate") -> None:
        super().__init__(context)

        # extensions
        self.__this: Optional[ContinueWithThisExtensions] = None

    @final
    @property
    def this(self) -> ContinueWithThisExtensions:
        """Extension methods that allow you to add, register and continue with a handler, directly inside another."""
        if self.__this is None:
            self.__this = ContinueWithThisExtensions(self._context)
        return self.__this

    def any(
        self,
        target_tag: str,
        update_type: type[TUpdate],
        keys: Sequence[AbstractKeyResolver[TUpdate, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:  # type: ignore
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
        self._context.dp.add_continuously_handler(
            ContinuouslyHandler(
                target_tag,
                self._context.handler_tag,
                update_type,
                keys,
                priority,
                *args,
                **kwargs,
            )
        )
        self._context.propagation.stop()

    def many(
        self, *continue_with_info: ContinueWithInfo[Any]
    ) -> NoReturn:  # type: ignore
        """Continues the propagation of the current context, with another handler."""
        self._context.dp.add_continuously_handler(
            tuple(  # type: ignore
                ContinuouslyHandler(
                    info.target_tag,
                    self._context.handler_tag,
                    info.update_type,
                    info.keys,
                    info.priority,
                    *info.args,
                    **info.kwargs,
                )
                for info in continue_with_info
            )
        )
        self._context.propagation.stop()

    def message(
        self,
        target_tag: str,
        keys: Sequence[AbstractKeyResolver[Message, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:
        self.any(
            target_tag,
            Message,
            keys,
            priority,
            *args,
            **kwargs,
        )

    def callback_query(
        self,
        target_tag: str,
        keys: Sequence[AbstractKeyResolver[CallbackQuery, Any]],
        priority: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> NoReturn:
        self.any(
            target_tag,
            CallbackQuery,
            keys,
            priority,
            *args,
            **kwargs,
        )
