import { DancerEvent } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function fetchDancerEvents(): Promise<DancerEvent[]> {
  const res = await fetch(`${API_BASE}/api/events`);
  if (!res.ok) {
    throw new Error(`Failed to load events: ${res.status}`);
  }
  return res.json();
}

export function icsDownloadUrl(): string {
  return `${API_BASE}/api/ics`;
}
