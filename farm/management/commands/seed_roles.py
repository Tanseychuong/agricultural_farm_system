"""
Seeds the five Django auth Groups used for role-based access control,
mirroring the PostgreSQL roles defined in Phase 7 (farm_admin, farm_manager,
inventory_officer, sales_officer, farm_worker).

Safe to run multiple times (idempotent) — existing groups are updated in
place rather than duplicated. Does not touch any existing users, models,
or the database schema.

Usage:
    python manage.py seed_roles
"""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


# model names use Django's default lowercase, no-underscore codename form
FULL_ACCESS = ["add", "change", "delete", "view"]
MANAGE = ["add", "change", "delete", "view"]
LIMITED_WRITE = ["add", "change", "view"]
READ_ONLY = ["view"]

ROLE_DEFINITIONS = {
    "Farm Administrator": {
        # every model in the farm app, full CRUD
        "models": [
            "farm", "crop", "worker", "equipment", "fertilizer", "customer",
            "harvest", "sale", "cropworker", "equipmentassignment",
            "equipmentmaintenance", "fertilizerusage", "harvestworker",
            "saleitem",
        ],
        "actions": FULL_ACCESS,
    },
    "Farm Manager": {
        "models": [
            "farm", "crop", "worker", "harvest", "cropworker",
            "harvestworker", "equipmentassignment",
        ],
        "actions": MANAGE,
    },
    "Inventory Officer": {
        "models": [
            "equipment", "fertilizer", "fertilizerusage",
            "equipmentmaintenance",
        ],
        "actions": LIMITED_WRITE,
    },
    "Sales Officer": {
        "models": ["customer", "sale", "saleitem"],
        "actions": LIMITED_WRITE,
    },
    "Farm Worker": {
        "models": ["crop", "cropworker", "harvest", "harvestworker", "equipment"],
        "actions": READ_ONLY,
    },
}


class Command(BaseCommand):
    help = "Create/update the standard RBAC groups (Farm Administrator, Farm Manager, Inventory Officer, Sales Officer, Farm Worker)."

    def handle(self, *args, **options):
        for role_name, definition in ROLE_DEFINITIONS.items():
            group, created = Group.objects.get_or_create(name=role_name)

            codenames = [
                f"{action}_{model}"
                for model in definition["models"]
                for action in definition["actions"]
            ]

            permissions = Permission.objects.filter(
                content_type__app_label="farm",
                codename__in=codenames,
            )

            found = set(permissions.values_list("codename", flat=True))
            missing = set(codenames) - found
            if missing:
                self.stdout.write(
                    self.style.WARNING(
                        f"  {role_name}: {len(missing)} permission(s) not found "
                        f"(run 'python manage.py migrate' first if this is a fresh DB): "
                        f"{sorted(missing)}"
                    )
                )

            group.permissions.set(permissions)

            verb = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{verb} group '{role_name}' with {permissions.count()} permission(s)."
                )
            )

        self.stdout.write(self.style.SUCCESS("Role seeding complete."))