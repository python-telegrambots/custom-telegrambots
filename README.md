# Custom TelegramBots

_I'll make you excited!_

A set of custom classes and helpers to work with telegram bots.

_Enjoy strongly typed and heavily type hinted things._

## Installation

The package is available at [PYPI](https://pypi.org/project/telegrambots-custom/)

## Simple usage example

_Package is in preview state and theses are all in preview and may change later._

See [Wiki](https://github.com/python-telegrambots/custom-telegrambots/wiki/) for more working examples.

```py
from telegrambots.custom import (
    TelegramBot,
    MessageContext,
    message_filters as mf,
)  # -> filters for each update type are in separate modules.


# Create main bot object, this object may contains all available api methods.
bot = TelegramBot("BOT_TOKEN")

# Dispatcher is to process updates and dispatches them to handlers.
dp = bot.dispatcher  # By default, the dispatcher will process updates sequentially.

dp.add_default_exception_handler()  # Simple err handler that prints error message.


# Use decorator to register handler for each update type.
# You can use filters and combine them.
@dp.add.handlers.via_decorator.message(mf.Regex("^/start") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text(
        "Started"
    )  # -> bound method for messages, only available in `MessageContext`


if __name__ == "__main__":
    # Fire up the event loop.
    dp.unlimited()

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
    processor_type=ParallelProcessor,  # Now the dispatcher will use ParallelProcessor.
    # And it will process updates in parallel.
)
```

### Manage propagation of handlers

Stop processing this handler or all of pending handlers.

```py
@dp.add.handlers.via_decorator.message(mf.regex("^/start") & mf.private)
async def handle_message(context: MessageContext):
    await context.reply_text(
        "Started"
    )

    context.propagation.stop()  # -> stop propagating this update to other handlers.

    # ---- or ----

    context.propagation.resume()  # -> continue propagating this update to other handlers.

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
        self._set_metadata("balh", "Ablah")
        return True

    # ---- or anything you like ----

# @dp.add.handlers.via_decorator.message(AdvancedMessageFilter())
#    ---- sniff ----

    context["balh"] # Ablah
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

# @dp.add.handlers.via_decorator.message(regex('start'))
#    ...
```

### Let have some fun

So, it's a happy day and you're creating a new handler to receive some info from user.

Here's how you do it to get user's name ( as before ).

``` py

# ---- sniff ----

@dp.add.handlers.via_decorator.message(mf.regex("^/start") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text("Please gimme you name ...")

```

This is where you may go deep thinking ... Where should i get that name ?

Maybe you need another handler to receive what user sends after.

``` py

# ---- sniff ----

@dp.add.handlers.via_decorator.message(mf.regex("^/give") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text("Please gimme you name ...")


@dp.add.handlers.via_decorator.message(mf.text_message & mf.private)
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

You can use `@context.continue_with.this.message` decorator inside your handler.

It's much likely similar to `@dp.register_message_handler`, except it takes one more parameter before filter. And it's a `keys`.

Key resolver helps us know "what should we track?" in this case it's user's id from message.

Let's get to work:

``` py
@dp.add.handlers.via_decorator.message(mf.regex("^/give") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text("Please gimme you name ...")

    if context.update.from_user: # make sure the message has a user to track the id.

        @context.continue_with.this.message( # this is the actual mage! it make these two handlers related to each other.
            keys=[MessageSenderId(context.update.from_user.id)], # keep track of user using it's unique id.
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
@dp.add.handlers.via_decorator.message(mf.regex("^/give") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text("Please gimme you name ...")

    if context.update.from_user:

        @context.continue_with.this.message(
            keys=[MessageSenderId(context.update.from_user.id)],
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
                @context.continue_with.this.message_from( # same as keys=[MessageSenderId(context.update from_user.id)],

                    filter=mf.text_message & mf.private,
                    tag="give_age", # Another name, it's important!
                    name=context.update.text,  # -> you can pass custom data to handler. they're available in callback's *args or **kwargs.
                )
                async def _(context: MessageContext, *args: Any, **kwargs: Any):
                    await context.reply_text(
                        f"So {kwargs['name']}, your age is {context.update.text}!"
                    )
```

#### What about fallback or something

Sometimes, you need to apply a fallback for user. as example: when user sends something unrelated, you wanna tell him try again or something.

To do this, your starter handler should continue with two or more other handlers: one for requested response and other for unrelated updates. And you can do this as well!

This approach is different from previous. the only difference is that you can't create handlers inside current handlers and they should be created like normal handlers.

Let's create our three handlers

- Starter handler
- Requested response handler
- Unrelated update handler

``` py

# ---- sniff ----

# Our starter handler.
@dp.add.handlers.via_decorator.message(mf.regex("^/start") & mf.private)
async def handle_message(context: MessageContext):
    await context.reply_text("Please gimme you name ...")

# Here we excepted a valid text message.
@dp.add.handlers.via_decorator.message(filter=mf.text_message)
async def give_name(context: MessageContext):
    await context.reply_text(f"Ahh, your name is {context.update.text}!")

# All other type of messages ( non-text ) should go here.
@dp.add.handlers.via_decorator.message(filter=mf.any_message)
async def unrelated(context: MessageContext):
    await context.reply_text("Please try again with a text message.")

```

#### Let's make these three related

Here you can use method `context.continue_with_many`, it allows an handler to be continued with more than one handlers

> You need to import `from telegrambots.custom.contexts import ContinueWithInfo` in other to add your handlers to this.

Let's modify starter handler:

``` py
# Use decorator to register handler for each update type.
# You can use filters and combine them.
@dp.add.handlers.via_decorator.message(mf.regex("^/start") & mf.private)
async def handle_message(context: MessageContext):
    await context.reply_text("Please gimme you name ...")

    if context.update.from_user:
        keys = [MessageSenderId(context.update.from_user.id)] # keys is same for both. ( it should be a list )
        context.continue_with.many(
            ContinueWithInfo.with_message("give_name", keys, priority=1), # first of all try to continue with `"give_name"` if possible ( filters should pass )
            # If this handler is invoked, we'll stop propagation! so the next one is not triggered.
            ContinueWithInfo.with_message("unrelated", keys, priority=0), # If the first handler is not triggered and we reached this point, it means the update is unrelated.
        )
```

Next, we should tell other two handler, to only be triggered after our starter handler.

```py
@dp.add.handlers.via_decorator.message(filter=mf.text_message, continue_after=["handle_message"]) # continue only after `"handle_message"`
async def give_name(context: MessageContext):
    await context.reply_text(f"Ahh, your name is {context.update.text}!")
    context.propagation.stop() # At this point we received what we needed. then stop.


@dp.add.handlers.via_decorator.message(filter=mf.any_message, continue_after=["handle_message"]) # continue only after `"handle_message"`
async def unrelated(context: MessageContext):
    await context.reply_text("Please try again with a text message.")

```

Now it's a working example, but it works only ones. ( I the update is unrelated, we just notify user all things are over ).

But we need our customer to have chances to retry.

In order to do that, we can tell our unrelated handler to continue with `"give_name"` and even itself!

Let's modify unrelated method.

```py
@dp.add.handlers.via_decorator.message(
    filter=mf.any_message, continue_after=["handle_message", "unrelated"] # notice we added this methods name to `continue_after`, so it can be continued with after itself ( user sends multiple unrelated updates in a row )

    # You can use allow_continue_after_self = True, which dose the same.
)
async def unrelated(context: MessageContext):
    await context.reply_text("Please try again with a text message.")
    if context.update.from_user:
        # Used to resolve the key for the context.
        keys = [MessageSenderId(context.update.from_user.id)]
        context.continue_with.many( # now this method can also trigger `"give_name"` or itself based on received update. It creates a loop till we get our right answer.
            ContinueWithInfo.with_message("give_name", keys, priority=1),
            ContinueWithInfo.with_message("unrelated", keys, priority=0),
        )
```

You need to add `"unrelated"` to `"give_name"`'s `continue_after` parameter, so it can be continued after `"unrelated"` for a "try again".

```py
@dp.add.handlers.via_decorator.message(
    filter=mf.text_message, continue_after=["handle_message", "unrelated"]
)
async def give_name(context: MessageContext):
    await context.reply_text(f"Ahh, your name is {context.update.text}!")
    context.propagation.stop()
```

now everything is ready! fast and clear.

Let see full example

```py
from telegrambots.custom import (
    TelegramBot,
    message_filters as mf,
    ContinueWithInfo,
    MessageContext,
)


bot = TelegramBot("BOT_TOKEN")
dp = bot.dispatcher

dp.add_default_exception_handler()


@dp.add.handlers.via_decorator.message(
    filter=mf.text_message & mf.private, continue_after=["handle_message", "unrelated"]
)
async def give_name(context: MessageContext):
    await context.reply_text(f"Ahh, your name is {context.update.text}!")
    context.propagation.stop()


@dp.add.handlers.via_decorator.message(
    filter=mf.any_message & mf.private,
    continue_after=["handle_message"],
    allow_continue_after_self=True,
)
async def unrelated(context: MessageContext):
    await context.reply_text("Please try again with a text message.")

    if context.update.from_user:
        user_id = context.update.from_user.id
        context.continue_with.many(
            ContinueWithInfo.with_message_from("give_name", user_id, priority=1),
            ContinueWithInfo.with_message_from("unrelated", user_id, priority=0),
        )


@dp.add.handlers.via_decorator.message(mf.Regex("^/start") & mf.private)
async def handle_message(context: MessageContext):
    await context.reply_text("Please gimme you name ...")

    if context.update.from_user:
        user_id = context.update.from_user.id
        context.continue_with.many(
            ContinueWithInfo.with_message_from("give_name", user_id, priority=1),
            ContinueWithInfo.with_message_from("unrelated", user_id, priority=0),
        )


if __name__ == "__main__":
    dp.unlimited()

```

> Remember, all continue_with like methods stop execution of the current handler. and nothing after them is gonna work inside handler.

_Are you excited now?_
