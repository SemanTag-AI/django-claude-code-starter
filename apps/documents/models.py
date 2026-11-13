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
        default=Status.WAITING,
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

    def __str__(self) -> str:
        """Return the title."""
        return self.title
