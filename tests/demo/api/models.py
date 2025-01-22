"""Module tests.demo.api.model."""

from typing import ClassVar

from django.db import IntegrityError
from django.db.models import (
    PROTECT,
    AutoField,
    CharField,
    CheckConstraint,
    ForeignKey,
    IntegerField,
    Manager,
    Model,
    ProtectedError,
    Q,
    QuerySet,
)
from django.db.transaction import atomic
from api.errors import (
    ResourceCheckConstraintError,
    ResourceMultipleObjectsReturnedError,
    ResourceNotFoundError,
    ResourceNotNullConstraintError,
    ResourceProtectedError,
    ResourceUniqueConstraintError,
)
from ninja.constants import NOT_SET, NOT_SET_TYPE

from ninja_extended.errors import handle_integrity_error, handle_protected_error


class ResourceQuerySet(QuerySet["Resource"]):
    """Resource QuerySet."""


class ResourceManager(Manager["Resource"]):
    """Resource Manager."""

    def get_queryset(self) -> QuerySet:
        """Get Resource QuerySet."""

        return ResourceQuerySet(model=self.model, using=self._db)

    def list_resources(self) -> QuerySet["Resource"]:
        """List all resources."""
        return self.get_queryset().all()

    def get_resource_by_id(self, id: int) -> "Resource":  # noqa: A002
        """Get a Resource by id."""

        try:
            return self.get_queryset().get(id=id)
        except self.model.DoesNotExist as error:
            raise ResourceNotFoundError(fields={"id": id}) from error
        except self.model.MultipleObjectsReturned as error:
            raise ResourceMultipleObjectsReturnedError(fields={"id": id}) from error

    def create_resource(
        self,
        value_unique: str,
        value_unique_together_1: str,
        value_unique_together_2: str,
        value_not_null: str,
        value_check: int,
    ) -> "Resource":
        """Create a Resource."""

        data = {
            "value_unique": value_unique,
            "value_unique_together_1": value_unique_together_1,
            "value_unique_together_2": value_unique_together_2,
            "value_not_null": value_not_null,
            "value_check": value_check,
        }

        with atomic():
            try:
                resource = self.model(**data)
                resource.save()

                return resource
            except IntegrityError as error:
                handle_integrity_error(
                    error=error,
                    unique_constraint_error_type=ResourceUniqueConstraintError,
                    not_null_constraint_error_type=ResourceNotNullConstraintError,
                    check_constraint_error_type=ResourceCheckConstraintError,
                    data=data,
                )

    def update_resource_by_id(
        self,
        id: int | NOT_SET_TYPE = NOT_SET,
        value_unique: str | NOT_SET_TYPE = NOT_SET,
        value_unique_together_1: str | NOT_SET_TYPE = NOT_SET,
        value_unique_together_2: str | NOT_SET_TYPE = NOT_SET,
        value_not_null: str | NOT_SET_TYPE = NOT_SET,
        value_check: int | NOT_SET_TYPE = NOT_SET,
    ) -> "Resource":
        """Update a Resource by id."""

        data = {
            "value_unique": value_unique,
            "value_unique_together_1": value_unique_together_1,
            "value_unique_together_2": value_unique_together_2,
            "value_not_null": value_not_null,
            "value_check": value_check,
        }
        dirty = False

        with atomic():
            try:
                resource = self.get_queryset().get(id=id)

                for key, value in data.items():
                    if value != NOT_SET:
                        setattr(resource, key, value)
                        dirty = True

                if dirty:
                    resource.save()

                return resource
            except self.model.DoesNotExist as error:
                raise ResourceNotFoundError(fields={"id": id}) from error
            except self.model.MultipleObjectsReturned as error:
                raise ResourceMultipleObjectsReturnedError(fields={"id": id}) from error
            except IntegrityError as error:
                handle_integrity_error(
                    error=error,
                    unique_constraint_error_type=ResourceUniqueConstraintError,
                    not_null_constraint_error_type=ResourceNotNullConstraintError,
                    check_constraint_error_type=ResourceCheckConstraintError,
                    data=data,
                )

    def delete_resource_by_id(self, id: int) -> None:
        """Delete a Resource by id."""

        try:
            self.get_queryset().get(id=id).delete()
        except self.model.DoesNotExist as error:
            raise ResourceNotFoundError(fields={"id": id}) from error
        except self.model.MultipleObjectsReturned as error:
            raise ResourceMultipleObjectsReturnedError(fields={"id": id}) from error
        except ProtectedError as error:
            handle_protected_error(error=error, protected_error_type=ResourceProtectedError)


class Resource(Model):
    class Meta:
        unique_together = ("value_unique_together_1", "value_unique_together_2")
        constraints = [
            CheckConstraint(name="value_check_gte_0", condition=Q(value_check__gte=0)),
        ]

    id = AutoField(primary_key=True, unique=True, editable=False)
    value_unique = CharField(max_length=32, unique=True, null=False, blank=False)
    value_unique_together_1 = CharField(max_length=32, null=False, blank=False)
    value_unique_together_2 = CharField(max_length=32, null=False, blank=False)
    value_not_null = CharField(max_length=32, null=False, blank=False)
    value_check = IntegerField(null=True)

    objects: ClassVar[ResourceManager] = ResourceManager()


class Child1(Model):
    id = AutoField(primary_key=True, unique=True, editable=False)
    resource = ForeignKey(
        Resource,
        on_delete=PROTECT,
        related_name="children_1",
        null=False,
    )


class Child2(Model):
    id = AutoField(primary_key=True, unique=True, editable=False)
    resource = ForeignKey(
        Resource,
        on_delete=PROTECT,
        related_name="children_2",
        null=False,
    )
