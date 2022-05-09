from abc import ABC, ABCMeta
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    final,
    TYPE_CHECKING,
)

from telegrambots.wrapper.types.objects import Update

from ...general import Exctractable, TUpdate
from ...extensions.context import PropagationExtension, ContinueWithExtensions


if TYPE_CHECKING:
    from ...dispatcher import Dispatcher
    from ...client import TelegramBot


class ContextTemplate(metaclass=ABCMeta):
    def __init__(
        self, dp: "Dispatcher", update: Update, update_type: type[Any], handler_tag: str
    ):
        self.__dp = dp
        self.__update = update
        self.__update_type = update_type
        self.__handler_tag = handler_tag

        # extensions
        self.__propagation: Optional[PropagationExtension] = None
        self.__continue_with: Optional[ContinueWithExtensions] = None

    @final
    @property
    def dp(self) -> "Dispatcher":
        """Returns the dispatcher."""
        return self.__dp

    @final
    @property
    def bot(self) -> "TelegramBot":
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

    @final
    @property
    def propagation(self) -> PropagationExtension:
        """Manage propagation of the context."""
        if self.__propagation is None:
            self.__propagation = PropagationExtension(self)
        return self.__propagation

    @final
    @property
    def continue_with(self) -> ContinueWithExtensions:
        """A set of methods to enable continue_with features for the context."""
        if self.__continue_with is None:
            self.__continue_with = ContinueWithExtensions(self)
        return self.__continue_with


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
