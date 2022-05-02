# Custom TelegramBots

A set of custom classes and helpers to work with telegram bots.

_Enjoy strongly typed and heavily type hinted things._

## Simple usage example

_Package is in preview state and theses are all in preview and may change later._

```py
import asyncio

from telegrambots.custom.client import TelegramBot
from telegrambots.custom.contexts import MessageContext
from telegrambots.custom.dispatcher import Dispatcher

import telegrambots.custom.filters.messages as mf  # -> filters for each update type are in separate modules.

# you can easily add new filters by importing them and adding them to the list.

# Create main bot object, this object may contains all available api methods.
bot = TelegramBot("BOT_TOKEN")

# Dispatcher is to process updates and dispatches them to handlers.
dp = Dispatcher(bot)


# Use decorator to register handler for each update type.
# You can use filters and combine them.
@dp.register_message_handler(mf.regex("^/start") & mf.private)
async def handle_message(
    context: MessageContext,
):  # -> async callback function to handle update
    await context.reply_text(
        "Started"
    )  # -> bound method for messages, only available in `MessageContext`


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
