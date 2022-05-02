# Custom TelegramBots

A set of custom classes and helpers to work with telegram bots.

_Enjoy strongly typed and heavily type hinted things._

## Simple usage example

_Package is in preview state and theses are all in preview and may change later._

```py
import asyncio

from telegrambots.custom import TelegramBot, Dispatcher
from telegrambots.custom.contexts import MessageContext

from telegrambots.custom import (
    message_filters as mf,
)  # -> filters for each update type are in separate modules.

# you can easily add new filters by importing them and adding them to the list.

# Create main bot object, this object may contains all available api methods.
bot = TelegramBot("BOT_TOKEN")


# A function to handle errors inside handlers.
async def handle_error(_: TelegramBot, e: Exception):
    print(e)


# Dispatcher is to process updates and dispatches them to handlers.
dp = Dispatcher(
    bot, handle_error
)  # By default, the dispatcher will process updates sequentially.


# Use decorator to register handler for each update type.
# You can use filters and combine them.
@dp.register_message_handler(mf.regex("^/start") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text(
        "Started"
    )  # -> bound method for messages, only available in `MessageContext`
    await asyncio.sleep(5)
    await context.reply_text("Done")


async def main():
    me = await bot.get_me()
    print(me.pretty_str())  # let's know who we are.

    print("Streaming updates ...")
    # For now you should fetch updates manually and feed them to dispatcher.
    async for update in bot.stream_updates(["message"]):
        await dp.feed_update(update)


if __name__ == "__main__":
    # Fire up the event loop.
    asyncio.run(main())
```

### Process updates in parallel

Dispatcher processes updates sequentially by default. but you can change the behavior.

```py
# ---- sniff ----

from src.telegrambots.custom.processor import ParallelProcessor

# ---- sniff ----

# Dispatcher is to process updates and dispatches them to handlers.
dp = Dispatcher(
    bot,
    handle_error=handle_error,
    processor_type=ParallelProcessor,  # Now the dispatcher will use ParallelProcessor.
    # And it will process updates in parallel.
)
```

### Manage propagation of handlers

Stop processing this handler or all of pending handlers.

```py
@dp.register_message_handler(mf.regex("^/start") & mf.private)
async def handle_message(context: MessageContext):
    await context.reply_text(
        "Started"
    )

    context.stop_propagation()  # -> stop propagating this update to other handlers.

    # ---- or ----

    context.continue_propagation()  # -> continue propagating this update to other handlers.

```

### Custom filters

You can create custom filters for any type of update.

#### Abstractly ( Slow, Featured )

Create a class that inherit from `Filter`, then setup your filter.

```py
from typing import Optional

from src.telegrambots.custom.filters import Filter
from telegrambots.wrapper.types.objects import Message


class AdvancedMessageFilter(Filter[Message]):
    def __init__(self) -> None:
        super().__init__()
        # ---- do your initialization here ----

    def __check__(self, update: Optional[Message]) -> bool:
        # ---- check if update is a valid for your case ----
        return True

    # ---- or anything you like ----

# @dp.register_message_handler(AdvancedMessageFilter())
#    ...
```

#### Using factories ( Fast, Low options )

Or you can use filter factories ( available for each type of update ) to quickly create filter.

```py
import re

from src.telegrambots.custom.filters.messages import message_filter_factory


def regex(pattern: str | re.Pattern[str]):
    if isinstance(pattern, str):
        ap = re.compile(pattern)
    else:
        ap = pattern

    return message_filter_factory(
        lambda message: message.text is not None and ap.match(message.text) is not None
    )

# @dp.register_message_handler(regex('start'))
#    ...
```

...
