from abc import ABC, ABCMeta
from typing import Callable, Generic, Optional, final

from telegrambots.wrapper.types.objects import Update

from ...client import TelegramBot
from ...general import Exctractable, TUpdate


class ContextTemplate(metaclass=ABCMeta):
    def __init__(self, bot: TelegramBot, update: Update):
        self.__bot = bot
        self.__update = update

    @final
    @property
    def bot(self) -> TelegramBot:
        """`TelegramBot`: Bot instance"""
        return self.__bot

    @final
    @property
    def wrapper_update(self) -> Update:
        return self.__update


class GenericContext(Generic[TUpdate], Exctractable[TUpdate], ABC, ContextTemplate):
    def __init__(self, bot: TelegramBot, update: Update) -> None:
        super().__init__(bot, update)

    @final
    @property
    def update(self) -> TUpdate:
        """`TUpdate`: Update instance"""
        inner = self.__extractor__(self.wrapper_update)
        if inner is None:
            raise ValueError(f"Cannot exctract inner update.")
        return inner


class Context(Generic[TUpdate], GenericContext[TUpdate]):
    def __init__(
        self,
        _exctractor: Callable[[Update], Optional[TUpdate]],
        bot: TelegramBot,
        update: Update,
    ) -> None:
        super().__init__(bot, update)
        self.__extractor = _exctractor

    @final
    def __extractor__(self, update: Update) -> Optional[TUpdate]:
        return self.__extractor(update)
