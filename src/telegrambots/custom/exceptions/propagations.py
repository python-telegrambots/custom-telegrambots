class BreakPropagation(Exception):
    """
    This exception is used to break the execution of a handling loop.
    """

    pass


class ContinuePropagation(Exception):
    """
    This exception is used to continue the execution of a handling loop ( Skip this one ).
    """

    pass
