import { StudioEvent } from "./types";

// Hardcoded for this prototype. In a real version, the studio would maintain
// these through their own admin interface - they're not about any one
// dancer's arrival time, so they don't go through the extraction/reconcile
// pipeline that produces DancerEvent entries.
export const studioEvents: StudioEvent[] = [
  {
    id: "ticket-sales-open",
    title: "Reverie tickets go on sale",
    date: "2026-05-04",
    time: "10:00",
    note: "Ticketmaster - studio-wide info, not specific to Colette's schedule.",
  },
];
