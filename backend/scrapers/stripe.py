from bs4 import BeautifulSoup
from typing import List, Dict, Any
from backend.utils import safe_get
from backend.config import STRIPE_URL, FILTER_KEYWORDS
from backend.logger import logger

def scrape_stripe() -> List[Dict[str, Any]]:
    logger.info(f"Scraping Stripe: {STRIPE_URL}")
    r = safe_get(STRIPE_URL)
    if not r:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    jobs: List[Dict[str, Any]] = []

    for a in soup.select("a.JobsListings__link"):
        href = a.get("href")
        if not href:
            continue
        title = a.get_text(strip=True)
        if not title:
            continue
        if any(k.lower() in title.lower() for k in FILTER_KEYWORDS):
            continue
        link = href if href.startswith("http") else f"https://stripe.com{href}"
        if not any(link == j.get("link") for j in jobs):
            jobs.append({"title": title, "link": link, "site": "stripe"})
    logger.info(f"[Stripe] job listings found: {len(jobs)}")
    return jobs

