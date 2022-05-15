import asyncio
import logging
from typing import (
    Any,
    Mapping,
    Optional,
    cast,
    final,
    overload,
    TYPE_CHECKING,
)

from telegrambots.wrapper.types.objects import Update

from .contexts._contexts._continuously_handler import ContinuouslyHandlerTemplate
from .exceptions.handlers import HandlerRegistered
from .exceptions.propagations import BreakPropagation, ContinuePropagation
from .handlers._handlers.handler_template import HandlerTemplate
from .processor import ProcessorTemplate, SequentialProcessor
from .extensions.dispatcher import AddExtensions
from .handlers import AbstractExceptionHandler, default_exception_handler
from .general import TKey

if TYPE_CHECKING:
    from .client import TelegramBot


logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
dispatcher_logger = logging.getLogger("telegrambots.dispatcher")


class Dispatcher:
    def __init__(
        self,
        _bot: "TelegramBot",
        *,
        processor_type: Optional[type[ProcessorTemplate[Update[Any]]]] = None,
    ) -> None:

        """Initializes the dispatcher.

        Args:
            bot (`TelegramBot`): The bot to use.
            handle_error (`Callable[[TelegramBot, Exception], Coroutine[None, None, None]]`, optional): A function that handles errors.
            processor_type (`type[ProcessorTemplate[Update]]`, optional): The type of processor to use. Defaults to None.
        """
        self._bot = _bot
        self._handlers: dict[type[Any], dict[str, HandlerTemplate]] = {}
        self._continuously_handlers: list[tuple[ContinuouslyHandlerTemplate]] = []
        self._handle_errors: list[AbstractExceptionHandler] = []
        self._shared_data: dict[str, Any] = {}

        self._processor: ProcessorTemplate[Update[Any]]
        if processor_type is None:
            self._processor = SequentialProcessor[Update[Any]](self._process_update)
        else:
            self._processor = processor_type(self._process_update)

        # extensions
        self.__add: Optional[AddExtensions] = None

    @final
    @property
    def bot(self) -> "TelegramBot":
        """Returns the bot."""
        return self._bot

    @final
    @property
    def add(self) -> AddExtensions:
        """Extensions to add different things to the dispatcher."""
        if self.__add is None:
            self.__add = AddExtensions(self)
        return self.__add

    async def feed_update(self, update: Update[Any]):
        """Feeds an update to the dispatcher.

        Args:
            update (`Update`): The update to feed.
        """
        dispatcher_logger.info(
            f"Feeding update {cast(type, update.update_type).__name__}:{update.update_id}"
        )
        await self._processor.process(update)

    def unlimited(self, *allowed_updates: str):
        """Sets the dispatcher to unlimited mode. receiving updates till unlimited timout."""
        asyncio.run(self._unlimited(*allowed_updates))

    def handler_tag_exists(self, tag: str, update_type: type[Any]):
        """Checks if a handler with the given tag exists.

        Args:
            tag (`str`): The tag of the handler.
            update_type (`type[Any]`): The type of update to check.
        """
        if update_type not in self._handlers:
            return False
        return tag in self._handlers[update_type]

    def add_shared_data(self, key: str, value: TKey) -> TKey:
        """Adds a shared data to the dispatcher.

        Args:
            key (`str`): The key of the shared data.
            value (`TKey`): The value of the shared data.
        """
        self._shared_data[key] = value
        return value

    def add_handler(self, handler: HandlerTemplate):
        """Adds a handler to the dispatcher.

        Args:
            tag (`str`): The tag of the handler. Should be unique.
            handler (`HandlerTemplate`): The handler to add.
        """
        if handler.update_type not in self._handlers:
            dispatcher_logger.info(
                f"Added handler batch for {handler.update_type.__name__}s"
            )
            self._handlers[handler.update_type] = {}

        if handler.tag in self._handlers[handler.update_type]:
            raise HandlerRegistered(handler.tag, handler.update_type)

        self._handlers[handler.update_type][handler.tag] = handler
        dispatcher_logger.info(
            f"Added handler {handler.update_type.__name__}:{handler.tag}"
        )

    def add_exception_handler(self, exception_handler: AbstractExceptionHandler):
        """Adds an exception handler to the dispatcher.

        Args:
            exception_handler (`AbstractExceptionHandler`): The exception handler to add.
        """
        self._handle_errors.append(exception_handler)

    def add_default_exception_handler(self):
        """Adds the default exception handler to the dispatcher."""
        self.add_exception_handler(default_exception_handler)

    @overload
    def add_continuously_handler(
        self,
        continuously_handler: ContinuouslyHandlerTemplate,
    ):
        """Adds a handler for continuously updates."""
        ...

    @overload
    def add_continuously_handler(
        self,
        continuously_handler: tuple[ContinuouslyHandlerTemplate],
    ):
        """Adds a handler for continuously updates."""
        ...

    def add_continuously_handler(
        self,
        continuously_handler: ContinuouslyHandlerTemplate
        | tuple[ContinuouslyHandlerTemplate],
    ):
        """Adds a handler for continuously updates."""

        if isinstance(continuously_handler, (tuple, list)):
            self._continuously_handlers.append(continuously_handler)
            dispatcher_logger.info(
                f"Added a batch of continuously handlers {', '.join(f'{x.update_type.__name__}:{x.target_tag}' for x in continuously_handler)}"
            )
        else:
            dispatcher_logger.info(
                f"Added a continuously handler: {continuously_handler.update_type.__name__}:{continuously_handler.target_tag}"
            )
            self._continuously_handlers.append((continuously_handler,))

    async def _unlimited(self, *allowed_updates: str):
        async with self.bot:
            async for update in self.bot.stream_updates(list(allowed_updates)):
                await self.feed_update(update)

    async def _process_update(self, update: Update[Any]):
        update_type = update.update_type
        if update_type is None:
            await self._try_handle_error(ValueError(f"Unknown update type: {update}"))
            return

        for batch in self._continuously_handlers:
            for c in sorted(batch, key=lambda x: x.priority, reverse=True):
                if c.update_type == update_type:
                    if c.check_keys(update):
                        handler = self._handlers[update_type][c.target_tag]

                        result = handler.should_process(update)
                        if not result.result:
                            continue

                        if handler.continue_after is not None:
                            if c.start_tag not in handler.continue_after:
                                continue

                        dispatcher_logger.info(
                            f"Processing continuously handler {c.update_type.__name__}:{c.target_tag}"
                        )
                        c.kwargs.update(continue_with_key=c.keys)
                        await self._do_handling(
                            handler,
                            update,
                            result.metadata,
                            *c.args,
                            **c.kwargs,
                        )
                        self._continuously_handlers.remove(batch)
                        return  # Don't process the update anymore

        if update_type not in self._handlers:
            return

        for _, handler in sorted(
            (_, h)
            for _, h in sorted(
                self._handlers[update_type].items(),
                key=lambda x: x[1].priority,
                reverse=True,
            )
            if not h.continue_after
        ):
            result = handler.should_process(update)
            if result.result:
                handling_result = await self._do_handling(
                    handler, update, result.metadata
                )
                if handling_result is not None:
                    if handling_result:
                        continue
                    else:
                        break

    async def _do_handling(
        self,
        handler: HandlerTemplate,
        update: Update[Any],
        filter_data: Mapping[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        kwargs |= self._shared_data
        try:
            await handler.process(
                update,
                filter_data,
                *args,
                **kwargs,
            )
        except ContinuePropagation:
            return True  # -> continue to next handler
        except BreakPropagation:
            return False  # -> break from loop
        except Exception as e:
            # -> handle error
            try:
                await self._try_handle_error(e)
            except:
                pass
        return None

    async def _try_handle_error(self, e: Exception):
        for handler in self._handle_errors:
            await handler.try_handle(self, e)
