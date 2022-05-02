from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from telegrambots.wrapper.types.objects import Update

TUpdate = TypeVar("TUpdate")


class Exctractable(Generic[TUpdate], ABC):
    @abstractmethod
    def __extractor__(self, update: Update) -> Optional[TUpdate]:
        ...


class Checkable(Generic[TUpdate], ABC):
    @abstractmethod
    def __check__(self, update: Optional[TUpdate]) -> bool:
        ...


def extract(exctractable: Exctractable[TUpdate], update: Update) -> Optional[TUpdate]:
    if not isinstance(exctractable, Exctractable):  # type: ignore
        raise TypeError("exctractable must be Exctractable")
    return exctractable.__extractor__(update)


def check(checkable: Checkable[TUpdate], update: Optional[TUpdate]) -> bool:
    if not isinstance(checkable, Checkable):  # type: ignore
        raise TypeError("checkable must be Checkable")
    return checkable.__check__(update)
