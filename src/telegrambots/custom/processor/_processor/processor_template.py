from abc import ABC, abstractmethod
import typing


TItem = typing.TypeVar("TItem")


class ProcessorTemplate(typing.Generic[TItem], ABC):
    """Abstract base class for processors."""

    def __init__(
        self,
        to_process: typing.Callable[
            [TItem], typing.Coroutine[typing.Any, typing.Any, None]
        ],
    ) -> None:
        super().__init__()
        self._to_process = to_process

    @abstractmethod
    async def __processor__(self, item: TItem):
        ...

    @typing.final
    async def process(self, item: TItem) -> None:
        """Processes an item.
        Args:
            item (`TItem`): The item to process.
        """
        await self.__processor__(item)

    @typing.final
    async def _do_job(self, item: TItem) -> None:
        """Processes an item.
        Args:
            item (`TItem`): The item to process.
        """
        await self._to_process(item)


# sequential
# parallel
# advanced
# custom
