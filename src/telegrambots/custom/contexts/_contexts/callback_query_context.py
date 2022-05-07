from typing import Optional, final, TYPE_CHECKING

from telegrambots.wrapper.types.objects import CallbackQuery, Update

from .context_template import GenericContext

if TYPE_CHECKING:
    from ...dispatcher import Dispatcher


class CallbackQueryContext(GenericContext[CallbackQuery]):
    def __init__(
        self,
        dp: "Dispatcher",
        update: Update,
        handler_tag: str,
    ) -> None:
        super().__init__(
            dp, update=update, update_type=CallbackQuery, handler_tag=handler_tag
        )

    @final
    def __extractor__(self, update: Update) -> CallbackQuery:
        c = update.callback_query
        if c is not None:
            return c
        raise ValueError("Update has no callback query")

    async def answer(
        self,
        text: str,
        *,
        show_alert: bool = False,
        url: Optional[str] = None,
        cache_time: int = 0
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
