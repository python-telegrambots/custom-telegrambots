from typing import Callable, Optional
from telegrambots.wrapper.types.objects import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


class InlineButtonBuilder:
    """An helper class to simplify the creation of InlineKeyboardMarkup"""

    def __init__(
        self,
        create: Optional[
            Callable[[type[InlineKeyboardButton]], InlineKeyboardButton]
        ] = None,
    ) -> None:
        """Create a new InlineButtonBuilder

        An helper class to simplify the creation of InlineKeyboardMarkup

        Args:
            create: A function that creates a new InlineKeyboardButton.
        """
        self._buttons: list[list[InlineKeyboardButton]] = [[]]
        if create is not None:
            self.append_button(create)

    def __call__(self):
        """Return the InlineKeyboardMarkup from builder."""
        return self.build()

    def append_button(
        self,
        create: Callable[[type[InlineKeyboardButton]], InlineKeyboardButton],
        row_index: Optional[int] = None,
        column_index: Optional[int] = None,
    ):
        """Append a button to the builder.

        Args:
            create: A function that creates a new InlineKeyboardButton.
            row_index: The row index of the button.
            column_index: The column index of the button.
        """
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
        """Append many buttons to the builder.

        Args:
            *create: A list of functions that creates a new InlineKeyboardButton.
        """
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
        """Append a row to the builder.

        Args:
            create: A function that creates a new InlineKeyboardButton.
            insert_index: The index of the row.
        """
        to_append = [] if create is None else [create(InlineKeyboardButton)]

        if insert_index is None:
            self._buttons.append(to_append)
        else:
            self._buttons.insert(insert_index, to_append)
        return self

    def build(self):
        """Return the InlineKeyboardMarkup from builder."""
        return InlineKeyboardMarkup(self._buttons)
