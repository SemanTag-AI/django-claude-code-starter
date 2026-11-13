"""The rules of the register. Plain functions: they know nothing about pages."""

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser

from .models import Document

#: A document may wait this many full days for its review before it counts as overdue.
REVIEW_DEADLINE_DAYS = 30


def may_review(document: Document, user: AbstractBaseUser) -> bool:
    """Say whether this user may approve or reject this document."""
    raise NotImplementedError("the review rule is not written yet")


def is_overdue(document: Document, now: datetime) -> bool:
    """Say whether this document has waited too long for its review."""
    raise NotImplementedError("the overdue rule is not written yet")
