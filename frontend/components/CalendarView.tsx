"use client";

import { useEffect, useRef } from "react";

import { DancerEventCard, StudioEventCard } from "@/components/EventCards";
import { AgendaItem } from "@/lib/types";

export type MonthGroup = {
  monthKey: string; // YYYY-MM
  monthLabel: string;
  items: AgendaItem[];
};

export default function CalendarView({ groups }: { groups: MonthGroup[] }) {
  const sectionRefs = useRef<Record<string, HTMLElement | null>>({});

  useEffect(() => {
    const now = new Date();
    const currentKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
    // Scroll to the current month, or the nearest upcoming one if there's
    // nothing scheduled this month; fall back to the last month we have.
    const targetKey =
      groups.find((g) => g.monthKey >= currentKey)?.monthKey ??
      groups[groups.length - 1]?.monthKey;
    if (targetKey) {
      sectionRefs.current[targetKey]?.scrollIntoView({ block: "start" });
    }
  }, [groups]);

  return (
    <div className="flex-1 overflow-y-auto">
      {groups.map((group) => (
        <section
          key={group.monthKey}
          ref={(el) => {
            sectionRefs.current[group.monthKey] = el;
          }}
        >
          <h2 className="sticky top-0 z-10 border-b border-zinc-200 bg-zinc-100 px-6 py-2 text-sm font-semibold text-zinc-700 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-300">
            {group.monthLabel}
          </h2>
          <ol className="mx-auto flex max-w-2xl flex-col gap-3 px-6 py-4">
            {group.items.map((item) =>
              item.kind === "dancer" ? (
                <DancerEventCard key={item.event.id} event={item.event} />
              ) : (
                <StudioEventCard key={item.event.id} event={item.event} />
              )
            )}
          </ol>
        </section>
      ))}
    </div>
  );
}
