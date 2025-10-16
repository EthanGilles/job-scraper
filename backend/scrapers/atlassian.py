from typing import List
from backend.utils import safe_get
from backend.config import ATLASSIAN_URL, FILTER_KEYWORDS
from backend.logger import logger
import re

def format_location(locations: list[str]) -> str:
    """Format Atlassian locations into a single clean location string."""
    if not locations:
        return ""

    first_loc = next((loc for loc in locations if "remote" not in loc.lower()), locations[0])
    first_clean = re.split(r"[-,]", first_loc)[0].strip()
    first_clean = re.sub(r"\bUnited States\b", "", first_clean, flags=re.IGNORECASE)
    first_clean = re.sub(r"\d{5}", "", first_clean)
    first_clean = re.sub(r"\s{2,}", " ", first_clean).strip()

    words = first_clean.split()
    if len(words) == 2 and words[0] == words[1]:
        first_clean = words[0]

    has_remote = any("remote" in loc.lower() for loc in locations)
    if has_remote and "remote" not in first_clean.lower():
        return f"{first_clean} or Remote"

    return first_clean


def scrape_atlassian():
    logger.debug(f"Scraping Atlassian API: {ATLASSIAN_URL}")
    url = ATLASSIAN_URL
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "referer": "https://www.atlassian.com/company/careers/all-jobs"
    }

    r = safe_get(url, headers=headers)
    data = r.json()
    jobs: list[dict[str, str]] = []
    categories = ["engineering", "interns", "graduates", "site reliability engineering"]

    for job in data:
        title = job.get("title", "").strip()
        category = job.get("category", "").strip()
        locations = job.get("locations", []) or []
        link = job.get("portalJobPost", {}).get("portalUrl")

        if "Canada" in title:
            continue
        if not title or not locations:
            continue
        if category.lower() not in categories:
            continue
        if not any("united states" in loc.lower() for loc in locations):
            continue
        if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
            continue
        if any(link == j.get("link") for j in jobs):
            continue

        formatted_location = format_location(locations)

        jobs.append({
            "title": title,
            "category": category,
            "location": formatted_location,
            "link": link,
            "site": "atlassian"
        })

    logger.debug(f"[Atlassian] Engineering jobs in US/Remote found: {len(jobs)}")
    return jobs
