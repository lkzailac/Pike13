import { DancerEvent } from "./types";

// Expands the simple RRULE shapes this prototype's backend emits
// (FREQ=WEEKLY;BYDAY=<day>;UNTIL=<YYYYMMDD>) into one concrete event per
// occurrence, so the scrollable calendar can show the weekly class on every
// date it actually happens, not just its first occurrence.
export function expandRecurrence(event: DancerEvent): DancerEvent[] {
  if (!event.recurrence) return [event];

  const until = event.recurrence.match(/UNTIL=(\d{8})/)?.[1];
  if (!until) return [event];

  const untilDate = new Date(
    Number(until.slice(0, 4)),
    Number(until.slice(4, 6)) - 1,
    Number(until.slice(6, 8))
  );

  const [y, m, d] = event.date.split("-").map(Number);
  let cur = new Date(y, m - 1, d);

  const occurrences: DancerEvent[] = [];
  while (cur <= untilDate) {
    const dateStr = `${cur.getFullYear()}-${String(cur.getMonth() + 1).padStart(2, "0")}-${String(
      cur.getDate()
    ).padStart(2, "0")}`;
    occurrences.push({ ...event, id: `${event.id}-${dateStr}`, date: dateStr });
    cur = new Date(cur.getFullYear(), cur.getMonth(), cur.getDate() + 7);
  }
  return occurrences;
}
