import Image from "next/image";
import Link from "next/link";

const widgetEvents = [
  { dayLabel: "TODAY", title: "Mini PreK Ballet/Tap", time: "5:15 PM" },
  { dayLabel: "Thursday", title: "Dress Rehearsal – Ballet", time: "5:33 PM" },
  { dayLabel: "Sunday", title: "Recital Day (DREAM)", time: "5:45 PM" },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white dark:bg-zinc-950">
      {/* Nav */}
      <header className="sticky top-0 z-10 border-b border-zinc-200 bg-white/95 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/95">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
          <div className="flex items-center gap-10">
            <Image
              src="/logo.png"
              alt="Tiffany's School of Dance"
              width={160}
              height={32}
              className="h-8 w-auto"
              priority
            />
            <nav className="flex items-center gap-6">
              <a
                href="#"
                className="text-sm text-zinc-500 transition-colors hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100"
              >
                Enroll
              </a>
              <a
                href="#"
                className="text-sm text-zinc-500 transition-colors hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100"
              >
                My Classes
              </a>
              <Link
                href="/calendar"
                className="text-sm font-semibold text-violet-600 transition-colors hover:text-violet-700 dark:text-violet-400 dark:hover:text-violet-300"
              >
                My Calendar
              </Link>
              <a
                href="#"
                className="text-sm text-zinc-500 transition-colors hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100"
              >
                Account
              </a>
            </nav>
          </div>

          <div className="flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            Logged in as Catherine
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="bg-gradient-to-b from-violet-50 to-white py-14 dark:from-violet-950/20 dark:to-zinc-950">
        <div className="mx-auto max-w-7xl px-6">
          <p className="text-xs font-semibold uppercase tracking-widest text-violet-500">
            Spring / Summer 2026
          </p>
          <h1 className="mt-2 text-4xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            Welcome back, Catherine!
          </h1>
          <p className="mt-3 max-w-lg text-zinc-500 dark:text-zinc-400">
            The DREAM show recital season is in full swing. Check your upcoming
            schedule, download your ICS calendar, and stay on top of every
            rehearsal and performance.
          </p>
        </div>
      </section>

      {/* Body */}
      <div className="mx-auto max-w-7xl px-6 py-12">
        <div className="flex gap-10">
          {/* Main content */}
          <main className="flex-1 space-y-10">
            {/* News */}
            <section>
              <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-50">
                Studio News
              </h2>
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <NewsCard
                  tag="Announcement"
                  title="Recital tickets now on sale"
                  body="Tickets for the DREAM show are available on Ticketmaster. Reserve your seats early — performances fill up fast!"
                />
                <NewsCard
                  tag="Enrollment"
                  title="Summer enrollment open"
                  body="Register for summer intensive sessions and select fall 2026 classes now. Early enrollment closes July 31."
                />
                <NewsCard
                  tag="Reminder"
                  title="Costume pickup"
                  body="Costumes for the spring recital must be picked up by June 15. Check the front desk for your class's assigned time slot."
                />
                <NewsCard
                  tag="Upcoming"
                  title="Photo Day coming up"
                  body="Class photos are scheduled for May. Check your dancer's specific slot in your calendar."
                />
              </div>
            </section>

            {/* Quick links */}
            <section>
              <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-50">
                Quick Links
              </h2>
              <div className="mt-4 flex flex-wrap gap-2">
                {[
                  "Costume Info",
                  "Recital FAQ",
                  "Drop-In Classes",
                  "Tuition & Fees",
                  "Contact the Studio",
                ].map((label) => (
                  <a
                    key={label}
                    href="#"
                    className="rounded-full border border-zinc-200 px-4 py-2 text-sm text-zinc-600 transition-colors hover:border-violet-300 hover:text-violet-700 dark:border-zinc-700 dark:text-zinc-400 dark:hover:border-violet-600 dark:hover:text-violet-300"
                  >
                    {label}
                  </a>
                ))}
              </div>
            </section>

            {/* About */}
            <section>
              <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-50">
                About Tiffany&apos;s School of Dance
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-zinc-500 dark:text-zinc-400">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
                in reprehenderit in voluptate velit esse cillum dolore eu fugiat
                nulla pariatur.
              </p>
              <p className="mt-3 text-sm leading-relaxed text-zinc-500 dark:text-zinc-400">
                Excepteur sint occaecat cupidatat non proident, sunt in culpa
                qui officia deserunt mollit anim id est laborum. Sed ut
                perspiciatis unde omnis iste natus error sit voluptatem
                accusantium doloremque laudantium, totam rem aperiam eaque ipsa
                quae ab illo inventore veritatis et quasi architecto beatae
                vitae dicta sunt explicabo nemo enim ipsam voluptatem.
              </p>
            </section>
          </main>

          {/* Upcoming Events Widget */}
          <aside className="w-60 shrink-0">
            <div className="sticky top-20 overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
              <div className="border-b border-zinc-100 px-5 py-4 dark:border-zinc-800">
                <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-50">
                  Upcoming Events
                </h3>
              </div>

              <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
                {widgetEvents.map((ev) => (
                  <div key={ev.dayLabel} className="px-5 py-3.5">
                    <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-400">
                      {ev.dayLabel}
                    </p>
                    <p className="mt-1 text-sm font-medium leading-snug text-zinc-800 dark:text-zinc-100">
                      {ev.title}
                    </p>
                    <p className="text-xs text-violet-600 dark:text-violet-400">
                      {ev.time}
                    </p>
                  </div>
                ))}
              </div>

              <div className="px-5 py-4">
                <Link
                  href="/calendar"
                  className="flex w-full items-center justify-center rounded-full bg-violet-600 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-violet-700"
                >
                  View Full Calendar
                </Link>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}

function NewsCard({
  title,
  body,
  tag,
}: {
  title: string;
  body: string;
  tag: string;
}) {
  return (
    <div className="rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
      <span className="inline-block rounded-full bg-violet-50 px-2.5 py-0.5 text-xs font-medium text-violet-600 dark:bg-violet-950 dark:text-violet-300">
        {tag}
      </span>
      <h3 className="mt-2 text-sm font-semibold text-zinc-900 dark:text-zinc-50">
        {title}
      </h3>
      <p className="mt-1 text-xs leading-relaxed text-zinc-500 dark:text-zinc-400">
        {body}
      </p>
    </div>
  );
}
