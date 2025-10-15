from typing import List
from backend.logger import logger
from backend.config import FILTER_KEYWORDS, DATADOG_URL
import requests

def scrape_datadog() -> List[dict[str, str]]:
    logger.debug(f"Scraping Datadog careers API: {DATADOG_URL}")

    r = safe_get(DATADOG_URL)
    data = r.json()
    all_jobs = []

    for job in data.get("jobs", []):
        title = job.get("title", "")
        location = job.get("location", {}).get("name", "")
        link = job.get("absolute_url")
        metadata = job.get("metadata", [])

        # --- Extract relevant metadata safely ---
        area = ""
        early_career = ""
        cost_center = ""
        for meta in metadata:
            val = meta.get("value")
            if val is not None:
                val = str(val).strip()
            else:
                val = ""

            if meta.get("name") == "Area - Engineering":
                area = val
            elif meta.get("name") == "Early Career Time Type":
                early_career = val
            elif meta.get("name") == "Cost Center":
                cost_center = val

        # --- Filter by Engineering OR Early Career/Internship OR Professional Services ---
        if not (
            (area and "engineering" in area.lower()) or
            (early_career and early_career.lower() in ["internship", "early career"]) or
            (cost_center and "professional services" in cost_center.lower())
        ):
            continue

        # --- Only include jobs in the USA ---
        if not any(c in location.lower() for c in ["usa", "united states"]):
            continue

        # --- Filter out bad titles / links / duplicates / keywords ---
        if not title or not link:
            continue
        if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
            continue
        if any(link == j.get("link") for j in all_jobs):
            continue

        all_jobs.append({
            "title": title,
            "category": area or cost_center or "Engineering",
            "location": location,
            "link": link,
            "site": "datadog"
        })

    logger.debug(f"[Datadog] US Engineering / Early Career / Professional Services jobs found: {len(all_jobs)}")
    return all_jobs

