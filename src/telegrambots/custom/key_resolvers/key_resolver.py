from abc import ABC, abstractmethod
from typing import Callable, Generic

from telegrambots.wrapper.types.objects import Update

from ..general import Exctractable, TKey, TUpdate


class AbstractKeyResolver(Generic[TUpdate, TKey], Exctractable[TUpdate], ABC):
    def __init__(self, key: TKey):
        self._key = key

    def is_key(self, update: Update):
        return self.resolver(self.__extractor__(update)) == self.key

    @property
    def key(self) -> TKey:
        return self._key

    @property
    def resolver(self):
        return self._resolve

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
        super().__init__(key)
        self.__resolver = resolver
        self.__extractor = _extractor

    def _resolve(self, update: TUpdate) -> TKey:
        return self.__resolver(update)

    def __extractor__(self, update: Update) -> TUpdate:
        return self.__extractor(update)
