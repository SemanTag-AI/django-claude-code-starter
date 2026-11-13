"""The numbers on the dashboard."""

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser
from pydantic import BaseModel

from .choices import Status
from .models import Document
from .rules import is_overdue, may_review


class DashboardSummary(BaseModel):
    """How many documents stand where, for one user at one moment."""

    waiting: int
    overdue: int
    approved: int
    rejected: int
    for_you: int


def dashboard_summary(user: AbstractBaseUser, now: datetime) -> DashboardSummary:
    """Count the documents per status, and those that wait for a review by this user."""
    waiting = list(Document.objects.filter(status=Status.WAITING))
    return DashboardSummary(
        waiting=len(waiting),
        overdue=sum(is_overdue(document, now) for document in waiting),
        approved=Document.objects.filter(status=Status.APPROVED).count(),
        rejected=Document.objects.filter(status=Status.REJECTED).count(),
        for_you=sum(may_review(document, user) for document in waiting),
    )
