# Generated by Django 4.2.7 on 2023-11-26 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Box",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated"),
                ),
                ("title", models.CharField(max_length=50, verbose_name="Title")),
            ],
            options={
                "verbose_name": "Box for keys",
                "verbose_name_plural": "Boxes for keys",
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Street",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated"),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "prefix",
                    models.CharField(
                        choices=[
                            ("вул.", "вулиця"),
                            ("б.", "бульвар"),
                            ("пр.", "проспект"),
                            ("пров.", "провулок"),
                        ],
                        default="вул.",
                        max_length=6,
                        verbose_name="Prefix",
                    ),
                ),
                (
                    "old_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Old name"
                    ),
                ),
                (
                    "old_prefix",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("вул.", "вулиця"),
                            ("б.", "бульвар"),
                            ("пр.", "проспект"),
                            ("пров.", "провулок"),
                        ],
                        max_length=6,
                        verbose_name="Old prefix",
                    ),
                ),
            ],
            options={
                "verbose_name": "Street",
                "verbose_name_plural": "Streets",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Cell",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated"),
                ),
                ("title", models.CharField(max_length=15)),
                (
                    "box",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cells",
                        to="search_keys.box",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cell",
                "verbose_name_plural": "Cells",
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Building",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated"),
                ),
                (
                    "number",
                    models.CharField(max_length=15, verbose_name="Building number"),
                ),
                (
                    "cell",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="search_keys.cell",
                        verbose_name="Cell",
                    ),
                ),
                (
                    "street",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buildings",
                        to="search_keys.street",
                        verbose_name="Street",
                    ),
                ),
            ],
            options={
                "verbose_name": "Building number",
                "verbose_name_plural": "Building numbers",
                "ordering": ("number",),
            },
        ),
    ]
