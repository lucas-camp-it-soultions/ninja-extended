"""Module utils."""

import re
from decimal import Decimal


def camel_to_kebap(value: str) -> str:
    """Convert a camel case string to a kebap case string.

    Args:
        value (str): The string in camel case.

    Returns:
        str: The string in kebap case.
    """
    return re.sub(pattern=r"(?<!^)(?=[A-Z])", repl="-", string=value).lower()


def snake_to_camel(value: str) -> str:
    """Convert a snake case string to a camel case string.

    Args:
        value (str): The string in snake case.

    Returns:
        str: The string in camel case.
    """
    camel_str = re.sub(pattern=r"_([a-zA-Z])", repl=lambda match: match.group(1).upper(), string=value)

    return camel_str[0].lower() + camel_str[1:] if camel_str else ""


def pluralize(value: str) -> str:
    """Pluralize a string.

    Args:
        value (str): The string in singular.

    Returns:
        str: The string in plural.
    """

    if value.endswith(("ch", "sh", "x", "s", "z", "o")):
        return f"{value}es"

    if value.endswith("y") and value[-2] not in "aeiou":
        return f"{value[:-1]}ies"

    if value.endswith("f"):
        return f"{value[:-1]}ves"

    if value.endswith("fe"):
        return f"{value[:-2]}ves"

    return f"{value}s"


def convert_value_to_detail_string(value: bool | Decimal | float | int | str) -> str:  # noqa: PYI041
    """Convert a value into a string representation.

    Args:
        value (bool | Decimal | float | int | str): The value to be converted.

    Raises:
        ValueError: If the value can not be converted.

    Returns:
        str: The string representation value.
    """

    if value is None:
        return "null"

    if value is True:
        return "true"

    if value is False:
        return "false"

    if isinstance(value, Decimal):
        return str(value)

    if isinstance(value, float):
        return str(value)

    if isinstance(value, int):
        return str(value)

    if isinstance(value, str):
        return f"'{value}'"

    raise ValueError(f"Can't convert value of type '{type(value)}' for detail string.")  # noqa: EM102
