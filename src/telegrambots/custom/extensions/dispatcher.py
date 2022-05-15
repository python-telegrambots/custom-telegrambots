import importlib
import inspect
import os
from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Generator, Optional, final

from telegrambots.wrapper.types.objects import CallbackQuery, Message

from ..contexts import CallbackQueryContext, MessageContext
from ..contexts._contexts.context_template import Context
from ..filters import Filter
from ..general import TUpdate
from ..handlers import CallbackQueryHandler, MessageHandler
from ..handlers._handlers.handler_template import AbstractHandler, Handler

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
        filter: Optional[Filter[TUpdate]],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ):
        """Registers a handler for updates.

        Args:
            type_of_update (`type[TUpdate]`): The type of update to handle.
            filter (`Filter[TUpdate]`, optional): A filter that checks if the update passes the filter.
            tag (`Optional[str]`, optional): A tag for the handler. Should be unique. Defaults to None.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
            allow_continue_after_self (`bool`, optional): Same as current adding handler tag to continue_after.
        """

        def decorator(
            _function: Callable[[Context[TUpdate]], Coroutine[Any, Any, None]]
        ):
            n_tag = tag or _function.__name__
            self._dp.add_handler(
                Handler(
                    self._dp,
                    n_tag,
                    type_of_update,
                    _function,
                    filter,
                    continue_after,
                    allow_continue_after_self,
                    priority,
                ),
            )

        return decorator

    def message(
        self,
        filter: Optional[Filter[Message]],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ):
        """Registers a handler for messages.

        Args:
            filter (`Filter[Message]`, optional): A filter that checks if the message passes the filter.
            tag (`str`): A tag for the handler. Should be unique.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
            allow_continue_after_self (`bool`, optional): Same as current adding handler tag to continue_after.
        """

        def decorator(_function: Callable[[MessageContext], Coroutine[Any, Any, None]]):
            self._dp.add.handlers.message(
                tag or _function.__name__,
                _function,
                filter,
                continue_after,
                allow_continue_after_self,
                priority,
            )

        return decorator

    def callback_query(
        self,
        filter: Optional[Filter[CallbackQuery]],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ):
        """Registers a handler for callback queries.

        Args:
            filter (`Filter[CallbackQuery]`, optional): A filter that checks if the callback query passes the filter.
            tag (`str`): A tag for the handler. Should be unique.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
            allow_continue_after_self (`bool`, optional): Same as current adding handler tag to continue_after.
        """

        def decorator(
            _function: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]]
        ):
            self._dp.add.handlers.callback_query(
                tag or _function.__name__,
                _function,
                filter,
                continue_after,
                allow_continue_after_self,
                priority,
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
        filter: Optional[Filter[CallbackQuery]] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ):
        """Registers a handler for callback queries.

        Args:
            tag (`str`): A tag for the handler. Should be unique.
            function (`Callable[[CallbackQueryContext], Coroutine[Any, Any, None]]`): The function to call.
            filter (`Filter[CallbackQuery]`, optional): A filter that checks if the callback query passes the filter.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
            allow_continue_after_self (`bool`, optional): Same as current adding handler tag to continue_after.
        """

        self._dp.add_handler(
            CallbackQueryHandler(
                self._dp,
                tag,
                function,
                filter,
                continue_after,
                allow_continue_after_self,
                priority,
            )
        )

    def message(
        self,
        tag: str,
        function: Callable[[MessageContext], Coroutine[Any, Any, None]],
        filter: Optional[Filter[Message]] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ):
        """Registers a handler for messages.

        Args:
            tag (`str`): A tag for the handler. Should be unique.
            function (`Callable[[MessageContext], Coroutine[Any, Any, None]]`): The function to call.
            filter (`Filter[Message]`, optional): A filter that checks if the message passes the filter.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
            allow_continue_after_self (`bool`, optional): Same as current adding handler tag to continue_after.
        """

        self._dp.add_handler(
            MessageHandler(
                self._dp,
                tag,
                function,
                filter,
                continue_after,
                allow_continue_after_self,
                priority,
            )
        )

    @staticmethod
    def __all(dir_path: Path):
        """Returns all directories in a directory.

        Args:
            dir_path (`str`): The path to the directory.
        """
        return (Path(dir_path).joinpath(d).resolve() for d in os.listdir(dir_path))

    @staticmethod
    def __iter_modules(
        file_path: Path, package: str = ""
    ) -> Generator[str, None, None]:
        """Returns all modules in a directory.

        Args:
            file_path (`str`): The path to the directory.
        """

        if not package:
            package = file_path.stem

        for file in AddHandlersExtensions.__all(file_path):
            if file.is_dir():
                yield from AddHandlersExtensions.__iter_modules(
                    file, package + "." + file.name
                )
            elif file.is_file() and file.suffix == ".py":
                if file.stem == "__init__":
                    continue
                yield package + "." + file.name[:-3]
            else:
                continue

    def locate(self, path: Path):
        """Registers a module for adding handlers.

        Args:
            path (`str`): The path to the directory.
        """

        for module_name in AddHandlersExtensions.__iter_modules(path):

            try:
                module = importlib.import_module(module_name)

                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, AbstractHandler):
                        if not inspect.isabstract(obj):
                            instance: AbstractHandler[Any, Any] = obj()  # type: ignore
                            instance.set_dp(self._dp)
                            self._dp.add_handler(instance)

                            yield name

            except ImportError:
                continue


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
