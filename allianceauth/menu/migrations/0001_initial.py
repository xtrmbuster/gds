# Generated by Django 4.2.9 on 2024-02-15 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        db_index=True,
                        help_text="Text to show on menu",
                        max_length=150,
                        verbose_name="text",
                    ),
                ),
                (
                    "order",
                    models.IntegerField(
                        db_index=True,
                        default=9999,
                        help_text="Order of the menu. Lowest First",
                        verbose_name="order",
                    ),
                ),
                (
                    "is_hidden",
                    models.BooleanField(
                        default=False,
                        help_text="Hide this menu item.If this item is a folder all items under it will be hidden too",
                        verbose_name="is hidden",
                    ),
                ),
                (
                    "hook_hash",
                    models.CharField(
                        default=None,
                        editable=False,
                        max_length=64,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "classes",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Font Awesome classes to show as icon on menu, e.g. <code>fa-solid fa-house</code>",
                        max_length=150,
                        verbose_name="icon classes",
                    ),
                ),
                (
                    "url",
                    models.TextField(
                        default="",
                        help_text="External URL this menu items will link to",
                        verbose_name="url",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Folder this item is in (optional)",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="menu.menuitem",
                        verbose_name="folder",
                    ),
                ),
            ],
        ),
    ]
