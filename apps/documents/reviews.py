"""Recording a review."""

from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser

from .choices import Status
from .models import Document


def record_review(document: Document, reviewer: AbstractBaseUser, decision: Status, now: datetime) -> bool:
    """Record the decision of a reviewer. Return False if the document was no longer waiting."""
    raise NotImplementedError("recording a review is not written yet")
