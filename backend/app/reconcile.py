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
            title=enrollment["class_style_name"],
            date=first_class_date,
            listed_time=enrollment["start_time"],
            arrival_time=enrollment["start_time"],
            arrival_basis=(
                f"Weekly class start time per enrollment record (instructor: "
                f"{enrollment['instructor']}) - no arrival buffer specified in source "
                f"material. Season runs {first_class_date} to {last_class_date} per "
                f"{show_assignment['source_doc']}."
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

    # 3. Dress Rehearsal - one combined class can perform multiple numbers, each
    # with its own on-stage call time, so match ALL rows, not just the first.
    rehearsal_slots = [
        s
        for s in get_dress_rehearsal_slots()
        if s["show"] == show_assignment["show"] and _same_class(enrollment, s)
    ]
    for slot in rehearsal_slots:
        rule = arrival_rules["dress_rehearsal"]
        arrival = _subtract_minutes(slot["onstage_start"], rule["offset_minutes"])
        events.append(
            CalendarEvent(
                id=f"dress-rehearsal-{slot['dance_style'].lower()}",
                title=f"Dress Rehearsal - {slot['dance_style']} (\"{slot['song_title']}\")",
                date=slot["rehearsal_date"],
                listed_time=slot["onstage_start"],
                arrival_time=arrival,
                arrival_basis=(
                    f"Row {slot['row']} of the Show Order/Dress Rehearsal grid: "
                    f"{slot['dance_style']} number \"{slot['song_title']}\", on-stage "
                    f"{slot['onstage_start']}-{slot['onstage_end']} (matched by show + "
                    f"class day/time). {rule['basis_text']} => arrive by {arrival}."
                ),
                location="Landmark Theater - Artist Entrance, West Jefferson St, Syracuse, NY",
                source_doc=slot["source_doc"],
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
                    f"Catherine is assigned to the {show_assignment['show']} show "
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
