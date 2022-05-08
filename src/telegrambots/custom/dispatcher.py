import logging
from typing import Any, Callable, Coroutine, Optional, overload

from telegrambots.wrapper.types.objects import CallbackQuery, Message, Update

from .client import TelegramBot
from .contexts import CallbackQueryContext, MessageContext
from .contexts._contexts._continuously_handler import ContinuouslyHandlerTemplate
from .contexts._contexts.context_template import GenericContext
from .exceptions.handlers import HandlerRegistered
from .exceptions.propagations import BreakPropagation, ContinuePropagation
from .filters._filters.filter_template import Filter
from .general import TUpdate
from .handlers._handlers.handler_template import Handler, HandlerTemplate
from .handlers._handlers.update_handler import CallbackQueryHandler, MessageHandler
from .processor import ProcessorTemplate, SequentialProcessor

dispatcher_logger = logging.getLogger("telegrambots.dispatcher")


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
            handle_error (`Callable[[TelegramBot, Exception], Coroutine[None, None, None]]`, optional): A function that handles errors.
            processor_type (`type[ProcessorTemplate[Update]]`, optional): The type of processor to use. Defaults to None.
        """
        self._bot = _bot
        self._handlers: dict[type[Any], dict[str, HandlerTemplate]] = {}
        self._continuously_handlers: list[tuple[ContinuouslyHandlerTemplate]] = []
        self._handle_error = handle_error

        self._processor: ProcessorTemplate[Update]
        if processor_type is None:
            self._processor = SequentialProcessor[Update](self._process_update)
        else:
            self._processor = processor_type(self._process_update)

    @property
    def bot(self) -> TelegramBot:
        """Returns the bot."""
        return self._bot

    async def feed_update(self, update: Update):
        """Feeds an update to the dispatcher.

        Args:
            update (`Update`): The update to feed.
        """
        dispatcher_logger.info(f"Feeding update {update}")
        await self._processor.process(update)

    def handler_tag_exists(self, tag: str, update_type: type[Any]):
        """Checks if a handler with the given tag exists.

        Args:
            tag (`str`): The tag of the handler.
            update_type (`type[Any]`): The type of update to check.
        """
        if update_type not in self._handlers:
            return False
        return tag in self._handlers[update_type]

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
                f"Added a batch of continuously handlers {', '.join(f'{x.update_type}:{x.target_tag}' for x in continuously_handler)}"
            )
        else:
            dispatcher_logger.info(
                f"Added a continuously handler: {continuously_handler.update_type}:{continuously_handler.target_tag}"
            )
            self._continuously_handlers.append((continuously_handler,))

    def add_handler(self, tag: str, handler: HandlerTemplate):
        """Adds a handler to the dispatcher.

        Args:
            tag (`str`): The tag of the handler. Should be unique.
            handler (`HandlerTemplate`): The handler to add.
        """
        if handler.update_type not in self._handlers:
            dispatcher_logger.info(f"Added handler batch for {handler.update_type}s")
            self._handlers[handler.update_type] = {}

        if tag in self._handlers[handler.update_type]:
            raise HandlerRegistered(tag, handler.update_type)

        self._handlers[handler.update_type][tag] = handler
        dispatcher_logger.info(f"Added handler {handler.update_type}:{tag}")

    def add_callback_query_handler(
        self,
        tag: str,
        function: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]],
        filter: Filter[CallbackQuery],
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for callback queries.

        Args:
            tag (`str`): A tag for the handler. Should be unique.
            function (`Callable[[CallbackQueryContext], Coroutine[Any, Any, None]]`): The function to call.
            filter (`Filter[CallbackQuery]`): A filter that checks if the callback query passes the filter.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
        """

        self.add_handler(tag, CallbackQueryHandler(function, filter, continue_after))

    def add_message_handler(
        self,
        tag: str,
        function: Callable[[MessageContext], Coroutine[Any, Any, None]],
        filter: Filter[Message],
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for messages.

        Args:
            tag (`str`): A tag for the handler. Should be unique.
            function (`Callable[[MessageContext], Coroutine[Any, Any, None]]`): The function to call.
            filter (`Filter[Message]`): A filter that checks if the message passes the filter.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
        """

        self.add_handler(tag, MessageHandler(function, filter, continue_after))

    def register_update_handler(
        self,
        type_of_update: type[TUpdate],
        extractor: Callable[[Update], Optional[TUpdate]],
        filter: Filter[TUpdate],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for updates.

        Args:
            type_of_update (`type[TUpdate]`): The type of update to handle.
            extractor (`Callable[[Update], Optional[TUpdate]]`): A function that extracts the update from an update.
            filter (`Filter[TUpdate]`): A filter that checks if the update passes the filter.
            tag (`Optional[str]`, optional): A tag for the handler. Should be unique. Defaults to None.
            continue_after (`Optional[str]`, optional): The tag of the handler to continue after. Defaults to None.
        """

        def decorator(
            _function: Callable[[GenericContext[TUpdate]], Coroutine[Any, Any, None]]
        ):
            self.add_handler(
                tag or _function.__name__,
                Handler(type_of_update, extractor, _function, filter, continue_after),
            )

        return decorator

    def register_message_handler(
        self,
        filter: Filter[Message],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for messages.

        Args:
            filter (`Filter[Message]`): A filter that checks if the message passes the filter.
            tag (`str`): A tag for the handler. Should be unique.
        """

        def decorator(_function: Callable[[MessageContext], Coroutine[Any, Any, None]]):
            self.add_message_handler(
                tag or _function.__name__, _function, filter, continue_after
            )

        return decorator

    def register_callback_query_handler(
        self,
        filter: Filter[CallbackQuery],
        tag: Optional[str] = None,
        continue_after: Optional[list[str]] = None,
    ):
        """Registers a handler for callback queries.

        Args:
            filter (`Filter[CallbackQuery]`): A filter that checks if the callback query passes the filter.
            tag (`str`): A tag for the handler. Should be unique.
        """

        def decorator(
            _function: Callable[[CallbackQueryContext], Coroutine[Any, Any, None]]
        ):
            self.add_callback_query_handler(
                tag or _function.__name__, _function, filter, continue_after
            )

        return decorator

    async def _process_update(self, update: Update):
        update_type = update.update_type
        if update_type is None:
            await self._try_handle_error(ValueError(f"Unknown update type: {update}"))
            return

        for batch in self._continuously_handlers:
            for c in sorted(batch, key=lambda x: x.priority, reverse=True):
                if c.update_type == update_type:
                    if c.check_keys(update):
                        handler = self._handlers[update_type][c.target_tag]

                        if not handler.should_process(update):
                            continue

                        if handler.continue_after is not None:
                            if c.start_tag not in handler.continue_after:
                                continue

                        dispatcher_logger.info(
                            f"Processing continuously handler {c.update_type}:{c.target_tag}"
                        )
                        await self._do_handling(
                            handler, update, c.target_tag, *c.args, **c.kwargs
                        )
                        self._continuously_handlers.remove(batch)
                        return  # Don't process the update anymore

        if update_type not in self._handlers:
            return

        for k, handler in sorted(
            (k, h)
            for k, h in sorted(
                self._handlers[update_type].items(),
                key=lambda x: x[1].priority,
                reverse=True,
            )
            if not h.continue_after
        ):
            if handler.should_process(update):
                handling_result = await self._do_handling(handler, update, k)
                if handling_result is not None:
                    if handling_result:
                        continue
                    else:
                        break

    async def _do_handling(
        self,
        handler: HandlerTemplate,
        update: Update,
        handler_tag: str,
        *args: Any,
        **kwargs: Any,
    ):
        try:
            await handler.process(
                self, update, handler.update_type, handler_tag, *args, **kwargs
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
        if self._handle_error is not None:
            await self._handle_error(self._bot, e)
