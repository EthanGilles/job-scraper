from bs4 import BeautifulSoup
from typing import List, Dict, Any
from backend.utils import safe_get
from backend.config import ATLASSIAN_URL, FILTER_KEYWORDS
from backend.logger import logger

def scrape_atlassian():
    logger.info(f"Scraping Atlassian API: {ATLASSIAN_URL}")
    url = ATLASSIAN_URL
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "referer": "https://www.atlassian.com/company/careers/all-jobs"
    }

    r = safe_get(url, headers=headers)
    data = r.json()
    jobs: list[dict[str, str]] = []
    categories = ["engineering", "interns", "graduates"]

    for i, job in enumerate(data):
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
        loc_ok = any(("united states" in loc.lower()) for loc in locations)
        if not loc_ok:
            continue
        if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
            continue
        if not link:
            logger.warning(f"[Atlassian] Skipping job with no apply link: {title} | locations={locations}")
            continue
        if any(link == j.get("link") for j in jobs):
            continue

        jobs.append({
            "title": title,
            "category": category,
            "locations": locations,
            "link": link,          
            "site": "atlassian"
        })

    logger.info(f"[Atlassian] Engineering jobs in US/Remote found: {len(jobs)}")
    return jobs
