from .processor_template import ProcessorTemplate, TItem
import typing


class SequentialProcessor(typing.Generic[TItem], ProcessorTemplate[TItem]):
    """Processor that processes items sequentially."""

    def __init__(
        self,
        to_process: typing.Callable[
            [TItem], typing.Coroutine[typing.Any, typing.Any, None]
        ],
    ) -> None:
        super().__init__(to_process)

    @typing.final
    async def __processor__(self, item: TItem) -> None:
        await self._do_job(item)
