"""Fill an empty register with two users and a dozen documents, to look around in."""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.documents.choices import Status, Tag
from apps.documents.models import Document

#: Printed in the README. It is a password for a demo on your own machine and for nothing else.
DEMO_PASSWORD = "review-me-please"  # noqa: S105
DEMO_USERS = ("alice", "bob")

# Title, submitter, days ago, status, tags.
DEMO_DOCUMENTS = (
    ("Access policy", "alice", 1, Status.WAITING, [Tag.POLICY]),
    ("Backup procedure", "bob", 3, Status.WAITING, [Tag.PROCEDURE]),
    ("Supplier overview", "alice", 12, Status.WAITING, [Tag.REPORT, Tag.CONTRACT]),
    ("Onboarding checklist", "bob", 30, Status.WAITING, [Tag.PROCEDURE, Tag.PERSONAL_DATA]),
    ("Incident report October", "alice", 31, Status.WAITING, [Tag.REPORT]),
    ("Hosting contract", "bob", 45, Status.WAITING, [Tag.CONTRACT]),
    ("Privacy notice", "alice", 20, Status.APPROVED, [Tag.POLICY, Tag.PERSONAL_DATA]),
    ("Password procedure", "bob", 40, Status.APPROVED, [Tag.PROCEDURE]),
    ("Annual security report", "alice", 60, Status.APPROVED, [Tag.REPORT]),
    ("Clean desk policy", "bob", 75, Status.APPROVED, [Tag.POLICY]),
    ("Old cleaning contract", "alice", 50, Status.REJECTED, [Tag.CONTRACT]),
    ("Draft retention policy", "bob", 8, Status.REJECTED, [Tag.POLICY, Tag.PERSONAL_DATA]),
)


class Command(BaseCommand):
    """Create the demo users and documents, once."""

    help = "Create two demo users and a dozen documents. Only works with debug on."

    def handle(self, *args: object, **options: object) -> None:
        """Refuse outside development, do nothing the second time, otherwise fill the register.

        All or nothing: half a set of demo data would block the next attempt.
        """
        if not settings.DEBUG:
            raise CommandError("The demo users have a public password. Refusing to create them with debug off.")
        users = get_user_model().objects
        if users.filter(username__in=DEMO_USERS).exists():
            self.stdout.write("The demo data is already there. Nothing was created.")
            return

        with transaction.atomic():
            people = {name: users.create_user(username=name, password=DEMO_PASSWORD) for name in DEMO_USERS}
            now = timezone.now()
            for title, submitter, days_ago, status, tags in DEMO_DOCUMENTS:
                reviewed = status != Status.WAITING
                reviewer = next(person for name, person in people.items() if name != submitter)
                submitted_at = now - timedelta(days=days_ago)
                Document.objects.create(
                    title=title,
                    body=f"This is where the text of the document '{title}' would be.",
                    tags=[tag.value for tag in tags],
                    status=status,
                    submitted_by=people[submitter],
                    submitted_at=submitted_at,
                    reviewed_by=reviewer if reviewed else None,
                    reviewed_at=submitted_at + timedelta(days=2) if reviewed else None,
                )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created the users {' and '.join(DEMO_USERS)} (password: {DEMO_PASSWORD}) "
                f"and {len(DEMO_DOCUMENTS)} documents."
            )
        )
