from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from app.ics_gen import build_ics
from app.reconcile import build_dancer_events

app = FastAPI(title="Dancer Calendar Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/events")
def get_events():
    return build_dancer_events()


@app.get("/api/ics")
def get_ics():
    ics_bytes = build_ics(build_dancer_events())
    return Response(
        content=ics_bytes,
        media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=Catherine-dance-calendar.ics"},
    )
