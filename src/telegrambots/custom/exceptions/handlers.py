from typing import Any


class HandlerRegistered(Exception):
    def __init__(self, tag: str, update_type: type[Any]) -> None:
        super().__init__(
            f"Handler with tag {tag} is already registered for update type {update_type}."
        )
