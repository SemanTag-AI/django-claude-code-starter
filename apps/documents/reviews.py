"""Recording a review."""

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import PermissionDenied

from .choices import Status
from .models import Document
from .rules import may_review


def record_review(document: Document, reviewer: AbstractBaseUser, decision: Status, now: datetime) -> bool:
    """Record the decision of a reviewer. Return False if the document was no longer waiting.

    The status changes in one conditional update, so that of two reviewers who decide
    at the same moment exactly one is recorded.

    Raises:
        ValueError: if the decision is not an approval or a rejection.
        PermissionDenied: if this reviewer may not review this document.
    """
    if decision not in (Status.APPROVED, Status.REJECTED):
        raise ValueError("A review is an approval or a rejection.")
    if not may_review(document, reviewer):
        raise PermissionDenied("Whoever submitted a document does not review it.")
    changed = Document.objects.filter(pk=document.pk, status=Status.WAITING).update(
        status=decision, reviewed_by=reviewer, reviewed_at=now
    )
    return changed == 1
