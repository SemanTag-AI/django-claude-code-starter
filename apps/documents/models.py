"""The one thing this app stores: a document and its review."""

from django.conf import settings
from django.db import models
from django.utils import timezone

from .choices import Status


class Document(models.Model):
    """A document somebody submitted, and what the reviewer decided."""

    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name.title()) for status in Status],
        default=Status.WAITING.value,
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="submitted_documents"
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reviewed_documents",
        null=True,
        blank=True,
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Newest first, everywhere."""

        ordering = ["-submitted_at", "-pk"]
        # The rules live in rules.py. These are the same rules on the one layer that
        # still holds when the code above it has a bug.
        constraints = [
            models.CheckConstraint(
                condition=models.Q(reviewed_by__isnull=True) | ~models.Q(reviewed_by=models.F("submitted_by")),
                name="reviewer_is_not_the_submitter",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(status=Status.WAITING.value, reviewed_by__isnull=True, reviewed_at__isnull=True)
                    | (
                        ~models.Q(status=Status.WAITING.value)
                        & models.Q(reviewed_by__isnull=False, reviewed_at__isnull=False)
                    )
                ),
                name="reviewed_exactly_when_decided",
            ),
        ]

    def __str__(self) -> str:
        """Return the title."""
        return self.title
