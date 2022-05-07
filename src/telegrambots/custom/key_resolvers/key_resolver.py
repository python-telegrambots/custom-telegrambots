from abc import abstractmethod
from typing import Callable, Generic

from telegrambots.wrapper.types.objects import Update

from ..general import Exctractable, TKey, TUpdate


class AbstractKeyResolver(Generic[TUpdate, TKey], Exctractable[TUpdate]):
    def is_key(self, update: Update):
        return self.resolver(self.__extractor__(update)) == self.key

    @property
    def resolver(self):
        return self._resolve

    @property
    @abstractmethod
    def key(self) -> TKey:
        ...

    @abstractmethod
    def _resolve(self, update: TUpdate) -> TKey:
        ...


class KeyResolver(Generic[TUpdate, TKey], AbstractKeyResolver[TUpdate, TKey]):
    def __init__(
        self,
        _extractor: Callable[[Update], TUpdate],
        resolver: Callable[[TUpdate], TKey],
        key: TKey,
    ):
        self.__resolver = resolver
        self.__key = key
        self.__extractor = _extractor

    @property
    def key(self):
        return self.__key

    def _resolve(self, update: TUpdate) -> TKey:
        return self.__resolver(update)

    def __extractor__(self, update: Update) -> TUpdate:
        return self.__extractor(update)
