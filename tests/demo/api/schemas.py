"""Module tests.demo.api.schemas."""

from ninja import Schema
from ninja.constants import NOT_SET

from ninja_extended.fields import IntField, IntFieldValues, StringField, StringFieldValues


class ResourceFieldValues:
    id = IntFieldValues(description="The id of the resource.")
    value_unique = StringFieldValues(description="The value_unique of the resource", min_length=3)
    value_unique_together_1 = StringFieldValues(description="The value_unique_together_1 of the resource")
    value_unique_together_2 = StringFieldValues(description="The value_unique_together_2 of the resource")
    value_not_null = StringFieldValues(description="The value_not_null of the resource")
    value_check = IntFieldValues(description="The value_check of the resource")


class ResourceCreateRequest(Schema):
    value_unique: str = StringField(field_values=ResourceFieldValues.value_unique)
    value_unique_together_1: str = StringField(field_values=ResourceFieldValues.value_unique_together_1)
    value_unique_together_2: str = StringField(field_values=ResourceFieldValues.value_unique_together_2)
    value_not_null: str | None = StringField(field_values=ResourceFieldValues.value_not_null)
    value_check: int | None = IntField(field_values=ResourceFieldValues.value_check)


class ResourceUpdateRequest(Schema):
    value_unique: str = StringField(field_values=ResourceFieldValues.value_unique, default=None)
    value_unique_together_1: str = StringField(field_values=ResourceFieldValues.value_unique_together_1, default=None)
    value_unique_together_2: str = StringField(field_values=ResourceFieldValues.value_unique_together_2, default=None)
    value_not_null: str | None = StringField(field_values=ResourceFieldValues.value_not_null, default=None)
    value_check: int | None = IntField(field_values=ResourceFieldValues.value_check, default=None)


class ResourceResponse(Schema):
    id: int = IntField(field_values=ResourceFieldValues.id)
    value_unique: str = StringField(field_values=ResourceFieldValues.value_unique)
    value_unique_together_1: str = StringField(field_values=ResourceFieldValues.value_unique_together_1)
    value_unique_together_2: str = StringField(field_values=ResourceFieldValues.value_unique_together_2)
    value_not_null: str | None = StringField(field_values=ResourceFieldValues.value_not_null)
    value_check: int | None = IntField(field_values=ResourceFieldValues.value_check)
