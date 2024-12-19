from decimal import Decimal

import pytest

from ninja_extended.utils import camel_to_kebap, convert_value_to_detail_string, pluralize, snake_to_camel


@pytest.mark.parametrize(
    ("camel_string", "kebap_string"),
    [
        ("foobar", "foobar"),
        ("Foobar", "foobar"),
        ("fooBar", "foo-bar"),
        ("FooBar", "foo-bar"),
        ("FooBarBaz", "foo-bar-baz"),
    ],
)
def test_camel_to_kebap(camel_string: str, kebap_string: str):
    assert camel_to_kebap(value=camel_string) == kebap_string


@pytest.mark.parametrize(
    ("snake_string", "camel_string"),
    [
        ("foobar", "foobar"),
        ("foo_bar", "fooBar"),
        ("foo_bar_baz", "fooBarBaz"),
    ],
)
def test_snake_to_camel(snake_string: str, camel_string: str):
    assert snake_to_camel(value=snake_string) == camel_string


@pytest.mark.parametrize(
    ("value", "output"),
    [
        (True, "true"),
        (False, "false"),
        (Decimal("42.21"), "42.21"),
        (42, "42"),
        (42.21, "42.21"),
        ("foo", "'foo'"),
    ],
)
def test_convert_value_to_detail_string(value: bool, output: str):  # noqa: FBT001
    assert convert_value_to_detail_string(value=value) == output


@pytest.mark.parametrize(
    ("singular", "plural"),
    [
        ("couch", "couches"),
        ("fish", "fishes"),
        ("fox", "foxes"),
        ("cross", "crosses"),
        ("quartz", "quartzes"),
        ("hero", "heroes"),
        ("country", "countries"),
        ("leef", "leeves"),
        ("life", "lives"),
        ("apple", "apples"),
    ],
)
def test_pluralize(singular: str, plural: str):
    assert pluralize(value=singular) == plural
