from enum import Enum

from pydantic import BaseModel


class ComplaintStatus(str, Enum):
    OPEN = "open"
    PENDING_REVIEW = "pending_review"
    IN_PROGRESS = "in_progress"
    ESCALATED = "escalated"
    ON_HOLD = "on_hold"
    RESOLVED = "resolved"
    REOPENED = "reopened"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    CLOSED = "closed"


class ComplaintRequest(BaseModel):
    description: str
    session_id: str
    name: str
    mobile_number: str


class ComplaintResponse(ComplaintRequest):
    _id: str
    status: ComplaintStatus