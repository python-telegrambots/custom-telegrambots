from typing import Any, Optional, cast, Union

from telegrambots.wrapper.client import TelegramBotsClient
from telegrambots.wrapper.types.methods import (
    GetUpdates,
    SendMessage,
    GetMe,
    AddStickerToSet,
    AnswerCallbackQuery,
    AnswerInlineQuery,
    AnswerPreCheckoutQuery,
    AnswerShippingQuery,
    AnswerWebAppQuery,
    ApproveChatJoinRequest,
    BanChatMember,
    BanChatSenderChat,
    GetChatMenuButton,
    DeclineChatJoinRequest,
    DeleteChatPhoto,
    DeleteChatStickerSet,
    DeleteMessage,
    DeleteWebhook,
    DeleteMyCommands,
    DeleteStickerFromSet,
    EditMessageCaption,
    EditMessageLiveLocation,
    EditMessageMedia,
    EditMessageReplyMarkup,
    EditMessageText,
    EditChatInviteLink,
    ForwardMessage,
    GetChat,
    GetChatAdministrators,
    GetChatMember,
    GetChatMemberCount,
    GetFile,
    GetGameHighScores,
    GetMyCommands,
    GetWebhookInfo,
    GetStickerSet,
    GetMyDefaultAdministratorRights,
    GetUserProfilePhotos,
    LeaveChat,
    LogOut,
    PinChatMessage,
    PromoteChatMember,
    RestrictChatMember,
    RevokeChatInviteLink,
    SendChatAction,
    SendMediaGroup,
    SendSticker,
    SendVideo,
    SetChatDescription,
    SetChatPhoto,
    SetChatStickerSet,
    SetChatTitle,
    SetMyCommands,
    SetMyDefaultAdministratorRights,
    SetGameScore,
    StopMessageLiveLocation,
    SendAnimation,
    SendAudio,
    SendDocument,
    SendGame,
    SendInvoice,
    SendLocation,
    # SendDice,
    # SendVideoNote,
    # SendVoice,
    # SetChatPermissions,
    # SendContact,
    # SendVenue,
    # SendPhoto,
    # SendPoll,
)
from telegrambots.wrapper.types.objects import (
    ForceReply,
    InlineKeyboardMarkup,
    MessageEntity,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    MaskPosition,
    InlineQueryResult,
    ShippingOption,
    MenuButton,
    BotCommandScope,
    InputMedia,
    Message,
    GameHighScore,
    UserProfilePhotos,
    BotCommand,
    InputFile,
    ChatPermissions,
    ChatAdministratorRights,
    LabeledPrice,
    # InputMediaAnimation,
    # InputMediaAudio,
    # InputMediaDocument,
    # InputMediaPhoto,
    # InputMediaVideo,
)
from .dispatcher import Dispatcher


class TelegramBot(TelegramBotsClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._dispatcher: Optional[Dispatcher] = None

    @property
    def dispatcher(self) -> Dispatcher:
        """Returns the dispatcher instance."""
        if self._dispatcher is None:
            self._dispatcher = Dispatcher(self)
        return self._dispatcher

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
    ) -> list[Update[Any]]:
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
                offset, limit=100, timeout=290, allowed_updates=allowed_updates
            )

            for update in updates:
                yield update
                offset = update.update_id + 1

    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        png_sticker: str,
        emojis: str,
        mask_position: Optional[MaskPosition] = None,
    ):
        """Use this method to add a new sticker to a set created by the bot.

        Args:
            user_id (`int`): User identifier of sticker set owner.
            name (`str`): Sticker set name.
            png_sticker (`str`): Png image with the sticker, must be up to 512 kilobytes in size,
                dimensions must not exceed 512px, and either width or height must be exactly 512px.
            emojis (`str`): One or more emoji corresponding to the sticker.
            mask_position (`Optional[MaskPosition]`, optional): Position where the mask should be placed on
                the sticker.

        """
        return await self(
            AddStickerToSet(
                user_id=user_id,
                name=name,
                png_sticker=png_sticker,
                emojis=emojis,
                mask_position=mask_position,
            )
        )

    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: list[InlineQueryResult],
        cache_time: int = 300,
        is_personal: bool = False,
        next_offset: Optional[str] = None,
        switch_pm_text: Optional[str] = None,
        switch_pm_parameter: Optional[str] = None,
    ):
        """Use this method to send answers to an inline query.

        No more than 50 results per query are allowed.

        Args:
            inline_query_id (`str`): Unique identifier for the answered query.
            results (`list[InlineQueryResult]`): A list of results for the inline query.
            cache_time (`int`, optional): The maximum amount of time in seconds that the
                result of the inline query may be cached on the server. Defaults to 300.
            is_personal (`Optional[bool]`, optional): Pass True, if results may be cached on
                the server side only for the user that sent the query.
            next_offset (`Optional[str]`, optional): Pass the offset that a client should send in
                the next query with the same text to receive more results.
            switch_pm_text (`Optional[str]`, optional): If passed, clients will display a button with specified text
                that switches the user to a private chat with the bot and sends the bot a start message
                with the parameter switch_pm_parameter.
            switch_pm_parameter (`Optional[str]`, optional): Deep-linking parameter for the /start message
                sent to the bot when user presses the switch button. 1-64 characters,
                only A-Z, a-z, 0-9, _ and - are allowed.

        """
        return await self(
            AnswerInlineQuery(
                inline_query_id=inline_query_id,
                results=results,
                cache_time=cache_time,
                is_personal=is_personal,
                next_offset=next_offset,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter=switch_pm_parameter,
            )
        )

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: bool = False,
        url: Optional[str] = None,
        cache_time: int = 0,
    ):
        """Use this method to send answers to callback queries sent from inline keyboards.

        Args:
            callback_query_id (`str`): Unique identifier for the query to be answered.
            text (`Optional[str]`, optional): Text of the notification. If not specified, nothing will be shown on the screen.
            show_alert (`Optional[bool]`, optional): If true, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
            url (`Optional[str]`, optional): URL that will be opened by the user's client.
            cache_time (`Optional[int]`, optional): The maximum amount of time in seconds that the result of the callback query may be cached client-side.

        """
        await self(
            AnswerCallbackQuery(
                callback_query_id=callback_query_id,
                text=text,
                show_alert=show_alert,
                url=url,
                cache_time=cache_time,
            )
        )

    async def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        shipping_options: Optional[list[ShippingOption]] = None,
        error_message: Optional[str] = None,
    ):
        """Use this method to send answers to pre-checkout queries.

        Args:
            shipping_query_id (`str`): Unique identifier for the query to be answered.
            ok (`bool`): Specify True if delivery to the specified address is possible and False if there are any problems (for example, if delivery to the specified address is not possible).
            shipping_options (`Optional[list[ShippingOption]]`, optional): Required if ok is True. A JSON-serialized array of available shipping options.
            error_message (`Optional[str]`, optional): Required if ok is False. Error message in human readable form that explains why it is impossible to complete the order (e.g. "Sorry, delivery to your desired address is unavailable'). Telegram will display this message to the user.

        """
        return await self(
            AnswerShippingQuery(
                shipping_query_id=shipping_query_id,
                ok=ok,
                shipping_options=shipping_options,
                error_message=error_message,
            )
        )

    async def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        error_message: Optional[str] = None,
    ):
        """Use this method to send answers to pre-checkout queries.

        Args:
            pre_checkout_query_id (`str`): Unique identifier for the query to be answered.
            ok (`bool`): Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.
            error_message (`Optional[str]`, optional): Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.

        """
        return await self(
            AnswerPreCheckoutQuery(
                pre_checkout_query_id=pre_checkout_query_id,
                ok=ok,
                error_message=error_message,
            )
        )

    async def answer_web_app_query(
        self, web_app_query_id: str, inline_query_result: InlineQueryResult
    ):
        """Use this method to send answers to Telegram's reverse queries.

        Args:
            data (`str`): Reverse query identifier.
            ok (`bool`): Specify True if the query is answered successfully.
            error_message (`Optional[str]`, optional): Required if ok is False. Error message in human readable form that explains the reason for failure to perform the query.
        """
        await self(
            AnswerWebAppQuery(
                web_app_query_id=web_app_query_id,
                result=inline_query_result,
            )
        )

    async def approve_chat_join_request(self, chat_id: int | str, user_id: int):
        """Use this method to approve a chat join request.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).
            invite_link (`Optional[str]`, optional): Required if a chat_id and a message_id are both specified. Identifier of the sent message.
            timeout (`int`, optional): Timeout in seconds for long polling. Defaults to 30.
        """
        return await self(
            ApproveChatJoinRequest(
                chat_id=chat_id,
                user_id=user_id,
            )
        )

    async def ban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        until_date: Optional[int] = None,
        revoke_messages: Optional[bool] = None,
    ):
        """Use this method to kick a user from a group or a supergroup.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).
            user_id (`int`): Unique identifier of the target user.
            until_date (`Optional[int]`, optional): Date when the user will be unbanned, unix time. If user is banned for more than 366 days or less than 30 seconds from the current time they are considered to be banned forever.
            revoke_messages (`Optional[str]`, optional): Optional. A JSON-serialized object for a new BotCommand.
        """
        await self(
            BanChatMember(
                chat_id=chat_id,
                user_id=user_id,
                until_date=until_date,
                revoke_messages=revoke_messages,
            )
        )

    # generate method for BanChatSenderChat
    async def ban_chat_sender_chat(self, chat_id: int | str, sender_chat_id: int):
        """Use this method to kick a user from a group or a supergroup.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).
            sender_chat_id (`int`): Unique identifier of the target user.

        """
        await self(
            BanChatSenderChat(
                chat_id=chat_id,
                sender_chat_id=sender_chat_id,
            )
        )

    # generate method for GetChatMenuButton
    async def get_chat_menu_button(self, chat_id: Optional[None]) -> MenuButton:
        """Use this method to get the current chat menu button.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).

        """
        return await self(
            GetChatMenuButton(
                chat_id=chat_id,
            )
        )

    # generate method for DeclineChatJoinRequest
    async def decline_chat_join_request(self, chat_id: int | str, user_id: int):
        """Use this method to approve a chat join request.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).
            user_id (`int`): Unique identifier of the target user.
        """
        await self(
            DeclineChatJoinRequest(
                chat_id=chat_id,
                user_id=user_id,
            )
        )

    # generate method for DeleteChatPhoto
    async def delete_chat_photo(self, chat_id: int | str):
        """Use this method to delete a chat photo.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).

        """
        await self(
            DeleteChatPhoto(
                chat_id=chat_id,
            )
        )

    # generate method for DeleteChatStickerSet
    async def delete_chat_sticker_set(self, chat_id: int | str):
        """Use this method to delete a group sticker set from a supergroup.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).
        """
        await self(
            DeleteChatStickerSet(
                chat_id=chat_id,
            )
        )

    # generate method for DeleteMessage
    async def delete_message(self, chat_id: int | str, message_id: int):
        """Use this method to delete a message.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).
            message_id (`int`): Identifier of the message to delete.
        """
        await self(
            DeleteMessage(
                chat_id=chat_id,
                message_id=message_id,
            )
        )

    # generate method for DeleteWebhook
    async def delete_webhook(self, drop_pending_updates: Optional[bool] = None):
        """Use this method to remove webhook integration if you decide to switch back to getUpdates."""
        await self(DeleteWebhook(drop_pending_updates))

    # generate method for DeleteMyCommands
    async def delete_my_commands(
        self,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
    ):
        """Use this method to delete your own commands."""
        await self(DeleteMyCommands(scope, language_code))

    # generate method for DeleteStickerFromSet
    async def delete_sticker_from_set(self, sticker: str):
        """Use this method to delete a sticker from a set created by the bot."""
        await self(DeleteStickerFromSet(sticker))

    # generate method for EditMessageCaption
    async def edit_message_caption(
        self,
        chat_id: int | str,
        message_id: int,
        caption: Optional[str] = None,
        caption_entities: Optional[list[MessageEntity]] = None,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit captions of messages sent by the bot or via the bot (for inline bots).

        Args:
            chat_id (`int` | `str`): Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            message_id (`int`): Required if inline_message_id is not specified. Identifier of the message to edit.
            caption (`Optional[str]`, optional): New caption of the message.
            caption_entities (`Optional[list[MessageEntity]]`, optional): A JSON-serialized object for an array of special entities that appear in the caption.
            parse_mode (`Optional[str]`, optional): Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for an inline keyboard.

        Returns:
            `Message`: on success.
        """
        return cast(
            Message,
            await self(
                EditMessageCaption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=caption,
                    caption_entities=caption_entities,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                )
            ),
        )

    # generate method for EditMessageCaption with inline_message_id
    async def edit_inline_message_caption(
        self,
        inline_message_id: str,
        caption: Optional[str] = None,
        caption_entities: Optional[list[MessageEntity]] = None,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit captions of messages sent by the bot or via the bot (for inline bots).

        Args:
            inline_message_id (`str`): Required. Identifier of the inline message.
            caption (`Optional[str]`, optional): New caption of the message.
            caption_entities (`Optional[list[MessageEntity]]`, optional): A JSON-serialized object for an array of special entities that appear in the caption.
            parse_mode (`Optional[str]`, optional): Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for an inline keyboard.
        """
        await self(
            EditMessageCaption(
                inline_message_id=inline_message_id,
                caption=caption,
                caption_entities=caption_entities,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
        )

    # generate method for EditMessageReplyMarkup
    async def edit_message_reply_markup(
        self,
        chat_id: int | str,
        message_id: int,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit only the reply markup of messages sent by the bot or via the bot (for inline bots).

        Args:
            chat_id (`int` | `str`): Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            message_id (`int`): Required if inline_message_id is not specified. Identifier of the message to edit.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for an inline keyboard.

        Returns:
            `Message`: on success.
        """
        return cast(
            Message,
            await self(
                EditMessageReplyMarkup(
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=reply_markup,
                )
            ),
        )

    # generate method for EditMessageReplyMarkup with inline_message_id
    async def edit_inline_message_reply_markup(
        self,
        inline_message_id: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit only the reply markup of messages sent by the bot or via the bot (for inline bots).

        Args:
            inline_message_id (`str`): Required. Identifier of the inline message.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for an inline keyboard.
        """
        await self(
            EditMessageReplyMarkup(
                inline_message_id=inline_message_id,
                reply_markup=reply_markup,
            )
        )

    # generate method for EditMessageText
    async def edit_message_text(
        self,
        chat_id: int | str,
        message_id: int,
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit text and game messages sent by the bot or via the bot (for inline bots).

        Args:
            chat_id (`int` | `str`): Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            message_id (`int`): Required if inline_message_id is not specified. Identifier of the message to edit.
            text (`str`): New text of the message.
            parse_mode (`Optional[str]`, optional): Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.
            entities (`Optional[list[MessageEntity]]`, optional): A JSON-serialized object for an array of special entities that appear in the message text.
            disable_web_page_preview (`Optional[bool]`, optional): Disables link previews for links in this message.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for an inline keyboard.

        Returns:
            `Message`: on success.
        """
        return cast(
            Message,
            await self(
                EditMessageText(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=text,
                    parse_mode=parse_mode,
                    entities=entities,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup,
                )
            ),
        )

    # generate method for EditMessageText with inline_message_id
    async def edit_inline_message_text(
        self,
        inline_message_id: str,
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit text and game messages sent by the bot or via the bot (for inline bots).

        Args:
            inline_message_id (`str`): Required. Identifier of the inline message.
            text (`str`): New text of the message.
            parse_mode (`Optional[str]`, optional): Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.
            entities (`Optional[list[MessageEntity]]`, optional): A JSON-serialized object for an array of special entities that appear in the message text.
            disable_web_page_preview (`Optional[bool]`, optional): Disables link previews for links in this message.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for an inline keyboard.

        """
        await self(
            EditMessageText(
                inline_message_id=inline_message_id,
                text=text,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
            )
        )

    # generate method for EditMessageLiveLocation
    async def edit_message_live_location(
        self,
        chat_id: int | str,
        message_id: int,
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit live location messages sent by the bot or via the bot (for inline bots).

        Args:
            chat_id (`int` | `str`): Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            message_id (`int`): Required if inline_message_id is not specified. Identifier of the message to edit.
            latitude (`float`): Latitude of new location.
            longitude (`float`): Longitude of new location.
            horizontal_accuracy (`Optional[float]`, optional): The radius of uncertainty for the location, measured in meters; 0-1500.
            heading (`Optional[int]`, optional): The direction in which user is moving, in degrees; 1-360.
            proximity_alert_radius (`Optional[int]`, optional): The maximum distance for proximity alerts about approaching another chat member, in meters.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for an inline keyboard.

        Returns:
            `Message`: on success.
        """
        return cast(
            Message,
            await self(
                EditMessageLiveLocation(
                    chat_id=chat_id,
                    message_id=message_id,
                    latitude=latitude,
                    longitude=longitude,
                    horizontal_accuracy=horizontal_accuracy,
                    heading=heading,
                    proximity_alert_radius=proximity_alert_radius,
                    reply_markup=reply_markup,
                )
            ),
        )

    # generate method for EditMessageLiveLocation with inline_message_id
    async def edit_inline_message_live_location(
        self,
        inline_message_id: str,
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit live location messages sent by the bot or via the bot (for inline bots).

        Args:
            inline_message_id (`str`): Required. Identifier of the inline message.
            latitude (`float`): Latitude of new location.
            longitude (`float`): Longitude of new location.
            horizontal_accuracy (`Optional[float]`, optional): The radius of uncertainty for the location, measured in meters; 0-1500.
            heading (`Optional[int]`, optional): The direction in which user is moving, in degrees; 1-360.
            proximity_alert_radius (`Optional[int]`, optional): The maximum distance for proximity alerts about approaching another chat member, in meters.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for an inline keyboard.

        """
        await self(
            EditMessageLiveLocation(
                inline_message_id=inline_message_id,
                latitude=latitude,
                longitude=longitude,
                horizontal_accuracy=horizontal_accuracy,
                heading=heading,
                proximity_alert_radius=proximity_alert_radius,
                reply_markup=reply_markup,
            )
        )

    # generate method for EditMessageMedia
    async def edit_message_media(
        self,
        chat_id: int | str,
        message_id: int,
        media: InputMedia,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit animation, audio, document, photo, or video messages. If a message is a part of a message album, then it can be edited only to a photo or a video. Otherwise, message type can be changed arbitrarily. When inline message is edited, new file can't be uploaded. Use previously uploaded file via its file_id or specify a URL.

        Args:
            chat_id (`int` | `str`): Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            message_id (`int`): Required if inline_message_id is not specified. Identifier of the message to edit.
            media (`InputMedia`): A JSON-serialized object for a new media content of the message.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for a new inline keyboard.

        Returns:
            `Message`: on success.
        """
        return cast(
            Message,
            await self(
                EditMessageMedia(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=reply_markup,
                )
            ),
        )

    # generate method for EditMessageMedia with inline_message_id
    async def edit_inline_message_media(
        self,
        inline_message_id: str,
        media: InputMedia,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ):
        """Use this method to edit animation, audio, document, photo, or video messages. If a message is a part of a message album, then it can be edited only to a photo or a video. Otherwise, message type can be changed arbitrarily. When inline message is edited, new file can't be uploaded. Use previously uploaded file via its file_id or specify a URL.

        Args:
            inline_message_id (`str`): Required. Identifier of the inline message.
            media (`InputMedia`): A JSON-serialized object for a new media content of the message.
            reply_markup (`Optional[InlineKeyboardMarkup]`, optional): A JSON-serialized object for a new inline keyboard.
        """
        await self(
            EditMessageMedia(
                inline_message_id=inline_message_id,
                media=media,
                reply_markup=reply_markup,
            )
        )

    # generate method for EditChatInviteLink
    async def edit_chat_invite_link(
        self,
        chat_id: int | str,
        invite_link: str,
        name: Optional[str] = None,
        expire_date: Optional[int] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None,
    ):
        """Use this method to edit the text of an inline text or game message sent via bot (for bot-user pairs).

        Args:
            chat_id (`int` | `str`): Required. Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            invite_link (`str`): New text of the message.
            name (`Optional[str]`, optional): New chat title, for channels and group chats.
            expire_date (`Optional[int]`, optional): New chat description, for groups, supergroups and channels.
            member_limit (`Optional[int]`, optional): New chat invite link, for supergroups and channels.
            creates_join_request (`Optional[bool]`, optional): Pass True, if the chat should be a public supergroup or channel, not bound to any chat list.

        Returns:
            `ChatInviteLink`: on success.
        """
        return await self(
            EditChatInviteLink(
                chat_id=chat_id,
                invite_link=invite_link,
                name=name,
                expire_date=expire_date,
                member_limit=member_limit,
                creates_join_request=creates_join_request,
            )
        )

    # generate method for ForwardMessage
    async def forward_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
    ):
        """Use this method to forward messages of any kind. On success, the sent Message is returned.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            from_chat_id (`int` | `str`): Unique identifier for the chat where the original message was sent (or channel username in the format @channelusername).
            message_id (`int`): Message identifier in the chat specified in from_chat_id.
            disable_notification (`Optional[bool]`, optional): Sends the message silently. Users will receive a notification with no sound.
            protect_content (`Optional[bool]`, optional): Pass True, if the content of the message needs to be protected from deletion, such as for a screenshot or a file.

        Returns:
            `Message`: On success, the sent Message is returned.
        """
        return await self(
            ForwardMessage(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
                disable_notification=disable_notification,
                protect_content=protect_content,
            )
        )

    # generate method for GetChat
    async def get_chat(self, chat_id: int | str):
        """Use this method to get up to date information about the chat (current name of the user for one-on-one conversations, current username of a user, group or channel, etc.).

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).

        Returns:
            `Chat`: On success, the chat object is returned.
        """
        return await self(GetChat(chat_id=chat_id))

    # generate method for GetChatAdministrators
    async def get_chat_administrators(self, chat_id: int | str):
        """Use this method to get a list of administrators in a chat. On success, returns an Array of ChatMember objects that contains information about all chat administrators except other bots. If the chat is a group or a supergroup and no administrators were appointed, only the creator will be returned.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).

        Returns:
            `ChatMembers`: On success, returns an Array of ChatMember objects that contains information about all chat administrators except other bots.
        """
        return await self(GetChatAdministrators(chat_id=chat_id))

    # generate method for GetChatMembersCount
    async def get_chat_member_count(self, chat_id: int | str):
        """Use this method to get the number of members in a chat.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).

        Returns:
            `int`: On success, returns the number of members in the chat.
        """
        return await self(GetChatMemberCount(chat_id=chat_id))

    # generate method for GetChatMember
    async def get_chat_member(self, chat_id: int | str, user_id: int):
        """Use this method to get information about a member of a chat.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            user_id (`int`): Unique identifier of the target user.

        Returns:
            `ChatMember`: On success, returns a ChatMember object.
        """
        return await self(GetChatMember(chat_id=chat_id, user_id=user_id))

    # generate method for GetFile
    async def get_file(self, file_id: str):
        """Use this method to get basic info about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size.

        Args:
            file_id (`str`): File identifier to get info about.

        Returns:
            `File`: On success, a File object is returned.
        """
        return await self(GetFile(file_id=file_id))

    # generate method for GetGameHighScores
    async def get_game_high_scores(
        self,
        user_id: int,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
    ) -> list[GameHighScore]:
        """Use this method to get data for high score tables. Will return the score of the specified user and several of his neighbors in a game. On success, returns an Array of GameHighScore objects.

        Args:
            user_id (`int`): Target user id.
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            message_id (`int`): Identifier of the sent message.
            inline_message_id (`Optional[str]`, optional): Identifier of the inline message.

        Returns:
            `GameHighScores`: On success, returns an Array of GameHighScore objects.
        """
        return await self(
            GetGameHighScores(
                user_id=user_id,
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
            )
        )

    # generate method for GetMyCommands
    async def get_my_commands(
        self,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
    ):
        """Use this method to get the current list of the bot's commands. Requires no parameters. Returns Array of BotCommand objects.

        Args:
            scope (`Optional[BotCommandScope]`, optional): Scope of the commands to be returned.
            language_code (`Optional[str]`, optional): IETF language tag of the returned localized command descriptions.

        Returns:
            `BotCommands`: On success, returns an Array of BotCommand objects.
        """
        return await self(GetMyCommands(scope, language_code))

    # generate method for GetWebhookInfo
    async def get_webhook_info(self):
        """Use this method to get current webhook status. Requires no parameters. On success, returns a WebhookInfo object. If the bot is using getUpdates, will return an object with the url field empty.

        Returns:
            `WebhookInfo`: On success, returns a WebhookInfo object.
        """
        return await self(GetWebhookInfo())

    # generate method for GetStickerSet
    async def get_sticker_set(self, name: str):
        """Use this method to get a sticker set. On success, a StickerSet object is returned.

        Args:
            name (`str`): Short name of the sticker set that is used in t.me/addstickers/ URLs (e.g., animals).

        Returns:
            `StickerSet`: On success, a StickerSet object is returned.
        """
        return await self(GetStickerSet(name=name))

    # generate method for GetMyDefaultAdministratorRights
    async def get_my_default_administrator_rights(self):
        """Use this method to get information about the current default chat administrator.

        Returns:
            `ChatPermissions`: On success, returns a ChatPermissions object.
        """
        return await self(GetMyDefaultAdministratorRights())

    # generate method for GetUserProfilePhotos
    async def get_user_profile_photos(
        self, user_id: int, offset: Optional[int] = None, limit: int = 5
    ) -> UserProfilePhotos:
        """Use this method to get a user's profile pictures. Returns a UserProfilePhotos object.

        Args:
            user_id (`int`): Unique identifier of the target user.
            offset (`int`, optional): Sequential number of the first photo to be returned. By default, all photos are returned.
            limit (`int`, optional): Limits the number of photos to be retrieved. Values between 1—100 are accepted. Defaults to 100.

        Returns:
            `UserProfilePhotos`: On success, returns a UserProfilePhotos object.
        """
        return await self(
            GetUserProfilePhotos(user_id=user_id, offset=offset, limit=limit)
        )

    # generate method for LeaveChat
    async def leave_chat(self, chat_id: int | str):
        """Use this method for your bot to leave a group, supergroup or channel.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup or channel (in the format @channelusername).
        """
        await self(LeaveChat(chat_id=chat_id))

    # generate method for LogOut
    async def log_out(self):
        """Use this method to log out from the telegram servers."""
        await self(LogOut())

    # generate method for PinChatMessage
    async def pin_chat_message(
        self,
        chat_id: int | str,
        message_id: int,
        disable_notification: Optional[bool] = None,
    ):
        """Use this method to pin a message in a supergroup. The bot must be an administrator in the chat for this to work and must have the ‘can_pin_messages’ admin right in the supergroup or ‘can_edit_messages’ admin right in the channel. Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).
            message_id (`int`): Identifier of a message to pin.
            disable_notification (`bool`, optional): Pass True, if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels.

        Returns:
            `bool`: On success, True is returned.
        """
        return await self(
            PinChatMessage(
                chat_id=chat_id,
                message_id=message_id,
                disable_notification=disable_notification,
            )
        )

    # generate method for PromoteChatMember
    async def promote_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        is_anonymous: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_manage_video_chats: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
    ):
        """Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Pass False for all boolean parameters to demote a user. Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            user_id (`int`): Unique identifier of the target user.
            is_anonymous (`bool`, optional): Pass True, if the administrator's presence in the chat is hidden.
            can_manage_chat (`bool`, optional): Pass True, if the administrator can change chat title, photo and other settings.
            can_change_info (`bool`, optional): Pass True, if the administrator can change chat title, photo and other settings.
            can_manage_video_chats (`bool`, optional): Pass True, if the administrator can create and delete video notes.
            can_post_messages (`bool`, optional): Pass True, if the administrator can create channel posts, channels only.
            can_edit_messages (`bool`, optional): Pass True, if the administrator can edit messages of other users, channels only.
            can_delete_messages (`bool`, optional): Pass True, if the administrator can delete messages of other users.
            can_invite_users (`bool`, optional): Pass True, if the administrator can invite new users to the chat.
            can_restrict_members (`bool`, optional): Pass True, if the administrator can restrict, ban or unban chat members.
            can_pin_messages (`bool`, optional): Pass True, if the administrator can pin messages, supergroups only.
            can_promote_members (`bool`, optional): Pass True, if the administrator can add new administrators with a subset of his own privileges or demote administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed by him).
        """
        return await self(
            PromoteChatMember(
                chat_id=chat_id,
                user_id=user_id,
                is_anonymous=is_anonymous,
                can_manage_chat=can_manage_chat,
                can_change_info=can_change_info,
                can_post_messages=can_post_messages,
                can_edit_messages=can_edit_messages,
                can_manage_video_chats=can_manage_video_chats,
                can_delete_messages=can_delete_messages,
                can_invite_users=can_invite_users,
                can_restrict_members=can_restrict_members,
                can_pin_messages=can_pin_messages,
                can_promote_members=can_promote_members,
            )
        )

    # generate method for RestrictChatMember
    async def restrict_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        permissions: ChatPermissions,
        until_date: Optional[int] = None,
    ):
        """Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate admin rights. Pass True for all boolean parameters to lift restrictions from a user. Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername).
            user_id (`int`): Unique identifier of the target user.
            permissions (`ChatPermissions`): New user permissions.
            until_date (`int`, optional): Date when restrictions will be lifted for the user, unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever.
        """
        return await self(
            RestrictChatMember(
                chat_id=chat_id,
                user_id=user_id,
                permissions=permissions,
                until_date=until_date,
            )
        )

    # generate method for RevokeChatInviteLink
    async def revoke_chat_invite_link(self, chat_id: int | str, invite_link: str):
        """Use this method to revoke a link from a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        """
        return await self(
            RevokeChatInviteLink(chat_id=chat_id, invite_link=invite_link)
        )

    # generate method for SendChatAction
    async def send_chat_action(self, chat_id: int | str, action: str):
        """Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            action (`ChatAction`): Type of action to broadcast.
        """
        return await self(SendChatAction(chat_id=chat_id, action=action))

    # generate method for SendMediaGroup
    async def send_media_group(
        self,
        chat_id: int | str,
        media: list[InputMedia],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
    ) -> list[Message]:
        """Use this method to send a group of photos or videos as an album. On success, an array of the sent Messages is returned.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            media (`list`): A JSON-serialized array describing photos and videos to be sent, must include 2–10 items.
            disable_notification (`bool`, optional): Sends the messages silently. Users will receive a notification with no sound.
            protect_content (`bool`, optional): If True, content of the messages will be protected against deletion.
            reply_to_message_id (`int`, optional): If the messages are a reply, ID of the original message.
            allow_sending_without_reply (`bool`, optional): Pass True, if the message should be sent even if the specified replied-to message is not found
        """
        return await self(
            SendMediaGroup(
                chat_id=chat_id,
                media=media,  # type: ignore
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
            )
        )

    # generate method for SendSticker
    async def send_sticker(
        self,
        chat_id: int | str,
        sticker: InputFile,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
    ):
        """Use this method to send static .WEBP or animated .TGS stickers. On success, the sent Message is returned.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            sticker (`InputFile`): Sticker to send.
            disable_notification (`bool`, optional): Sends the message silently. Users will receive a notification with no sound.
            protect_content (`bool`, optional): If True, content of the messages will be protected against deletion.
            reply_to_message_id (`int`, optional): If the message is a reply, ID of the original message.
            reply_markup (`InlineKeyboardMarkup` | `ReplyKeyboardMarkup` | `ReplyKeyboardRemove` | `ForceReply`, optional): Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
            allow_sending_without_reply (`bool`, optional): Pass True, if the message should be sent even if the specified replied-to message is not found
        """
        return await self(
            SendSticker(
                chat_id=chat_id,
                sticker=sticker,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    # generate method for SendVideo
    async def send_video(
        self,
        chat_id: int | str,
        video: InputFile,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        caption: Optional[str] = None,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
    ):
        """Use this method to send video files, Telegram clients support mp4 videos (other formats may be sent as Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            video (`InputFile`): Video to send.
            duration (`int`, optional): Duration of sent video in seconds.
            width (`int`, optional): Video width.
            height (`int`, optional): Video height.
            caption (`str`, optional): Video caption (may also be used when resending videos by file_id), 0-200 characters.
            caption_entities (`list`, optional): List of special entities that appear in the caption, which can be specified instead of using parse_mode.
            disable_notification (`bool`, optional): Sends the message silently. Users will receive a notification with no sound.
            protect_content (`bool`, optional): If True, content of the messages will be protected against deletion.
            reply_to_message_id (`int`, optional): If the message is a reply, ID of the original message.
            allow_sending_without_reply (`bool`, optional): Pass True, if the message should be sent even if the specified replied-to message is not found
            reply_markup (`InlineKeyboardMarkup` | `ReplyKeyboardMarkup` | `ReplyKeyboardRemove` | `ForceReply`, optional): Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        """
        return await self(
            SendVideo(
                chat_id=chat_id,
                video=video,
                duration=duration,
                width=width,
                height=height,
                caption=caption,
                caption_entities=caption_entities,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    # generate method for SetChatDescription
    async def set_chat_description(self, chat_id: int | str, description: str):
        """Use this method to change the description of a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            description (`str`): New chat description, 0-255 characters.
        """
        return await self(SetChatDescription(chat_id=chat_id, description=description))

    # generate method for SetChatPhoto
    async def set_chat_photo(self, chat_id: int | str, photo: InputFile):
        """Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            photo (`InputFile`): New chat photo, uploaded using multipart/form-data.
        """
        return await self(SetChatPhoto(chat_id=chat_id, photo=photo))

    # generate method for SetChatStickerSet
    async def set_chat_sticker_set(self, chat_id: int | str, sticker_set_name: str):
        """Use this method to change the sticker set of a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            sticker_set_name (`str`): New value of the chat sticker set.
        """
        return await self(
            SetChatStickerSet(chat_id=chat_id, sticker_set_name=sticker_set_name)
        )

    # generate method for SetChatTitle
    async def set_chat_title(self, chat_id: int | str, title: str):
        """Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns True on success.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            title (`str`): New chat title, 1-255 characters.
        """
        return await self(SetChatTitle(chat_id=chat_id, title=title))

    # generate method for SetMyCommands
    async def set_my_commands(self, commands: list[BotCommand]):
        """Use this method to change the list of the bot's commands. Returns True on success.

        Args:
            commands (`List[BotCommand]`): New list of bot commands.
        """
        return await self(SetMyCommands(commands=commands))

    # generate method for SetMyDefaultAdministratorRights
    async def set_my_default_administrator_rights(
        self,
        rights: Optional[ChatAdministratorRights] = None,
        for_channels: Optional[bool] = None,
    ):
        """Use this method to set default custom title for all administrators. Returns True on success.

        Args:
            rights (`ChatAdministratorRights`, optional): New default chat administrator privileges.
            for_channels (`bool`, optional): Pass True, if the administrator can change chat title, photo and other settings.
        """
        return await self(
            SetMyDefaultAdministratorRights(
                rights=rights,
                for_channels=for_channels,
            )
        )

    # generate method for SetGameScore
    async def set_game_score(
        self,
        chat_id: int,
        message_id: int,
        user_id: int,
        score: int,
        force: Optional[bool] = None,
        disable_edit_message: Optional[bool] = None,
    ):
        """Use this method to set the score of the specified user in a game. On success, if the message was sent by the bot, returns the edited Message, otherwise returns True. Returns an error, if the new score is not greater than the user's current score in the chat and force is False.

        Args:
            user_id (`int`): User identifier.
            score (`int`): New score, must be non-negative.
            force (`bool`, optional): Pass True, if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters.
            disable_edit_message (`bool`, optional): Pass True, if the game message should not be automatically edited to include the current scoreboard.
            chat_id (`int`, optional): Required if inline_message_id is not specified. Unique identifier for the target chat.
            message_id (`int`, optional): Required if inline_message_id is not specified. Identifier of the sent message.
        """
        return await self(
            SetGameScore(
                user_id=user_id,
                score=score,
                force=force,
                disable_edit_message=disable_edit_message,
                chat_id=chat_id,
                message_id=message_id,
            )
        )

    async def set_inline_game_score(
        self,
        inline_message_id: str,
        user_id: int,
        score: int,
        force: Optional[bool] = None,
        disable_edit_message: Optional[bool] = None,
    ):
        """Use this method to set the score of the specified user in a game. On success, if the message was sent by the bot, returns the edited Message, otherwise returns True. Returns an error, if the new score is not greater than the user's current score in the chat and force is False.

        Args:
            user_id (`int`): User identifier.
            score (`int`): New score, must be non-negative.
            force (`bool`, optional): Pass True, if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters.
            disable_edit_message (`bool`, optional): Pass True, if the game message should not be automatically edited to include the current scoreboard.
            inline_message_id (`str`, optional): Required if chat_id and message_id are not specified. Identifier of the inline message.
        """
        return await self(
            SetGameScore(
                user_id=user_id,
                score=score,
                force=force,
                disable_edit_message=disable_edit_message,
                inline_message_id=inline_message_id,
            )
        )

    # generate method for StopMessageLiveLocation
    async def stop_message_live_location(
        self,
        chat_id: int | str,
        message_id: int,
    ):
        """Use this method to stop updating a live location message before live_period expires. On success, if the message was sent by the bot, returns the edited Message, otherwise returns True.

        Args:
            chat_id (`int` | `str`): Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            message_id (`int`): Required if inline_message_id is not specified. Identifier of the sent message.
        """
        return await self(
            StopMessageLiveLocation(
                chat_id=chat_id,
                message_id=message_id,
            )
        )

    async def stop_inline_message_live_location(
        self,
        inline_message_id: str,
    ):
        """Use this method to stop updating a live location message before live_period expires. On success, if the message was sent by the bot, returns the edited Message, otherwise returns True.

        Args:
            inline_message_id (`str`): Required if chat_id and message_id are not specified. Identifier of the inline message.
        """
        return await self(
            StopMessageLiveLocation(
                inline_message_id=inline_message_id,
            )
        )

    # generate method for SendAnimation
    async def send_animation(
        self,
        chat_id: Union[int, str],
        animation: Union[InputFile, str],
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        caption: Optional[str] = None,
        caption_entities: Optional[list[MessageEntity]] = None,
        parse_mode: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
    ):
        """Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            animation (`InputFile` | `str`): Animation to send. Pass a file_id as String to send an animation that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an animation from the Internet, or upload a new animation using multipart/form-data. More info on Sending Files ».
            duration (`int`, optional): Duration of sent animation in seconds.
            width (`int`, optional): Animation width.
            height (`int`, optional): Animation height.
            caption (`str`, optional): Animation caption (may also be used when resending animation by file_id).
            caption_entities (`list[MessageEntity]`, optional): List of special entities that appear in the caption, which can be specified instead of parse_mode.
            parse_mode (`str`, optional): Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
            disable_notification (`bool`, optional): Sends the message silently. Users will receive a notification with no sound.
            protect_content (`bool`, optional): If True, the content of the message cannot be edited.
            reply_to_message_id (`int`, optional): If the message is a reply, ID of
            allow_sending_without_reply (`bool`, optional): If set to True,
            the original message.
            reply_markup (`InlineKeyboardMarkup` | `ReplyKeyboardMarkup` | `ReplyKeyboardRemove` | `ForceReply`, optional): Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        """
        return await self(
            SendAnimation(
                chat_id=chat_id,
                animation=animation,
                duration=duration,
                width=width,
                height=height,
                caption=caption,
                caption_entities=caption_entities,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    # generate method for SendAudio
    async def send_audio(
        self,
        chat_id: Union[int, str],
        audio: Union[InputFile, str],
        caption: Optional[str] = None,
        caption_entities: Optional[list[MessageEntity]] = None,
        parse_mode: Optional[str] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Optional[Union[InputFile, str]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
    ):
        """Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .ogg file encoded with OPUS (other formats may be sent as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            audio (`InputFile` | `str`): Audio file to send. Pass a file_id as String to send an audio file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an audio file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files ».
            caption (`str`, optional): Audio caption, 0-200 characters.
            caption_entities (`list[MessageEntity]`, optional): List of special entities that appear in the caption, which can be specified instead of parse_mode.
            parse_mode (`str`, optional): Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
            duration (`int`, optional): Duration of the audio in seconds.
            performer (`str`, optional): Performer.
            title (`str`, optional): Track name.
            thumb (`InputFile` | `str`, optional ): Thumbnail of the file sent. The thumbnail should be in JPEG format and less than 200 KB in size. A thumbnail‘s width and height should not exceed 90. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can’t be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files ».
            disable_notification (`bool`, optional): Sends the message silently. Users will receive a notification with no sound.
            protect_content (`bool`, optional): If True, the content of the message will be protected against deletion.
            reply_to_message_id (`int`, optional): If the message is a reply, ID of the original message.
            allow_sending_without_reply (`bool`, optional): If the message is a reply, ID of the original message.
            reply_markup (`InlineKeyboardMarkup` | `ReplyKeyboardMarkup` | `ReplyKeyboardRemove` | `ForceReply`, optional): Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        """
        return await self(
            SendAudio(
                chat_id=chat_id,
                audio=audio,
                caption=caption,
                caption_entities=caption_entities,
                parse_mode=parse_mode,
                duration=duration,
                performer=performer,
                title=title,
                thumb=thumb,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    # generate method for SendDocument
    async def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[InputFile, str],
        thumb: Optional[Union[InputFile, str]] = None,
        caption: Optional[str] = None,
        caption_entities: Optional[list[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        parse_mode: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ] = None,
    ):
        """Use this method to send general files. On success, the sent Message is returned. Bots can currently send files of any type of up to 50 MB in size.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            document (`InputFile` | `str`): File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More info on Sending Files ».
            thumb (`InputFile` | `str`, optional): Thumbnail of the file sent. The thumbnail should be in JPEG format and less than 200 KB in size. A thumbnail‘s width and height should not exceed 90. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can’t be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files ».
            caption (`str`, optional): Document caption (may also be used when resending documents by file_id), 0-200 characters.
            caption_entities (`list[MessageEntity]`, optional): List of special entities that appear in the caption, which can be specified instead of parse_mode.
            disable_content_type_detection (`bool`, optional): Disables automatic server-side content type detection for files uploaded using multipart/form-data.
            parse_mode (`str`, optional): Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
            disable_notification (`bool`, optional): Sends the message silently. Users will receive a notification with no sound.
            protect_content (`bool`, optional): If True, the content of the message will be protected against deletion.
            reply_to_message_id (`int`, optional): If the message is a reply, ID of the original message.
            allow_sending_without_reply (`bool`, optional): If the message is a reply, ID of the original message.
            reply_markup (`InlineKeyboardMarkup` | `ReplyKeyboardMarkup` | `ReplyKeyboardRemove` | `ForceReply`, optional): Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        """
        return await self(
            SendDocument(
                chat_id=chat_id,
                document=document,
                thumb=thumb,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                disable_notification=disable_notification,
                disable_content_type_detection=disable_content_type_detection,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    # generate method for SendGame
    async def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        inline_keyboard_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:
        """Use this method to send a game. On success, the sent Message is returned.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            game_short_name (`str`): Short name of the game, serves as the unique identifier for the game. Set up your games via Botfather.
            disable_notification (`bool`, optional): Sends the message silently. Users will receive a notification with no sound.
            protect_content (`bool`, optional): If True, the content of the message will be protected against deletion.
            reply_to_message_id (`int`, optional): If the message is a reply, ID of the original message.
            allow_sending_without_reply (`bool`, optional): If the message is a reply, ID of the original message.
            reply_markup (`InlineKeyboardMarkup` | `ReplyKeyboardMarkup` | `ReplyKeyboardRemove` | `ForceReply`, optional): Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        """

        return await self(
            SendGame(
                chat_id=chat_id,
                game_short_name=game_short_name,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=inline_keyboard_markup,
            )
        )

    # generate method for SendInvoice
    async def send_invoice(
        self,
        chat_id: Union[int, str],
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        currency: str,
        prices: list[LabeledPrice],
        start_parameter: str,
        max_tip_amount: int = 0,
        suggested_tip_amounts: Optional[list[int]] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:

        """Use this method to send invoices. On success, the sent Message is returned.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            title (`str`): Product name, 1-32 characters.
            description (`str`): Product description, 1-255 characters.
            payload (`str`): Bot-defined invoice payload, 1-128 characters. This will be sent to the payments provider along with the invoice.
            provider_token (`str`): Payments provider token, obtained via Botfather.
            start_parameter (`str`): Unique deep-linking parameter that can be used to generate this invoice when used as a start parameter.
            currency (`str`): Three-letter ISO 4217 currency code.
            prices (`list`): List of objects with price information.
            provider_data (`str`, optional): JSON-encoded data about the invoice, which will be shared with the payment provider.
            photo_url (`str`, optional): URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
            photo_size (`int`, optional): Photo size.
            photo_width (`int`, optional): Photo width.
            photo_height (`int`, optional): Photo height.
            need_name (`bool`, optional): Pass True, if you require the user's full name to complete the order.
            need_phone_number (`bool`, optional): Pass True, if you require the user's phone number to complete the order.
            need_email (`bool`, optional): Pass True, if you require the user's email address to complete the order.
            need_shipping_address (`bool`, optional): Pass True, if you require the user's shipping address to complete the order.
            send_phone_number_to_provider (`bool`, optional): Pass True, if user's phone number should be sent to provider.
            send_email_to_provider (`bool`, optional): Pass True, if user's email address should be sent to provider.
            is_flexible (`bool`, optional): Pass True, if the final price depends on the shipping method.
            disable_notification (`bool`, optional): Sends the message silently. Users will receive a notification with no sound.
            reply_to_message_id (`int`, optional): If the message is a reply, ID of the original message.
            allow_sending_without_reply (`bool`, optional): If the message is a reply, ID of the original message.
            reply_markup (`InlineKeyboardMarkup`, optional): Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        """

        return await self(
            SendInvoice(
                chat_id=chat_id,
                title=title,
                description=description,
                payload=payload,
                provider_token=provider_token,
                currency=currency,
                prices=prices,
                max_tip_amount=max_tip_amount,
                suggested_tip_amounts=suggested_tip_amounts,
                start_parameter=start_parameter,
                provider_data=provider_data,
                photo_url=photo_url,
                photo_size=photo_size,
                photo_width=photo_width,
                photo_height=photo_height,
                need_name=need_name,
                need_phone_number=need_phone_number,
                need_email=need_email,
                need_shipping_address=need_shipping_address,
                send_phone_number_to_provider=send_phone_number_to_provider,
                send_email_to_provider=send_email_to_provider,
                is_flexible=is_flexible,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    # generate method for SendLocation
    async def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> Message:

        """Use this method to send point on the map. On success, the sent Message is returned.

        Args:
            chat_id (`int` | `str`): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            latitude (`float`): Latitude of the location.
            longitude (`float`): Longitude of the location.
            horizontal_accuracy (`float`, optional): The radius of uncertainty for the location, measured in meters.
            live_period (`int`, optional): Period in seconds for which the location will be updated.
            heading (`int`, optional): For live locations, a direction in which the user is moving (heading).
            disable_notification (`bool`, optional): Sends the message silently. Users will receive a notification
            proximity_alert_radius (`int`, optional): For live locations, a distance to the location
            reply_to_message_id (`int`, optional): If the message is a reply, ID of the original message.
            allow_sending_without_reply (`bool`, optional): If the message is a reply, ID of the original message.
            reply_markup (`InlineKeyboardMarkup`, optional): Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        """
        return await self(
            SendLocation(
                chat_id=chat_id,
                latitude=latitude,
                longitude=longitude,
                horizontal_accuracy=horizontal_accuracy,
                live_period=live_period,
                heading=heading,
                proximity_alert_radius=proximity_alert_radius,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
            )
        )

    # generate method for SendMediaGroup
    # generate method for SendDice
    # generate method for SendVideoNote
    # generate method for SendVoice
    # generate method for SetChatPermissions
    # generate method for SendContact
    # generate method for SendVenue
    # generate method for SendPhoto
    # generate method for SendPoll
