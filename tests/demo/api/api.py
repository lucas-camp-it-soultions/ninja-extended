"""Module tests.demo.api.api."""

from django.http import HttpRequest
from ninja.pagination import paginate

from api.models import Resource
from api.schemas import ResourceCreateRequest, ResourceResponse, ResourceUpdateRequest
from ninja_extended.api import ExtendedNinjaAPI, ExtendedRouter, response_factory
from ninja_extended.errors import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    CheckConstraintError,
    CSRFError,
    MultipleObjectsReturnedError,
    NotFoundError,
    NotNullConstraintError,
    ProtectedError,
    UniqueConstraintError,
    ValidationError,
    register_error_handler,
    register_validation_error_handler,
)
from ninja_extended.pagination import PageNumberPageSizePagination

api = ExtendedNinjaAPI(title="Test API", version="0.0.1", description="API description")
router = ExtendedRouter(tags=["resources"])

# Errors
register_error_handler(api=api, error_type=AuthenticationError)
register_error_handler(api=api, error_type=AuthorizationError)
register_error_handler(api=api, error_type=APIError)
register_error_handler(api=api, error_type=CheckConstraintError)
register_error_handler(api=api, error_type=CSRFError)
register_error_handler(api=api, error_type=MultipleObjectsReturnedError)
register_error_handler(api=api, error_type=NotFoundError)
register_error_handler(api=api, error_type=NotNullConstraintError)
register_error_handler(api=api, error_type=ProtectedError)
register_error_handler(api=api, error_type=UniqueConstraintError)
register_validation_error_handler(api=api)


@router.get(
    path="/",
    operation_id="listResources",
    summary="List all Resources",
    response=response_factory((200, list[ResourceResponse])),
)
def list_resources(request: HttpRequest):  # noqa: ARG001
    return Resource.objects.list_resources()


@router.get(
    path="/pagination",
    operation_id="listResourcesPagination",
    summary="List all Resources with pagination",
    response=response_factory((200, list[ResourceResponse])),
)
@paginate(PageNumberPageSizePagination)
def list_resources_pagination(request: HttpRequest):  # noqa: ARG001
    return Resource.objects.list_resources()


@router.get(
    path="/{id}",
    operation_id="getResourceById",
    summary="Get a Resource by id",
    response=response_factory((200, ResourceResponse), NotFoundError, MultipleObjectsReturnedError, ValidationError),
)
def get_resource_by_id(request: HttpRequest, id: int):  # noqa: ARG001, A002
    return Resource.objects.get_resource_by_id(id=id)


@router.post(
    path="/",
    operation_id="createResource",
    summary="Create a Resource",
    response=response_factory(
        (201, ResourceResponse), CheckConstraintError, NotNullConstraintError, UniqueConstraintError, ValidationError
    ),
)
def create_resource(request: HttpRequest, data: ResourceCreateRequest):  # noqa: ARG001
    return 201, Resource.objects.create_resource(**data.model_dump())


@router.patch(
    path="/{id}",
    operation_id="updateResourceById",
    summary="Update a Resource",
    response=response_factory(
        (200, ResourceResponse),
        NotFoundError,
        MultipleObjectsReturnedError,
        CheckConstraintError,
        NotNullConstraintError,
        UniqueConstraintError,
        ValidationError,
    ),
)
def update_resource_by_id(request: HttpRequest, id: int, data: ResourceUpdateRequest):  # noqa: ARG001, A002
    return Resource.objects.update_resource_by_id(id=id, **data.model_dump(exclude_unset=True))


@router.delete(
    path="/{id}",
    operation_id="deleteResourceById",
    summary="Delete a resource by id",
    response=response_factory(
        (204, None), NotFoundError, MultipleObjectsReturnedError, ProtectedError, ValidationError
    ),
)
def delete_resource_by_id(request: HttpRequest, id: int):  # noqa: ARG001, A002
    return 204, Resource.objects.delete_resource_by_id(id=id)


api.add_router("resources", router)
