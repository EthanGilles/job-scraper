from bs4 import BeautifulSoup
from typing import List, Dict, Any
from backend.utils import safe_get
from backend.config import DIGITALOCEAN_URL, FILTER_KEYWORDS
from backend.logger import logger

def scrape_digitalocean():
    url = DIGITALOCEAN_URL # Found an embedded API and using my requests info for my session to get the JSON from it.
    logger.debug(f"Scraping DigitalOcean (Greenhouse embed API): {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Origin": "https://www.digitalocean.com",
        "Referer": "https://www.digitalocean.com/careers/open-roles?location=Denver",
        "Accept": "*/*"
    }

    r = safe_get(url, headers=headers)
    data = r.json()
    jobs: list[dict[str, str]] = []

    for department in data.get("departments", []):
        for job in department.get("jobs", []):
            title = job.get("title")
            location_name = job.get("location", {}).get("name", "")
            link = job.get("absolute_url")

            if not title or not link:
                continue

            if not any(city in location_name.lower() for city in ["denver", "seattle", "boston", "austin"]):
                continue

            department_name = ""
            for meta in job.get("metadata", []):
                if meta.get("name") == "Career Page Grouping":
                    department_name = meta.get("value") or ""
                    break

            if not any(dept in department_name for dept in ["AI, Engineering & Technology", "Security"]):
                continue

            # Filter out unwanted keywords
            if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
                continue

            # Avoid duplicates
            if not any(link == j.get("link") for j in jobs):
                jobs.append({
                    "title": title,
                    "location": location_name,
                    "link": link,
                    "category": department_name,
                    "site": "digitalocean"
                })

    logger.debug(f"[DigitalOcean] job listings found: {len(jobs)}")
    return jobs
