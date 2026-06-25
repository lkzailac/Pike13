"""
Merges the raw extracted records into the dancer's final event list.

This is the part of the pipeline that matters most for trust: it matches the
dancer's enrolled class against per-event slot tables (which label classes
slightly differently than the enrollment record), and keeps the *listed*
time and the *arrival* time as separate fields so nothing gets silently
collapsed into a guess.
"""

from datetime import datetime, timedelta

from app.extraction import (
    get_arrival_rules,
    get_dancer_enrollment,
    get_dress_rehearsal_slots,
    get_photo_day_slots,
    get_recital_shows,
    get_show_assignment,
)
from app.models import CalendarEvent


def _same_class(enrollment: dict, slot: dict) -> bool:
    """Match a slot-table row to the dancer's enrolled class by day + start time.

    Class name strings differ slightly between documents (e.g. studio suffixes),
    so day-of-week + start time is the more reliable join key here.
    """
    return (
        slot["class_day"] == enrollment["class_day"]
        and slot["class_time"] == enrollment["start_time"]
    )


def _subtract_minutes(hhmm: str, minutes: int) -> str:
    t = datetime.strptime(hhmm, "%H:%M") - timedelta(minutes=minutes)
    return t.strftime("%H:%M")


def _last_weekday_on_or_before(date_str: str, weekday: int) -> str:
    """weekday: Monday=0 ... Sunday=6. Used to find the last Tuesday on/before the recital."""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    while d.weekday() != weekday:
        d -= timedelta(days=1)
    return d.strftime("%Y-%m-%d")


def _first_weekday_on_or_after(date_str: str, weekday: int) -> str:
    d = datetime.strptime(date_str, "%Y-%m-%d")
    while d.weekday() != weekday:
        d += timedelta(days=1)
    return d.strftime("%Y-%m-%d")


def build_dancer_events() -> list[CalendarEvent]:
    enrollment = get_dancer_enrollment()
    show_assignment = get_show_assignment()
    shows = get_recital_shows()
    arrival_rules = get_arrival_rules()

    events: list[CalendarEvent] = []

    # 1. Weekly recurring class, bounded by the season dates in the show-assignment doc.
    first_class_date = _first_weekday_on_or_after(
        show_assignment["class_season_start"], weekday=1  # Tuesday
    )
    last_class_date = _last_weekday_on_or_before(
        show_assignment["class_season_end"], weekday=1
    )
    events.append(
        CalendarEvent(
            id="weekly-class",
            title=f"{enrollment['class_name']} ({enrollment['instructor']})",
            date=first_class_date,
            listed_time=enrollment["start_time"],
            arrival_time=enrollment["start_time"],
            arrival_basis=(
                "Weekly class start time per enrollment record - no arrival buffer "
                f"specified in source material. Season runs {first_class_date} to "
                f"{last_class_date} per {show_assignment['source_doc']}."
            ),
            location=enrollment["location"],
            source_doc=enrollment["source_doc"],
            recurrence=f"FREQ=WEEKLY;BYDAY=TU;UNTIL={last_class_date.replace('-', '')}",
            duration_minutes=enrollment["length_minutes"],
        )
    )

    # 2. Photo Day - match enrollment to the dancer's specific slot.
    photo_slot = next(
        (s for s in get_photo_day_slots() if _same_class(enrollment, s)), None
    )
    if photo_slot:
        events.append(
            CalendarEvent(
                id="photo-day",
                title=f"Photo Day - {enrollment['class_name']}",
                date=photo_slot["date"],
                listed_time=photo_slot["photo_slot_start"],
                arrival_time=photo_slot["photo_slot_start"],
                arrival_basis=(
                    f"Assigned photo slot {photo_slot['photo_slot_start']}-"
                    f"{photo_slot['photo_slot_end']} for {enrollment['class_name']} "
                    "(matched by class day + start time against the Photo Day grid). "
                    "This is the slot itself, not a pre-arrival buffer."
                ),
                location=photo_slot["location"],
                source_doc=photo_slot["source_doc"],
                duration_minutes=10,
            )
        )

    # 3. Dress Rehearsal - match enrollment + show to the dancer's on-stage slot.
    rehearsal_slot = next(
        (
            s
            for s in get_dress_rehearsal_slots()
            if s["show"] == show_assignment["show"] and _same_class(enrollment, s)
        ),
        None,
    )
    if rehearsal_slot:
        rule = arrival_rules["dress_rehearsal"]
        arrival = _subtract_minutes(rehearsal_slot["onstage_start"], rule["offset_minutes"])
        events.append(
            CalendarEvent(
                id="dress-rehearsal",
                title=f"Dress Rehearsal - {show_assignment['show']} show",
                date=rehearsal_slot["rehearsal_date"],
                listed_time=rehearsal_slot["onstage_start"],
                arrival_time=arrival,
                arrival_basis=(
                    f"On-stage rehearsal slot is {rehearsal_slot['onstage_start']}-"
                    f"{rehearsal_slot['onstage_end']} (matched by show + class day/time "
                    f"against the Show Order/Dress Rehearsal grid). {rule['basis_text']} "
                    f"=> arrive by {arrival}."
                ),
                location="Landmark Theater - Artist Entrance, West Jefferson St, Syracuse, NY",
                source_doc=rehearsal_slot["source_doc"],
                duration_minutes=5,
            )
        )

    # 4. Recital Day - the dancer's assigned show.
    show = shows.get(show_assignment["show"])
    if show:
        rule = arrival_rules["recital"]
        arrival = _subtract_minutes(show["showtime"], rule["offset_minutes"])
        events.append(
            CalendarEvent(
                id="recital-day",
                title=f"Recital Day - {show_assignment['show']} show",
                date=show["date"],
                listed_time=show["showtime"],
                arrival_time=arrival,
                arrival_basis=(
                    f"Colette is assigned to the {show_assignment['show']} show "
                    f"({show_assignment['source_doc']}), showtime {show['showtime']}. "
                    f"{rule['basis_text']} => arrive by {arrival}. (Note: the email's "
                    "\"doors open 40 min prior\" rule is for ticketed audience members, "
                    "not performers, and is intentionally not used here.)"
                ),
                location=show["venue"],
                source_doc=shows["_source_doc"],
                duration_minutes=120,
            )
        )

    return events
