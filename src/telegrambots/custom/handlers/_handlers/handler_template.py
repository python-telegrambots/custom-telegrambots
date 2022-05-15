from abc import ABC, ABCMeta, abstractmethod
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    Mapping,
    Optional,
    TypeVar,
    final,
    TYPE_CHECKING,
)

from ...contexts._contexts.context_template import Context
from ...general import (
    Exctractable,
    TUpdate,
    check,
    extract,
    ContainedResult,
    general_extractor,
)

if TYPE_CHECKING:
    from telegrambots.wrapper.types.objects import Update

    from ...filters._filters.filter_template import Filter
    from ...dispatcher import Dispatcher


class HandlerTemplate(metaclass=ABCMeta):
    @abstractmethod
    async def __process__(
        self,
        update: "Update[Any]",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        ...

    @abstractmethod
    def should_process(self, update: "Update[Any]") -> ContainedResult:
        ...

    @property
    @abstractmethod
    def update_type(self) -> type[Any]:
        ...

    @property
    @abstractmethod
    def tag(self) -> str:
        ...

    @property
    @abstractmethod
    def dp(self) -> "Dispatcher":
        ...

    @property
    def continue_after(self) -> Optional[list[str]]:
        return None

    @property
    def priority(self) -> int:
        return 0

    async def process(
        self,
        update: "Update[Any]",
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs.update(**filter_data)
        return await self.__process__(
            update,
            filter_data,
            *args,
            **kwargs,
        )


class GenericHandler(Generic[TUpdate], Exctractable[TUpdate], ABC, HandlerTemplate):
    def __init__(
        self,
        tag: str,
        update_type: type[TUpdate],
        dp: Optional["Dispatcher"] = None,
        filter: Optional["Filter[TUpdate]"] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__()
        self.__dp = dp
        self.__tag = tag
        self.__filter = filter
        self.__update_type = update_type
        self.__priority = priority

        if not self.__tag:
            raise ValueError("Tag cannot be None or Empty.")

        if not self.__update_type:
            raise ValueError("Update type cannot be None or Empty.")

        if allow_continue_after_self:
            if continue_after:
                if tag not in continue_after:
                    continue_after = continue_after + [tag]
            else:
                continue_after = [tag]

        self._continue_after = continue_after

    @final
    def __extractor__(self, update: "Update[TUpdate]") -> TUpdate:
        return general_extractor(update)

    @abstractmethod
    async def __process__(
        self,
        update: "Update[TUpdate]",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        ...

    @final
    def should_process(self, update: "Update[TUpdate]") -> ContainedResult:
        if self.__filter is None:
            return ContainedResult(True, {})
        checked = check(self.__filter, extract(self, update))
        return ContainedResult(checked, self.__filter)

    @final
    @property
    def tag(self) -> str:
        return self.__tag

    @final
    @property
    def continue_after(self) -> Optional[list[str]]:
        return self._continue_after

    @final
    @property
    def update_type(self) -> type[TUpdate]:
        return self.__update_type

    @final
    @property
    def priority(self) -> int:
        return self.__priority

    @final
    @property
    def dp(self) -> "Dispatcher":
        if self.__dp is None:
            raise ValueError("Dispatcher not set!")
        return self.__dp

    @final
    def set_dp(self, dp: "Dispatcher") -> None:
        self.__dp = dp


TContext = TypeVar("TContext", bound=Context[Any])


class AbstractHandler(Generic[TContext, TUpdate], GenericHandler[TUpdate], ABC):
    def __init__(
        self,
        tag: str,
        update_type: type[TUpdate],
        dp: Optional["Dispatcher"] = None,
        filter: Optional["Filter[TUpdate]"] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            tag,
            update_type,
            dp,
            filter,
            continue_after,
            allow_continue_after_self,
            priority,
        )

    @final
    async def __process__(
        self,
        update: "Update[TUpdate]",
        *args: Any,
        **kwargs: Any,
    ):
        return await self._process(self._build_context(update, *args, **kwargs))

    @abstractmethod
    async def _process(self, context: TContext) -> None:
        ...

    @abstractmethod
    def _build_context(
        self,
        update: "Update[TUpdate]",
        *args: Any,
        **kwargs: Any,
    ) -> TContext:
        ...


class SealedHandler(Generic[TContext, TUpdate], AbstractHandler[TContext, TUpdate]):
    def __init__(
        self,
        dp: "Dispatcher",
        tag: str,
        update_type: type[TUpdate],
        processor: Callable[[TContext], Awaitable[None]],
        filter: Optional["Filter[TUpdate]"] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            tag,
            update_type,
            dp,
            filter,
            continue_after,
            allow_continue_after_self,
            priority,
        )

        if dp is None:
            raise ValueError("Dispatcher not set!")

        self._processor = processor

    @final
    async def _process(self, context: TContext) -> None:
        await self._processor(context)

    @abstractmethod
    def _build_context(
        self,
        update: "Update[TUpdate]",
        *args: Any,
        **kwargs: Any,
    ) -> TContext:
        ...


class Handler(Generic[TUpdate], SealedHandler[Context[TUpdate], TUpdate]):
    def __init__(
        self,
        dp: "Dispatcher",
        tag: str,
        update_type: type[TUpdate],
        processor: Callable[[Context[TUpdate]], Awaitable[None]],
        filter: Optional["Filter[TUpdate]"] = None,
        continue_after: Optional[list[str]] = None,
        allow_continue_after_self: bool = False,
        priority: int = 0,
    ) -> None:
        super().__init__(
            dp,
            tag,
            update_type,
            processor,
            filter,
            continue_after,
            allow_continue_after_self,
            priority,
        )

    @final
    def _build_context(self, update: "Update[TUpdate]", *args: Any, **kwargs: Any):
        return Context(
            self.dp,
            update,
            self.update_type,
            self.tag,
            *args,
            **kwargs,
        )
