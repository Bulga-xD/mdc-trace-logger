def is_true(value: str) -> bool:
    """
    Converts a string value to a boolean.

    :param value: The string to convert.
    :return: Boolean representation of the value.
    """
    return value.lower() in ("true", "1", "yes", "y", "on")
