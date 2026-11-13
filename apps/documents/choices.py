"""The fixed sets of values a document can carry."""

from enum import StrEnum


class Status(StrEnum):
    """Where a document stands in its review."""

    WAITING = "waiting"
    APPROVED = "approved"
    REJECTED = "rejected"


class Tag(StrEnum):
    """What a document is about. A document can carry several."""

    POLICY = "policy"
    PROCEDURE = "procedure"
    CONTRACT = "contract"
    REPORT = "report"
    PERSONAL_DATA = "personal-data"
