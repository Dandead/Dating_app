from django.core.management.base import BaseCommand
from django.conf import settings
from users.factories import DatingUserFactory


class Command(BaseCommand):
    help = "Create test users."

    def add_arguments(self, parser):
        parser.add_argument(
            "total",
            type=int,
            help="Indicates the number of users to be created.",
        )

    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR("Cannot create test users in production.")
            )
            return

        total = kwargs["total"]
        DatingUserFactory.create_batch(total)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {total} test users.")
        )
