import { formatShortDate, formatTime } from "@/lib/format";
import { DancerEvent, StudioEvent } from "@/lib/types";

export function DancerEventCard({ event }: { event: DancerEvent }) {
  const arrivalDiffers = event.listed_time !== event.arrival_time;
  // Recurring weekly-class instances still carry their RRULE string; one-off
  // events (Photo Day, Dress Rehearsal, Recital Day) don't - so they're the
  // "special" events worth visually calling out from the routine weekly class.
  const isSpecial = !event.recurrence;

  return (
    <li
      className={
        isSpecial
          ? "rounded-xl border-l-4 border-violet-500 bg-violet-50 p-4 shadow-md ring-1 ring-violet-200 dark:bg-violet-950/30 dark:ring-violet-900"
          : "rounded-xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900"
      }
    >
      <div className="flex items-baseline justify-between gap-2">
        <div>
          <h3
            className={
              isSpecial
                ? "font-semibold text-zinc-950 dark:text-zinc-50"
                : "font-medium text-zinc-700 dark:text-zinc-300"
            }
          >
            {event.title}
          </h3>
          <p className="text-xs text-zinc-500 dark:text-zinc-500">
            {formatShortDate(event.date)}
          </p>
        </div>
        <span
          className={
            isSpecial
              ? "whitespace-nowrap rounded-full bg-violet-600 px-2 py-0.5 text-xs font-semibold uppercase tracking-wide text-white"
              : "whitespace-nowrap text-xs font-medium uppercase tracking-wide text-zinc-400 dark:text-zinc-600"
          }
        >
          {isSpecial ? "Special Event" : "Weekly Class"}
        </span>
      </div>
      <p
        className={
          isSpecial
            ? "mt-2 text-lg font-semibold text-violet-700 dark:text-violet-400"
            : "mt-2 text-sm font-medium text-zinc-700 dark:text-zinc-300"
        }
      >
        Arrive {formatTime(event.arrival_time)}
      </p>
      {arrivalDiffers && (
        <p className="text-xs text-zinc-500 dark:text-zinc-500">
          (Start time: {formatTime(event.listed_time)})
        </p>
      )}
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
        {event.location}
      </p>
      <details className="mt-2 text-xs text-zinc-500 dark:text-zinc-500">
        <summary className="cursor-pointer select-none">More Info</summary>
        <p className="mt-1">{event.arrival_basis}</p>
        <p className="mt-1 italic">Source: {event.source_doc}</p>
      </details>
    </li>
  );
}

export function StudioEventCard({ event }: { event: StudioEvent }) {
  return (
    <li className="rounded-xl border border-zinc-200 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-950/50">
      <div className="flex items-baseline justify-between gap-2">
        <div>
          <h3 className="text-sm font-medium text-zinc-600 dark:text-zinc-400">
            {event.title}
          </h3>
          <p className="text-xs text-zinc-500 dark:text-zinc-500">
            {formatShortDate(event.date)}
          </p>
        </div>
        <span className="whitespace-nowrap text-xs font-medium uppercase tracking-wide text-zinc-400 dark:text-zinc-600">
          Studio
        </span>
      </div>
      <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-500">
        {formatTime(event.time)}
      </p>
      <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-500">
        {event.note}
      </p>
    </li>
  );
}
