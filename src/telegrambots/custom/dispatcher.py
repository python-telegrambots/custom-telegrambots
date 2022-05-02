from typing import Any, Callable, Coroutine, Optional

from telegrambots.wrapper.types.objects import CallbackQuery, Message, Update

from .client import TelegramBot
from .contexts import CallbackQueryContext, MessageContext
from .contexts._contexts.context_template import GenericContext
from .exceptions.propagations import BreakPropagation, ContinuePropagation
from .filters._filters.filter_template import Filter
from .general import TUpdate
from .handlers._handlers.handler_template import Handler, HandlerTemplate
from .handlers._handlers.update_handler import CallbackQueryHandler, MessageHandler
from .processor import ProcessorTemplate, SequentialProcessor


class Dispatcher:
    def __init__(
        self,
        _bot: TelegramBot,
        *,
        handle_error: Optional[
            Callable[[TelegramBot, Exception], Coroutine[Any, Any, None]]
        ] = None,
        processor_type: Optional[type[ProcessorTemplate[Update]]] = None,
    ) -> None:

        """Initializes the dispatcher.

        Args:
            bot (`TelegramBot`): The bot to use.
            _handle_error (`Callable[[TelegramBot, Exception], Coroutine[None, None, None]]`, optional): A function that handles errors.
        """
        self._bot = _bot
        self._handlers: list[HandlerTemplate] = []
        self._handle_error = handle_error

        self._processor: ProcessorTemplate[Update]
        if processor_type is None:
            self._processor = SequentialProcessor[Update](self._process_update)
        else:
            self._processor = processor_type(self._process_update)

    async def _process_update(self, update: Update):
        for handler in self._handlers:
            if handler.should_process(update):
                try:
                    await handler.process(self._bot, update)
                except ContinuePropagation:
                    continue  # -> continue to next handler
                except BreakPropagation:
                    break  # -> break from loop
                except Exception as e:
                    # -> handle error
                    if self._handle_error is not None:
                        await self._handle_error(self._bot, e)

    async def feed_update(self, update: Update):
        """Feeds an update to the dispatcher.

        Args:
            update (`Update`): The update to feed.
        """
        await self._processor.process(update)

    def add_handler(self, handler: HandlerTemplate):
        """Adds a handler to the dispatcher.

        Args:
            handler (`HandlerTemplate`): The handler to add.
        """
        self._handlers.append(handler)

    def register_update_handler(
        self,
        _extractor: Callable[[Update], Optional[TUpdate]],
        _filter: Filter[TUpdate],
    ):
        """Registers a handler for updates.

        Args:
            _extractor (`Callable[[Update], Optional[TUpdate]]`): A function that extracts the update from an update.
            _filter (`Filter[TUpdate]`): A filter that checks if the update passes the filter.
        """

        def decorator(
            _function: Callable[[GenericContext[TUpdate]], Coroutine[Any, Any, None]]
        ):
            self.add_handler(Handler(_extractor, _function, _filter))

        return decorator

    def register_message_handler(self, _filter: Filter[Message]):
        """Registers a handler for messages.

        Args:
            _filter (`Filter[Message]`): A filter that checks if the message passes the filter.
        """

        def decorator(_function: Callable[[MessageContext], Coroutine[Any, Any, None]]):
            self.add_handler(MessageHandler(_function, _filter))

        return decorator

    def register_callback_query_handler(self, _filter: Filter[CallbackQuery]):
        """Registers a handler for callback queries.

        Args:
            _filter (`Filter[CallbackQuery]`): A filter that checks if the callback query passes the filter.
        """

        def decorator(
            _function: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]]
        ):
            self.add_handler(CallbackQueryHandler(_function, _filter))

        return decorator
