from typing import Any, Optional, final, TYPE_CHECKING

from telegrambots.wrapper.types.objects import (
    CallbackQuery,
    Update,
    MessageEntity,
    InlineKeyboardMarkup,
)

from .context_template import Context

if TYPE_CHECKING:
    from ...dispatcher import Dispatcher


class CallbackQueryContext(Context[CallbackQuery]):
    def __init__(
        self,
        dp: "Dispatcher",
        update: Update[CallbackQuery],
        handler_tag: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(dp, update, CallbackQuery, handler_tag, *args, **kwargs)

    @final
    @property
    def data(self) -> Optional[str]:
        """Returns the data of the callback query."""
        return self.update.data

    @final
    @property
    def message(self):
        """The message of callback query."""
        return self.update.message

    @final
    @property
    def from_user(self):
        """The sender of callback query."""
        return self.update.from_user

    async def answer(
        self,
        text: str,
        *,
        show_alert: bool = False,
        url: Optional[str] = None,
        cache_time: int = 0,
    ) -> None:
        """Answers a callback query.

        Args:
            text (`str`): The text to show in the answer.
            show_alert (`bool`, optional): If true, an alert will be shown by the client. Defaults to False.
            url (`str`, optional): If specified, clients will open this url instead of the default url.
            cache_time (`int`, optional): The time in seconds that the result of the callback query will be available. Defaults to 0.
        """

        await self.bot.answer_callback_query(
            callback_query_id=self.update.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )

    async def edit_text(
        self,
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: bool = False,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Edits the text of a message.

        Args:
            text (`str`): The new text of the message.
            parse_mode (`str`, optional): The parse mode to use for the text. Defaults to None.
            entities (`list[MessageEntity]`, optional): A list of additional entities to send with the message. Defaults to None.
            disable_web_page_preview (`bool`, optional): Disables link previews for links in this message. Defaults to False.
            reply_markup (`InlineKeyboardMarkup`, optional): Additional interface options. Defaults to None.
        """

        if self.update.message is not None:
            return await self.bot.edit_message_text(
                chat_id=self.update.message.chat.id,
                message_id=self.update.message.message_id,
                text=text,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
            )
        else:
            raise ValueError(
                "CallbackQuery contains no message. you may use edit_inline_text instead"
            )

    async def edit_inline_text(
        self,
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: bool = False,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Edits the text of an inline message.

        Args:
            text (`str`): The new text of the message.
            parse_mode (`str`, optional): The parse mode to use for the text. Defaults to None.
            entities (`list[MessageEntity]`, optional): A list of additional entities to send with the message. Defaults to None.
            disable_web_page_preview (`bool`, optional): Disables link previews for links in this message. Defaults to False.
            reply_markup (`InlineKeyboardMarkup`, optional): Additional
        """

        if self.update.inline_message_id is not None:
            return await self.bot.edit_inline_message_text(
                inline_message_id=self.update.inline_message_id,
                text=text,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
            )
        else:
            raise ValueError(
                "CallbackQuery contains no inline message id. you may use edit_text instead"
            )

    async def edit_reply_markup(
        self, reply_markup: Optional[InlineKeyboardMarkup] = None
    ):
        """Edits the reply markup of a message.

        Args:
            reply_markup (`InlineKeyboardMarkup`, optional): The new reply markup of the message. Defaults to None.
        """
        if self.update.message is not None:
            return await self.bot.edit_message_reply_markup(
                chat_id=self.update.message.chat.id,
                message_id=self.update.message.message_id,
                reply_markup=reply_markup,
            )
        else:
            raise ValueError(
                "CallbackQuery contains no message. you may use edit_inline_reply_markup instead"
            )

    async def edit_inline_reply_markup(
        self, reply_markup: Optional[InlineKeyboardMarkup] = None
    ):
        """Edits the reply markup of an inline message.

        Args:
            reply_markup (`InlineKeyboardMarkup`, optional): The new reply markup of the message. Defaults to None.
        """
        if self.update.inline_message_id is not None:
            return await self.bot.edit_inline_message_reply_markup(
                inline_message_id=self.update.inline_message_id,
                reply_markup=reply_markup,
            )
        else:
            raise ValueError(
                "CallbackQuery contains no inline message id. you may use edit_reply_markup instead"
            )
