from abc import ABC, abstractmethod
import dataclasses
from typing import Any, Generic, Mapping, TypeVar

from telegrambots.wrapper.types.objects.update import Update, TUpdate

TKey = TypeVar("TKey")


class Exctractable(Generic[TUpdate], ABC):
    @abstractmethod
    def __extractor__(self, update: Update[TUpdate]) -> TUpdate:
        ...


class Checkable(Generic[TUpdate], ABC):
    @abstractmethod
    def __check__(self, update: TUpdate) -> bool:
        ...


@dataclasses.dataclass(init=True, frozen=True, slots=True)
class ContainedResult:
    result: bool
    metadata: Mapping[str, Any]


def extract(exctractable: Exctractable[TUpdate], update: Update[TUpdate]) -> TUpdate:
    if not isinstance(exctractable, Exctractable):  # type: ignore
        raise TypeError("exctractable must be Exctractable")
    return exctractable.__extractor__(update)


def check(checkable: Checkable[TUpdate], update: TUpdate) -> bool:
    if not isinstance(checkable, Checkable):  # type: ignore
        raise TypeError("checkable must be Checkable")
    return checkable.__check__(update)


def general_extractor(update: Update[TUpdate]) -> TUpdate:
    return update.actual_update
