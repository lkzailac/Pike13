"""
Stand-in for the Claude extraction call.

In production, each function below sends the relevant file(s) from context/
to Claude (vision for screenshots/PDF pages, text for plain copy) with a
prompt that asks for these exact fields back as structured JSON. For this
prototype, the API key is mocked, but the data is real and was manually
transcribed from the actual files in context/ so the reconciliation logic
downstream (app/reconcile.py) can be exercised against real source data.

Each function notes which file in context/ it stands in for, so swapping in
a real `anthropic` client call later is a localized change.
"""

_STUDIO_ADDRESSES = {
    "skaneateles": "1351 E Genesee St, Skaneateles, NY 13152",
}


def get_studio_address(location_hint: str) -> str:
    """Resolve a studio location reference (e.g. 'Studio 2-Skan', 'SKANEATELES') to a street address."""
    hint = location_hint.lower()
    if "skan" in hint:
        return _STUDIO_ADDRESSES["skaneateles"]
    raise ValueError(f"No known address for studio location: {location_hint!r}")


def get_dancer_enrollment() -> dict:
    """Stands in for extraction from 'Screenshot ... 2.03.05 PM.png' (Enrollment table).

    This is one combined weekly class (Ballet+Tap together), but it performs as
    two separate numbers in the recital - see get_dress_rehearsal_slots().
    """
    return {
        "first_name": "Colette",
        "last_name": "Cloherty",
        "season": "Fall/Spring Skaneateles 25-26",
        "class_name": "Mini PreK Ballet/Tap Tues.",
        "class_day": "Tuesday",
        "start_time": "17:15",
        "length_minutes": 40,
        "location": get_studio_address("Studio 2-Skan"),
        "instructor": "Grace Mayer",
        "source_doc": "Screenshot 2026-06-25 at 2.03.05 PM.png",
    }


def get_show_assignment() -> dict:
    """Stands in for extraction from 'Colette is in the DREAM show - update.pdf'."""
    return {
        "dancer_first_name": "Colette",
        "show": "DREAM",
        "class_season_start": "2026-01-02",
        "class_season_end": "2026-06-21",  # through recital day
        "source_doc": "Colette is in the DREAM show - update.pdf",
    }


def get_recital_shows() -> dict:
    """Stands in for extraction from the Reverie poster screenshots + venue card."""
    return {
        "WONDER": {"date": "2026-06-21", "showtime": "10:00", "venue": "Landmark Theater, 362 S Salina St, Syracuse, NY 13202"},
        "IMAGINE": {"date": "2026-06-21", "showtime": "14:30", "venue": "Landmark Theater, 362 S Salina St, Syracuse, NY 13202"},
        "DREAM": {"date": "2026-06-21", "showtime": "18:30", "venue": "Landmark Theater, 362 S Salina St, Syracuse, NY 13202"},
        "_source_doc": "Screenshot 2026-06-25 at 1.58.47/1.59.12/2.00.07/2.00.40 PM.png",
    }


def get_photo_day_slots() -> list[dict]:
    """Stands in for extraction from 'Screenshot ... 1.59.48 PM.png' (Photo Day grid)."""
    return [
        {
            "class_name": "Mini PreK Ballet/Tap Tues.",
            "class_day": "Tuesday",
            "class_time": "17:15",
            "photo_slot_start": "13:50",
            "photo_slot_end": "14:00",
            "date": "2026-05-03",
            "location": get_studio_address("SKANEATELES"),
            "source_doc": "Screenshot 2026-06-25 at 1.59.48 PM.png",
        },
        # ... other classes' rows omitted for this prototype; only Colette's class matters.
    ]


def get_dress_rehearsal_slots() -> list[dict]:
    """Stands in for extraction from 'Screenshot ... 1.59.12 PM.png' (Show Order / Dress Rehearsal grid).

    Colette's single combined Ballet/Tap class performs as two separate
    numbers in the DREAM show (row 7 and row 20 of the grid), each with its
    own on-stage call time, so each gets its own dress rehearsal slot here.
    """
    return [
        {
            "show": "DREAM",
            "row": 7,
            "studio": "Fall/Spring Skaneateles 25-26",
            "class_name": "Mini PreK Ballet Tues.",
            "dance_style": "Ballet",
            "class_day": "Tuesday",
            "class_time": "17:15",
            "teacher": "Grace",
            "song_title": "Ma Belle Evangeline",
            "rehearsal_date": "2026-06-20",
            "onstage_start": "18:03",
            "onstage_end": "18:08",
            "source_doc": "Screenshot 2026-06-25 at 1.59.12 PM.png",
        },
        {
            "show": "DREAM",
            "row": 20,
            "studio": "Fall/Spring Skaneateles 25-26",
            "class_name": "Mini PreK Tap Tues.",
            "dance_style": "Tap",
            "class_day": "Tuesday",
            "class_time": "17:15",
            "teacher": "Grace",
            "song_title": "Almost There",
            "rehearsal_date": "2026-06-20",
            "onstage_start": "19:00",
            "onstage_end": "19:05",
            "source_doc": "Screenshot 2026-06-25 at 1.59.12 PM.png",
        },
    ]


def get_arrival_rules() -> dict:
    """Stands in for extraction of the prose rules in 'Reverie Dress Rehearsal Email '26.pdf'."""
    return {
        "dress_rehearsal": {
            "offset_minutes": 30,
            "basis_text": "Email: \"Dancers should arrive 30 minutes before their scheduled rehearsal time, dressed in their costume.\"",
        },
        "recital": {
            "offset_minutes": 45,
            "basis_text": "Email: \"On recital day, dancers must arrive 45 minutes prior to showtime, fully dressed with hair and makeup already done.\"",
        },
        # Note: the email also states doors open 40 min before showtime for ticketed
        # *audience* members. That rule deliberately is not applied to the dancer's
        # own arrival time below - it governs guests, not performers.
    }
