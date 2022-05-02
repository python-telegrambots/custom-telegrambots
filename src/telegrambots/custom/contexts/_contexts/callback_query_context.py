from typing import Optional, final

from telegrambots.wrapper.types.objects import CallbackQuery, Update

from ...client import TelegramBot
from .context_template import GenericContext


class CallbackQueryContext(GenericContext[CallbackQuery]):
    def __init__(self, bot: TelegramBot, update: Update) -> None:
        super().__init__(bot, update)

    @final
    def __extractor__(self, update: Update) -> Optional[CallbackQuery]:
        return update.callback_query
