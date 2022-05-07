# Custom TelegramBots

A set of custom classes and helpers to work with telegram bots.

_Enjoy strongly typed and heavily type hinted things._

## Installation

The package is available at [PYPI](https://pypi.org/project/telegrambots-custom/)

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

### Let have some fun

So, it's a happy day and you're creating a new handler to receive some info from user.

Here's how you do it to get user's name ( as before ).

``` py

# ---- sniff ----

@dp.register_message_handler(mf.regex("^/start") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text("Please gimme you name ...")

```

This is where you may go deep thinking ... Where should i get that name ?

Maybe you need another handler to receive what user sends after.

``` py

# ---- sniff ----

@dp.register_message_handler(mf.regex("^/give") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text("Please gimme you name ...")


@dp.register_message_handler(mf.text_message & mf.private)
async def gimme_name(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text(f"Then your name is {context.update.text}!")

```

But this is not right, is it?

- How do we know the text message is related to `/give` command ?
- The second handler is called on every text message!
- ...

So you need a way to keep track of a user, right?

Here's where this package mages!!

You can use `@context.continue_with_this_message` decorator inside your handler.

It's much likely similar to `@dp.register_message_handler`, except it takes one more parameter before filter. And it's a `key_resolver`.

Key resolver helps us know "what should we track?" in this case it's user's id from message.

Let's get to work:

``` py
@dp.register_message_handler(mf.regex("^/give") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text("Please gimme you name ...")

    if context.update.from_user: # make sure the message has a user to track the id.

        @context.continue_with_this_message( # this is the actual mage! it make these two handlers related to each other.
            key_resolver=MessageSenderId(context.update.from_user.id), # keep track of user using it's unique id.
            filter=mf.text_message & mf.private, # any text message is ok here!
            tag="give_name", # It's optional! you can name the function below instead.
        )
        async def _(context: MessageContext):
            # Now you're 100% sure that this callback function is called only after a call to parent callback "handle_message".
            # Then it's what you actually want.
            await context.reply_text(f"Ahh, your name is {context.update.text}!")

```

Amazing ? it's not finished yet!

What if you need another info? like user's age? NO PROBLEM! repeat what you did before.

``` py
@dp.register_message_handler(mf.regex("^/give") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text("Please gimme you name ...")

    if context.update.from_user: 

        @context.continue_with_this_message(
            key_resolver=MessageSenderId(context.update.from_user.id),
            filter=mf.text_message & mf.private,
            tag="give_name"
        )
        async def _(context: MessageContext):
            await context.reply_text(f"Ahh, your name is {context.update.text}!")
            
            # ---- new code ----
            # Let's ask for user's age
            await context.reply_text(f"What's your age then?")

            if context.update.from_user:

                # Again
                @context.continue_with_this_message(
                    key_resolver=MessageSenderId(context.update.from_user.id),
                    filter=mf.text_message & mf.private,
                    tag="give_age", # Another name, it's important!
                    name=context.update.text,  # -> you can pass custom data to handler. they're available in callback's *args or **kwargs.
                )
                async def _(context: MessageContext, *args: Any, **kwargs: Any):
                    await context.reply_text(
                        f"So {kwargs['name']}, your age is {context.update.text}!"
                    )
```

_Are you excited now?_
