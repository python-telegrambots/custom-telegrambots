from typing import Optional, final

from telegrambots.wrapper.types.objects import (
    Message,
    Update,
    MessageEntity,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
)

from ...client import TelegramBot
from .context_template import GenericContext


class MessageContext(GenericContext[Message]):
    def __init__(self, bot: TelegramBot, update: Update) -> None:
        super().__init__(bot, update)

    @final
    def __extractor__(self, update: Update) -> Optional[Message]:
        return update.message

    @final
    async def reply_text(
        self,
        text: str,
        send_as_reply: bool = True,
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
            send_as_reply (`bool`, optional): If True, the message will be sent as reply to current message.
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
        return await self.bot.send_message(
            chat_id=self.update.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id
            if not send_as_reply
            else self.update.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
