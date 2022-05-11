from typing import Callable, Optional
from telegrambots.wrapper.types.objects import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


class InlineButtonBuilder:
    def __init__(self) -> None:
        self._buttons: list[list[InlineKeyboardButton]] = [[]]

    def append_button(
        self,
        create: Callable[[type[InlineKeyboardButton]], InlineKeyboardButton],
        row_index: Optional[int] = None,
        column_index: Optional[int] = None,
    ):
        if row_index is None:
            row_index = -1

        if column_index is None:
            self._buttons[row_index].append(create(InlineKeyboardButton))
        else:
            self._buttons[row_index].insert(column_index, create(InlineKeyboardButton))
        return self

    def append_many_buttons(
        self, *create: Callable[[type[InlineKeyboardButton]], InlineKeyboardButton]
    ):
        for c in create:
            self.append_button(c)
        return self

    def append_row(
        self,
        create: Optional[
            Callable[[type[InlineKeyboardButton]], InlineKeyboardButton]
        ] = None,
        insert_index: Optional[int] = None,
    ):
        to_append = [] if create is None else [create(InlineKeyboardButton)]

        if insert_index is None:
            self._buttons.append(to_append)
        else:
            self._buttons.insert(insert_index, to_append)
        return self

    def build(self):
        return InlineKeyboardMarkup(self._buttons)
