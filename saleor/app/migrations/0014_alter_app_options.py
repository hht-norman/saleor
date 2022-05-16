# Generated by Django 3.2.13 on 2022-05-11 13:07
from django.db import migrations
from django.db.models.signals import post_migrate


def assign_permissions(apps, schema_editor):
    def on_migrations_complete(sender=None, **kwargs):
        Group = apps.get_model("auth", "Group")
        Permission = apps.get_model("auth", "Permission")
        ContentType = apps.get_model("contenttypes", "ContentType")

        ct, _ = ContentType.objects.get_or_create(app_label="app", model="app")
        manage_observability, _ = Permission.objects.get_or_create(
            name="Manage observability",
            content_type=ct,
            codename="manage_observability",
        )
        manage_apps = Permission.objects.filter(
            codename="manage_apps", content_type__app_label="app"
        )
        for group in Group.objects.filter(permissions__in=manage_apps).iterator():
            group.permissions.add(manage_observability)

    post_migrate.connect(on_migrations_complete, weak=False)


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_alter_appextension_mount"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="app",
            options={
                "ordering": ("name", "pk"),
                "permissions": (
                    ("manage_apps", "Manage apps"),
                    ("manage_observability", "Manage observability"),
                ),
            },
        ),
        migrations.RunPython(assign_permissions, migrations.RunPython.noop),
    ]