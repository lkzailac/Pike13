from typing import Optional

from pydantic import BaseModel


class CalendarEvent(BaseModel):
    """A single dancer-facing calendar event, already resolved to an arrival time."""

    id: str
    title: str
    date: str  # YYYY-MM-DD, first occurrence for recurring events
    listed_time: str  # HH:MM, 24h - the time printed in the source material
    arrival_time: str  # HH:MM, 24h - the time the dancer actually needs to be there
    arrival_basis: str  # plain-English explanation of how arrival_time was derived
    location: str
    source_doc: str  # which file in context/ this was extracted from
    recurrence: Optional[str] = None  # RRULE string, only set for recurring events
    duration_minutes: int = 30
