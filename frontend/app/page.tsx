import CalendarView, { MonthGroup } from "@/components/CalendarView";
import { fetchDancerEvents, icsDownloadUrl } from "@/lib/api";
import { expandRecurrence } from "@/lib/expand";
import { formatMonthLabel } from "@/lib/format";
import { studioEvents } from "@/lib/studioEvents";
import { AgendaItem } from "@/lib/types";

export default async function Home() {
  let groups: MonthGroup[] = [];
  let loadError: string | null = null;

  try {
    const dancerEvents = await fetchDancerEvents();
    const expanded = dancerEvents.flatMap(expandRecurrence);

    const agenda: AgendaItem[] = [
      ...expanded.map(
        (event): AgendaItem => ({
          kind: "dancer",
          sortTime: `${event.date}T${event.arrival_time}`,
          event,
        })
      ),
      ...studioEvents.map(
        (event): AgendaItem => ({
          kind: "studio",
          sortTime: `${event.date}T${event.time}`,
          event,
        })
      ),
    ].sort((a, b) => a.sortTime.localeCompare(b.sortTime));

    const byMonth = new Map<string, AgendaItem[]>();
    for (const item of agenda) {
      const monthKey = item.sortTime.slice(0, 7);
      if (!byMonth.has(monthKey)) byMonth.set(monthKey, []);
      byMonth.get(monthKey)!.push(item);
    }
    groups = Array.from(byMonth.entries()).map(([monthKey, items]) => ({
      monthKey,
      monthLabel: formatMonthLabel(monthKey),
      items,
    }));
  } catch {
    loadError =
      "Couldn't reach the backend at " +
      (process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000") +
      ". Is it running?";
  }

  return (
    <div className="flex h-screen flex-col bg-zinc-50 dark:bg-black">
      <header className="shrink-0 border-b border-zinc-200 bg-zinc-50 px-6 py-6 dark:border-zinc-800 dark:bg-black">
        <div className="mx-auto max-w-2xl">
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-950 dark:text-zinc-50">
            Colette&apos;s Dance Calendar
          </h1>
          <a
            href={icsDownloadUrl()}
            className="mt-4 inline-flex w-fit items-center justify-center rounded-full bg-violet-600 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-violet-700"
          >
            Add All Events to Your Calendar (.ics)
          </a>

          {loadError && (
            <p className="mt-4 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-300">
              {loadError}
            </p>
          )}
        </div>
      </header>

      {!loadError && <CalendarView groups={groups} />}
    </div>
  );
}
