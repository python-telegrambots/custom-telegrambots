from abc import ABC, abstractmethod
from typing import Callable, Generic, Optional, final

from ...general import Checkable, TUpdate


class Filter(Generic[TUpdate], Checkable[TUpdate], ABC):
    @final
    def check(self, update: Optional[TUpdate]) -> bool:
        if update is None:
            return False
        return self.__check__(update)

    @final
    def __and__(self, other: "Filter[TUpdate]"):
        if not isinstance(other, Filter):  # type: ignore
            raise TypeError("other must be Filter")
        return AndFilter(self, other)

    @final
    def __or__(self, other: "Filter[TUpdate]"):
        if not isinstance(other, Filter):  # type: ignore
            raise TypeError("other must be Filter")
        return OrFilter(self, other)

    @final
    def __invert__(self):
        return ReverseFilter(self)

    @final
    def __xor__(self, other: "Filter[TUpdate]"):
        if not isinstance(other, Filter):  # type: ignore
            raise TypeError("other must be Filter")
        return XorFilter(self, other)


class SealedFilter(Filter[TUpdate]):
    def __init__(self, filter: Callable[[TUpdate], bool]):
        self._filter = filter

    @final
    def __check__(self, update: Optional[TUpdate]) -> bool:
        if update is None:
            return False
        return self._filter(update)


class JoinedFilter(Filter[TUpdate], ABC):
    def __init__(self, *_filters: Filter[TUpdate]) -> None:
        self._filters = _filters

    @abstractmethod
    def __wrapping__(self, update: TUpdate) -> bool:
        ...

    @final
    def __check__(self, update: Optional[TUpdate]) -> bool:
        if update is None:
            return False
        return self.__wrapping__(update)


class AndFilter(JoinedFilter[TUpdate]):
    def __init__(self, *_filters: Filter[TUpdate]) -> None:
        super().__init__(*_filters)

    @final
    def __wrapping__(self, update: TUpdate) -> bool:
        for filter in self._filters:
            if not filter.check(update):
                return False
        return True


class ReverseFilter(JoinedFilter[TUpdate]):
    def __init__(self, *_filters: Filter[TUpdate]) -> None:
        super().__init__(*_filters)

    @final
    def __wrapping__(self, update: TUpdate) -> bool:
        for filter in self._filters:
            if filter.check(update):
                return False
        return True


class OrFilter(JoinedFilter[TUpdate]):
    def __init__(self, *_filters: Filter[TUpdate]) -> None:
        super().__init__(*_filters)

    @final
    def __wrapping__(self, update: TUpdate) -> bool:
        for filter in self._filters:
            if filter.check(update):
                return True
        return False


class XorFilter(JoinedFilter[TUpdate]):
    def __init__(self, *_filters: Filter[TUpdate]) -> None:
        super().__init__(*_filters)

    @final
    def __wrapping__(self, update: TUpdate) -> bool:
        count = 0
        for filter in self._filters:
            if filter.check(update):
                count += 1
        return count == 1


def filter_factory(_check: Callable[[TUpdate], bool]) -> Filter[TUpdate]:
    """
    Factory function to create a filter.

    Args:
        _check (`Callable[[TUpdate], bool]`): A function that takes an item and returns a boolean.

    Returns:
        `Filter`: A filter that checks if a message passes the filter.
    """
    return SealedFilter(_check)
