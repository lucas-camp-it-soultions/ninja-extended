# Generated by Django 5.1.4 on 2025-01-21 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_childmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="Child1",
            fields=[
                ("id", models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="children_1", to="api.resource"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Child2",
            fields=[
                ("id", models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="children_2", to="api.resource"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="ChildModel",
        ),
    ]
