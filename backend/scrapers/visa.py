import requests
from typing import List, Dict, Any
from backend.utils import safe_get
from backend.config import FILTER_KEYWORDS, VISA_URL
from backend.logger import logger

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

FILTER_DEPARTMENTS = [
    "Risk", 
    "Finance/Accounting", 
    "Administrative", 
    "Sales", 
    "Customer Service", 
    "Client Services", 
    "Risk & Security", 
    "Legal & Compliance", 
    "Client Consulting", 
    "Strategy & Planning", 
    "Marketing & Communications", 
    "Business Development", 
    "Data Science/Data Engineering", 
    "Human Resources", 
]

def fetch_visa_page(page: int = 1, page_size: int = 1000) -> Dict[str, Any]:
    payload = {
        "page": page,
        "pageSize": page_size,
        "q": ""
    }
    response = requests.post(VISA_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def scrape_visa() -> List[Dict[str, str]]:
    logger.debug("Scraping Visa jobs from API")

    page = 1
    page_size = 1000
    jobs: List[Dict[str, str]] = []

    while True:
        data = fetch_visa_page(page, page_size)

        job_list = data.get("jobDetails", [])
        if not job_list:
            break

        for job in job_list:
            title = job.get("jobTitle", "").strip()
            link = job.get("applyUrl", "")
            location = f"{job.get('city', '')}, {job.get('region', '')}, {job.get('country', '')}"
            department = job.get("department", "")
            created = job.get("createdOn", "")

            if not title or not link:
                continue

            if "United States" not in job.get("country", ""):
                continue

            if any(k.lower() in title.lower() for k in FILTER_KEYWORDS):
                continue

            if any(dept in department for dept in FILTER_DEPARTMENTS):
                continue

            jobs.append({
                "title": title,
                "location": location,
                "link": link,
                "category": department,
                "site": "visa",
                "posted": created,
            })

        logger.debug(f"[Visa] Page {page}: Retrieved {len(job_list)} jobs")

        total = data.get("recordsMatched", 0)
        if page * page_size >= total:
            break

        page += 1

    logger.debug(f"[Visa] Total jobs stored: {len(jobs)}")
    return jobs
