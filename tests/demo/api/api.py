from django.db import IntegrityError
from django.http import HttpRequest
from ninja import Schema

from ninja_extended.api import ExtendedNinjaAPI, ExtendedRouter
from ninja_extended.errors.integrity import IntegrityErrorParser
from ninja_extended.fields import IntField, IntFieldValues, StringField, StringFieldValues

from .models import Resource

api = ExtendedNinjaAPI(title="Test API", version="0.0.1", description="API description")
router = ExtendedRouter()


class ResourceFieldValues:
    id = IntFieldValues(description="The id of the resource.")
    value_unique = StringFieldValues(description="The value_unique of the resource")
    value_unique_together_1 = StringFieldValues(description="The value_unique_together_1 of the resource")
    value_unique_together_2 = StringFieldValues(description="The value_unique_together_2 of the resource")
    value_not_null = StringFieldValues(description="The value_not_null of the resource")


class ResourceCreateRequest(Schema):
    value_unique: str = StringField(field_values=ResourceFieldValues.value_unique)
    value_unique_together_1: str = StringField(field_values=ResourceFieldValues.value_unique_together_1)
    value_unique_together_2: str = StringField(field_values=ResourceFieldValues.value_unique_together_2)
    value_not_null: str | None = StringField(field_values=ResourceFieldValues.value_not_null)


class ResourceResponse(Schema):
    id: int = IntField(field_values=ResourceFieldValues.id)
    value_unique: str = StringField(field_values=ResourceFieldValues.value_unique)
    value_unique_together_1: str = StringField(field_values=ResourceFieldValues.value_unique_together_1)
    value_unique_together_2: str = StringField(field_values=ResourceFieldValues.value_unique_together_2)
    value_not_null: str | None = StringField(field_values=ResourceFieldValues.value_not_null)


@router.post(
    path="/",
    operation_id="createResource",
    summary="Create a resource",
    description="Create a resource",
    tags=["resources"],
    response=ResourceResponse,
)
def create_resource(request: HttpRequest, data: ResourceCreateRequest):  # noqa: ARG001
    return Resource.objects.create(**data.model_dump())


api.add_router("", router)
