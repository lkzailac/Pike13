"""Builds a downloadable .ics file from the dancer's resolved event list.

Every VEVENT is anchored on `arrival_time`, not `listed_time` - the whole
point of this tool is that the calendar entry is when the dancer needs to be
there, not the time printed in the source material. The listed time and the
reasoning are kept in the event description for transparency.
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event
from icalendar.prop import vRecur

from app.models import CalendarEvent

_TZ = ZoneInfo("America/New_York")


def _local_dt(date_str: str, time_str: str) -> datetime:
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=_TZ)


def build_ics(events: list[CalendarEvent]) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//Dancer Calendar Prototype//pike13//")
    cal.add("version", "2.0")

    for evt in events:
        vevent = Event()
        vevent.add("uid", f"{evt.id}@dancer-calendar-prototype")
        vevent.add("summary", evt.title)
        vevent.add("location", evt.location)

        start = _local_dt(evt.date, evt.arrival_time)
        vevent.add("dtstart", start)
        vevent.add("dtend", start + timedelta(minutes=evt.duration_minutes))

        description = (
            f"Listed time in source material: {evt.listed_time}\n"
            f"Arrival time: {evt.arrival_time}\n\n"
            f"Why: {evt.arrival_basis}\n\n"
            f"Source: {evt.source_doc}"
        )
        vevent.add("description", description)

        if evt.recurrence:
            vevent.add("rrule", vRecur.from_ical(evt.recurrence))

        cal.add_component(vevent)

    return cal.to_ical()
