from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Coroutine
from traceback import print_exception

if TYPE_CHECKING:
    from ...dispatcher import Dispatcher


class AbstractExceptionHandler(ABC):
    def __init__(self, type: type[Exception], exact_exception: bool = False) -> None:
        super().__init__()
        self._exact = exact_exception
        self._type = type

    @abstractmethod
    async def _handle_exception(self, dp: "Dispatcher", e: Exception):
        ...

    def should_handle(self, e: Exception):
        if self._exact:
            return isinstance(e, self._type)
        else:
            return issubclass(type(e), self._type)

    async def try_handle(self, dp: "Dispatcher", e: Exception):
        if self.should_handle(e):
            await self._handle_exception(dp, e)


class ExceptionHandler(AbstractExceptionHandler):
    def __init__(
        self,
        handle: Callable[["Dispatcher", Exception], Coroutine[Any, Any, None]],
        type: type[Exception],
        exact_exception: bool = False,
    ) -> None:
        super().__init__(type, exact_exception)
        self._handle = handle

    async def _handle_exception(self, dp: "Dispatcher", e: Exception):
        return await self._handle(dp, e)


async def __handle_exception(dp: "Dispatcher", e: Exception):
    print_exception(e)


default_exception_handler = ExceptionHandler(__handle_exception, Exception)
