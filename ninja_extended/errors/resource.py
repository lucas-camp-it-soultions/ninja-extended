"""Module error.resource."""

from ninja_extended.errors.check_constraint import check_constraint_error_factory
from ninja_extended.errors.multiple_objects_returned import multiple_objects_returned_error_factory
from ninja_extended.errors.not_found import not_found_error_factory
from ninja_extended.errors.not_null_constraint import not_null_constraint_error_factory
from ninja_extended.errors.protected import protected_error_factory
from ninja_extended.errors.unique_constraint import unique_constraint_error_factory


class ResourceErrors:
    """Resource errors."""

    def __init__(self, resource: str):
        """Initialize a ResourceErrors class."""

        self.CheckConstraint = check_constraint_error_factory(resource_=resource)
        self.MultipleObjectsReturned = multiple_objects_returned_error_factory(resource_=resource)
        self.NotFound = not_found_error_factory(resource_=resource)
        self.NozNullConstraint = not_null_constraint_error_factory(resource_=resource)
        self.Protected = protected_error_factory(resource_=resource)
        self.UniqueConstraint = unique_constraint_error_factory(resource_=resource)
