from pydantic_core import PydanticUndefined

from ninja_extended.fields.base import BaseField, BaseFieldValues


def test_field_values_default_values():
    field_values = BaseFieldValues(description="Description")

    assert field_values.description == "Description"
    assert field_values.strict is True


def test_field_default(mocker):
    field_values = BaseFieldValues(description="Description")

    field_mock = mocker.patch("ninja_extended.fields.base.Field")

    BaseField(field_values=field_values)

    field_mock.assert_called_once_with(description="Description", strict=True, default=PydanticUndefined)


def test_field(mocker):
    field_values = BaseFieldValues(description="Description")

    field_mock = mocker.patch("ninja_extended.fields.base.Field")

    BaseField(field_values=field_values, default="foobar")

    field_mock.assert_called_once_with(description="Description", strict=True, default="foobar")
