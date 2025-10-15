import axios from "axios";

// @ts-ignore
const API_BASE = window.RUNTIME_CONFIG?.API_URL || "/api";

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

export async function fetchStats() {
  const res = await fetch(`${API_BASE}/stats`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}

export async function fetchTopJobs() {
  const res = await fetch(`${API_BASE}/top_jobs`);
  if (!res.ok) throw new Error("Failed to fetch top jobs");
  return res.json();
}

