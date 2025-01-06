from django.db import IntegrityError
from django.db.transaction import atomic
from django.http import HttpRequest
from ninja import Schema
from ninja.errors import ValidationError as NinjaValidationError
from ninja.pagination import paginate

from ninja_extended.api import ExtendedNinjaAPI, ExtendedRouter
from ninja_extended.errors import (
    NotNullConstraintError,
    UniqueConstraintError,
    ValidationError,
    register_exception_handler,
)
from ninja_extended.errors.integrity import handle_integrity_error
from ninja_extended.errors.validation import discriminate_validation_errors, validation_error_factory
from ninja_extended.fields import IntField, IntFieldValues, StringField, StringFieldValues
from ninja_extended.pagination import PageNumberPageSizePagination

from .models import Resource

api = ExtendedNinjaAPI(title="Test API", version="0.0.1", description="API description")
router = ExtendedRouter()


class ResourceFieldValues:
    id = IntFieldValues(description="The id of the resource.")
    value_unique = StringFieldValues(description="The value_unique of the resource", min_length=3)
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


register_exception_handler(api=api, error_type=ResourceUniqueConstraintError)
register_exception_handler(api=api, error_type=ResourceNotNullConstraintError)


@api.exception_handler(NinjaValidationError)
def validation_errors(request, exc):
    class TestValidationError(ValidationError):
        operation_id = request.operation_id

    if request.path.startswith("/"):
        router_prefix = request.path.split("/")[1]
    else:
        router_prefix = request.path.split("/")[0]
    if router_prefix == "":
        router_prefix = None

    DerivedValidationError = type(
        "DerivedValidationError",
        (ValidationError,),
        {
            "router_prefix": router_prefix,
            "operation_id": request.operation_id,
        },
    )

    errors = exc.errors

    error = DerivedValidationError(errors=errors)

    return api.create_response(
        request=request,
        data=error.schema()(**error.to_dict(), path=request.path, operation_id=request.operation_id),
        status=ValidationError.status,
    )


@router.get(
    path="/",
    operation_id="list-resources",
    summary="List all resources",
    description="List all resources",
    tags=["resources"],
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
    description="List all resources with pagination",
    tags=["resources"],
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
    description="Create a resource",
    tags=["resources"],
    response={
        201: ResourceResponse,
        422: discriminate_validation_errors(
            [
                ResourceNotNullConstraintError,
                ResourceUniqueConstraintError,
                validation_error_factory("resources", "create-resource"),
            ]
        ),
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
                data=data,
            )


api.add_router("resources", router)
