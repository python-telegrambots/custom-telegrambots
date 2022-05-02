from typing import Optional

from telegrambots.wrapper.client import TelegramBotsClient
from telegrambots.wrapper.types.methods import GetUpdates, SendMessage, GetMe
from telegrambots.wrapper.types.objects import (
    ForceReply,
    InlineKeyboardMarkup,
    MessageEntity,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)


class TelegramBot(TelegramBotsClient):
    def __init__(self, token: str):
        super().__init__(token)

    async def get_me(self):
        """Use this method to get information about the bot.

        Returns:
            `User`: A :class:`User` object.
        """
        return await self(GetMe())

    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
        ] = None,
    ):
        """Send text message to chat.

        Args:
            chat_id (`int`): Unique identifier for the target chat or username of the target channel
            text (`str`): Text of the message to be sent
            parse_mode (`Optional[str]`, optional): Send Markdown or HTML, if you want Telegram apps to show bold,
                italic, fixed-width text or inline URLs in your bot's message.
            entities (`Optional[list[MessageEntity]`], optional): List of special entities that appear in message text,
                which can be specified instead of parse_mode.
            disable_web_page_preview (`Optional[bool]`, optional): Disables link previews for links in this message.
            disable_notification (`Optional[bool]`, optional): Sends the message silently.
            protect_content (`Optional[bool]`, optional): If True, the message content will be protected.
            reply_to_message_id (`Optional[int]`, optional): reply to message id.
            allow_sending_without_reply (`Optional[bool]`, optional): If True, the message will be sent anyway.
            reply_markup (`Optional[ InlineKeyboardMarkup  |  ReplyKeyboardMarkup  |  ReplyKeyboardRemove  |  ForceReply ]`, optional):
                Additional interface options. An object for an inline keyboard, custom reply keyboard, ...

        Returns:
            `Message`: On success, the sent message is returned.
        """

        return await self(
            SendMessage(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    async def get_updates(
        self,
        offset: Optional[int] = None,
        limit: int = 100,
        timeout: int = 0,
        allowed_updates: Optional[list[str]] = None,
    ) -> list[Update]:
        """Use this method to receive incoming updates using long polling.

        Args:
            offset (`Optional[int]`, optional): Identifier of the first update to be returned.
                Must be greater by one than the highest among the identifiers of previously received updates.
                By default, updates starting with the earliest unconfirmed update are returned.
            limit (`Optional[int]`, optional): Limits the number of updates to be retrieved.
                Values between 1—100 are accepted. Defaults to 100.
            timeout (`Optional[int]`, optional): Timeout in seconds for long polling.
                Defaults to 0, i.e. usual short polling.
            allowed_updates (`Optional[list[str]]`, optional): List the types of updates you want your bot to receive.

        Returns:
            `list[Update]`: A list of updates.
        """
        return await self(
            GetUpdates(
                offset=offset,
                limit=limit,
                timeout=timeout,
                allowed_updates=allowed_updates,
            )
        )

    async def stream_updates(self, allowed_updates: Optional[list[str]] = None):
        """Streams updates from Telegram server.

        Args:
            allowed_updates (`Optional[list[str]]`, optional): List the types of updates you want your bot to receive.

        Yields:
            `Update`: Updates received from the server.
        """
        offset = 0

        while True:
            updates = await self.get_updates(
                offset, limit=100, timeout=300, allowed_updates=allowed_updates
            )

            for update in updates:
                yield update
                offset = update.update_id + 1
