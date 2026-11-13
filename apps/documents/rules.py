"""The rules of the register. Plain functions: they know nothing about pages."""

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser

from .choices import Status
from .models import Document

#: A document may wait this many full days for its review before it counts as overdue.
REVIEW_DEADLINE_DAYS = 30


def may_review(document: Document, user: AbstractBaseUser) -> bool:
    """Say whether this user may approve or reject this document.

    Whoever submitted a document does not review it. Nobody signs off on their own work.
    """
    return document.submitted_by_id != user.pk


def is_overdue(document: Document, now: datetime) -> bool:
    """Say whether this document has waited too long for its review.

    Only a waiting document can be overdue, and only after more than 30 full days:
    on day 30 it is not overdue, on day 31 it is.
    """
    if document.status != Status.WAITING:
        return False
    return (now - document.submitted_at).days > REVIEW_DEADLINE_DAYS
