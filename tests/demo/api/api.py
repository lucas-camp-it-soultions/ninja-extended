from typing import Annotated

from django.db import IntegrityError
from django.db.transaction import atomic
from django.http import HttpRequest
from ninja import Schema
from ninja.errors import ValidationError as NinjaValidationError
from ninja.pagination import paginate
from pydantic import Field

from ninja_extended.api import ExtendedNinjaAPI, ExtendedRouter
from ninja_extended.errors import (
    CheckConstraintError,
    NotNullConstraintError,
    UniqueConstraintError,
    ValidationError,
    register_error_handler,
    register_validation_error_handler,
)
from ninja_extended.errors.integrity import handle_integrity_error
from ninja_extended.fields import IntField, IntFieldValues, StringField, StringFieldValues
from ninja_extended.pagination import PageNumberPageSizePagination

from .models import Resource

api = ExtendedNinjaAPI(title="Test API", version="0.0.1", description="API description")
router = ExtendedRouter(tags=["resources"])


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


class ResourceResponse(Schema):
    id: int = IntField(field_values=ResourceFieldValues.id)
    value_unique: str = StringField(field_values=ResourceFieldValues.value_unique)
    value_unique_together_1: str = StringField(field_values=ResourceFieldValues.value_unique_together_1)
    value_unique_together_2: str = StringField(field_values=ResourceFieldValues.value_unique_together_2)
    value_not_null: str | None = StringField(field_values=ResourceFieldValues.value_not_null)
    value_check: int | None = IntField(field_values=ResourceFieldValues.value_check)


class ResourceUniqueConstraintError(UniqueConstraintError):
    resource = "Resource"


class ResourceNotNullConstraintError(NotNullConstraintError):
    resource = "Resource"


class ResourceCheckConstraintError(CheckConstraintError):
    resource = "Resource"


register_validation_error_handler(api=api)
register_error_handler(api=api, error_type=ResourceUniqueConstraintError)
register_error_handler(api=api, error_type=ResourceNotNullConstraintError)
register_error_handler(api=api, error_type=ResourceCheckConstraintError)


@router.get(
    path="/",
    operation_id="list-resources",
    summary="List all resources",
    response={
        200: list[ResourceResponse],
    },
)
def create_resource(request: HttpRequest):  # noqa: ARG001
    with atomic():
        return Resource.objects.all()


@router.get(
    path="/paginated",
    operation_id="list-resources-paginated",
    summary="List all resources with pagination",
    response={
        200: list[ResourceResponse],
    },
)
@paginate(PageNumberPageSizePagination)
def create_resource(request: HttpRequest):  # noqa: ARG001
    with atomic():
        return Resource.objects.all()


@router.post(
    path="/",
    operation_id="create-resource",
    summary="Create a resource",
    response={
        201: ResourceResponse,
        422: Annotated[
            ResourceNotNullConstraintError.schema | ResourceUniqueConstraintError.schema | ValidationError.schema | CheckConstraintError.schema,
            Field(discriminator="type"),
        ],
    },
)
def create_resource(request: HttpRequest, data: ResourceCreateRequest):  # noqa: ARG001
    with atomic():
        try:
            return 201, Resource.objects.create(**data.model_dump())
        except IntegrityError as error:
            handle_integrity_error(
                error=error,
                unique_constraint_error_type=ResourceUniqueConstraintError,
                not_null_constraint_error_type=ResourceNotNullConstraintError,
                check_constraint_error_type=ResourceCheckConstraintError,
                data=data,
            )


api.add_router("resources", router)
