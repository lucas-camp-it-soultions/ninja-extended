from django.db.models import AutoField, CharField, CheckConstraint, IntegerField, Model, Q


class Resource(Model):
    class Meta:
        unique_together = ("value_unique_together_1", "value_unique_together_2")
        constraints = [
            CheckConstraint(name="value_check_gte_0", condition=Q(value_check__gte=0)),
        ]

    id = AutoField(primary_key=True, unique=True, editable=False)
    value_unique = CharField(max_length=32, unique=True)
    value_unique_together_1 = CharField(max_length=32)
    value_unique_together_2 = CharField(max_length=32)
    value_not_null = CharField(max_length=32, null=False, blank=False)
    value_check = IntegerField(null=True)
