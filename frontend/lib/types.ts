// Mirrors backend/app/models.py CalendarEvent - one event the dancer must personally attend.
export type DancerEvent = {
  id: string;
  title: string;
  date: string; // YYYY-MM-DD
  listed_time: string; // HH:MM, 24h - time printed in the source material
  arrival_time: string; // HH:MM, 24h - time the dancer actually needs to be there
  arrival_basis: string;
  location: string;
  source_doc: string;
  recurrence?: string | null;
  duration_minutes: number;
};

// Studio-wide info (ticket sales, box office hours, etc.) - not dancer-specific,
// not extracted by the backend pipeline. Modeled here as if a studio admin
// maintains these separately from the per-dancer extraction pipeline.
export type StudioEvent = {
  id: string;
  title: string;
  date: string; // YYYY-MM-DD
  time: string; // HH:MM, 24h
  note: string;
};

export type AgendaItem =
  | { kind: "dancer"; sortTime: string; event: DancerEvent }
  | { kind: "studio"; sortTime: string; event: StudioEvent };
