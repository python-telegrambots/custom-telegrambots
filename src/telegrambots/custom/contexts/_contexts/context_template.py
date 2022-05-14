from typing import (
    Any,
    Generic,
    Mapping,
    Optional,
    final,
    TYPE_CHECKING,
)

from telegrambots.wrapper.types.objects import Update

from ...general import TUpdate
from ...extensions.context import PropagationExtension, ContinueWithExtensions
from ...general import TKey


if TYPE_CHECKING:
    from ...dispatcher import Dispatcher
    from ...client import TelegramBot


class Context(Generic[TUpdate], Mapping[str, Any]):
    def __init__(
        self,
        dp: "Dispatcher",
        update: Update[TUpdate],
        update_type: type[Any],
        handler_tag: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.__dp = dp
        self.__update = update
        self.__update_type = update_type
        self.__handler_tag = handler_tag
        self.__args = args
        self.__metadata = kwargs

        # extensions
        self.__propagation: Optional[PropagationExtension] = None
        self.__continue_with: Optional[ContinueWithExtensions] = None

    def __getitem__(self, name: str):
        return self.kwargs[name]

    def __setitem__(self, name: str, value: Any):
        self.kwargs[name] = value

    def __iter__(self):
        return iter(self.kwargs)

    def __len__(self) -> int:
        return len(self.kwargs)

    @final
    @property
    def update(self) -> TUpdate:
        """`TUpdate`: Update instance"""
        return self.wrapper_update.actual_update

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
    def wrapper_update(self) -> Update[TUpdate]:
        return self.__update

    @final
    @property
    def args(self):
        return self.__args

    @final
    @property
    def kwargs(self):
        return self.__metadata

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

    def try_get_data(
        self, /, name: str, type_of_data: type[TKey] = None
    ) -> Optional[TKey]:
        """Try to get data from the context.

        Args:
            name: Name of the data.
            type_of_data: Type of the data ( Hint only ).
        """
        if name in self.kwargs:
            return self.kwargs[name]
        return None
