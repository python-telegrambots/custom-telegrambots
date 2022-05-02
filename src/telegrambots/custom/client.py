from typing import Optional, cast

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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
        """
        await self(
            DeleteMessage(
                chat_id=chat_id,
                message_id=message_id,
            )
        )

    # generate method for DeleteWebhook
    async def delete_webhook(self, drop_pending_updates: Optional[bool] = None):
        """Use this method to remove webhook integration if you decide to switch back to getUpdates.

        Returns:
            `bool`: True on success.
        """
        await self(DeleteWebhook(drop_pending_updates))

    # generate method for DeleteMyCommands
    async def delete_my_commands(
        self,
        scope: Optional[BotCommandScope] = None,
        language_code: Optional[str] = None,
    ):
        """Use this method to delete your own commands.

        Returns:
            `bool`: True on success.
        """
        await self(DeleteMyCommands(scope, language_code))

    # generate method for DeleteStickerFromSet
    async def delete_sticker_from_set(self, sticker: str):
        """Use this method to delete a sticker from a set created by the bot.

        Returns:
            `bool`: True on success.
        """
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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

        Returns:
            `bool`: True on success.
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
