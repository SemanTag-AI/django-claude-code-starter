"""The numbers on the dashboard."""

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    """How many documents stand where, for one user at one moment."""

    waiting: int
    overdue: int
    approved: int
    rejected: int
    for_you: int


def dashboard_summary(user: AbstractBaseUser, now: datetime) -> DashboardSummary:
    """Count the documents per status, and those that wait for a review by this user."""
    raise NotImplementedError("the dashboard summary is not written yet")
