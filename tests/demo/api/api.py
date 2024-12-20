from django.db import IntegrityError
from django.db.transaction import atomic
from django.http import HttpRequest
from ninja import Schema

from ninja_extended.api import ExtendedNinjaAPI, ExtendedRouter
from ninja_extended.errors import NotNullConstraintError, UniqueConstraintError
from ninja_extended.errors.integrity import IntegrityErrorParser
from ninja_extended.errors.integrity.types import IntegrityErrorType
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


class ResourceUniqueConstraintError(UniqueConstraintError):
    resource_name = "Resource"


class ResourceNotNullConstraintError(NotNullConstraintError):
    resource_name = "Resource"


@api.exception_handler(ResourceUniqueConstraintError)
def resource_unique_constraint_error_handler(request: HttpRequest, error: ResourceUniqueConstraintError):
    return api.create_response(
        request=request,
        data=ResourceUniqueConstraintError.schema()(**error.to_dict(), path=request.path, operation_id=request.operation_id),
        status=ResourceUniqueConstraintError.status,
    )


@api.exception_handler(ResourceNotNullConstraintError)
def resource_not_null_constraint_error_handler(request: HttpRequest, error: ResourceNotNullConstraintError):
    return api.create_response(
        request=request,
        data=ResourceNotNullConstraintError.schema()(**error.to_dict(), path=request.path, operation_id=request.operation_id),
        status=ResourceNotNullConstraintError.status,
    )


@router.post(
    path="/resources",
    operation_id="createResource",
    summary="Create a resource",
    description="Create a resource",
    tags=["resources"],
    response={
        201: ResourceResponse,
        422: ResourceNotNullConstraintError.schema() | ResourceUniqueConstraintError.schema(),
    },
)
def create_resource(request: HttpRequest, data: ResourceCreateRequest):  # noqa: ARG001
    with atomic():
        try:
            return 201, Resource.objects.create(**data.model_dump())
        except IntegrityError as error:
            print("INSIDE ERROR HANDLER")
            type, columns = IntegrityErrorParser().parse(error=error)

            if type == IntegrityErrorType.UNIQUE_CONSTRAINT:
                raise ResourceUniqueConstraintError({key: data.model_dump()[key] for key in columns})

            if type == IntegrityErrorType.NOT_NULL_CONSTRAINT:
                raise ResourceNotNullConstraintError({key: data.model_dump()[key] for key in columns})


api.add_router("", router)
