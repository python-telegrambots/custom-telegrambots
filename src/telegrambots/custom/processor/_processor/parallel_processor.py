from .processor_template import ProcessorTemplate, TItem
import typing
import asyncio


class ParallelProcessor(typing.Generic[TItem], ProcessorTemplate[TItem]):
    """Processor that processes items in parallel."""

    def __init__(
        self,
        to_process: typing.Callable[
            [typing.Any], typing.Coroutine[typing.Any, typing.Any, None]
        ],
    ) -> None:
        super().__init__(to_process)

    async def __processor__(self, item: typing.Any) -> None:
        asyncio.create_task(self._do_job(item))
