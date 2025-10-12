import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export async function fetchJobs() {
  const res = await fetch(`${API_BASE}/jobs`);
  if (!res.ok) throw new Error("Network response was not ok");
  return res.json();
}

export async function fetchLogs(lines?: number) {
  const res = await fetch(`${API_BASE}/logs?lines=${lines ?? 500}`);
  if (!res.ok) throw new Error("Network response was not ok");
  return res.text(); // fetch as plain text
}
