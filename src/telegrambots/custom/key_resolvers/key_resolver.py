from abc import ABC, abstractmethod
from typing import Callable, Generic, final

from telegrambots.wrapper.types.objects import Update

from ..general import Exctractable, TKey, TUpdate


class AbstractKeyResolver(Generic[TUpdate, TKey], Exctractable[TUpdate], ABC):
    def __init__(self, key: TKey):
        self._key = key

    def is_key(self, update: Update[TUpdate]):
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

    @final
    def __extractor__(self, update: Update[TUpdate]) -> TUpdate:
        return update.actual_update


class KeyResolver(Generic[TUpdate, TKey], AbstractKeyResolver[TUpdate, TKey]):
    def __init__(
        self,
        resolver: Callable[[TUpdate], TKey],
        key: TKey,
    ):
        super().__init__(key)
        self.__resolver = resolver

    def _resolve(self, update: TUpdate) -> TKey:
        return self.__resolver(update)
