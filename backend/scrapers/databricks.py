from typing import List, Dict
from backend.utils import safe_get
from backend.config import FILTER_KEYWORDS, DATBRICKS_URL
from backend.logger import logger

EXCLUDE_DEPARTMENTS = [
    "Business Development",
    "Customer Success",
    "People and HR",
    "Product",
    "Professional Services",
    "Recruiting",
    "Research",
    "Sales",
    "Exec Sales Enablement",
    "Sales Development",
    "Legal",
    "Administration",
    "Go To Market",
]

# Cities we want to include
INCLUDE_CITIES = [
    "san francisco",
    "mountain view",
    "boston",
    "bellevue",
    "new york city",
    "new york",
    "seattle",
    "northeast - united states"
    "westcoast - united states"
    "central - united states"
    "united states"
    "remote"
]

def scrape_databricks():
    url = DATBRICKS_URL
    logger.debug(f"Scraping Databricks (Greenhouse embed API): {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Origin": "https://www.databricks.com",
        "Referer": "https://www.databricks.com/company/careers/open-positions",
        "Accept": "*/*"
    }

    r = safe_get(url, headers=headers)
    data = r.json()
    jobs: list[dict[str, str]] = []

    departments = data.get("result", {}).get("pageContext", {}).get("data", {}).get("allGreenhouseDepartment", {}).get("nodes", [])
    for department in departments:
        department_name = department.get("name", "")
        if department_name in EXCLUDE_DEPARTMENTS:
            continue  # skip excluded departments

        for job in department.get("jobs", []):
            title = job.get("title")
            location_name = job.get("location", {}).get("name", "")
            link = job.get("absolute_url")

            if not title or not link:
                continue

            # Include only jobs in the specified cities
            if not any(city in location_name.lower() for city in INCLUDE_CITIES):
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
                    "site": "databricks"
                })

    logger.debug(f"[Databricks] job listings found: {len(jobs)}")
    return jobs

