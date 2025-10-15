from bs4 import BeautifulSoup
from typing import List, Dict, Any
from backend.utils import safe_get
from backend.config import STRIPE_URL, FILTER_KEYWORDS
from backend.logger import logger


def scrape_stripe() -> List[Dict[str, Any]]:
    logger.debug(f"Scraping Stripe: {STRIPE_URL}")
    r = safe_get(STRIPE_URL)
    if not r:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    jobs: List[Dict[str, Any]] = []

    # Each job is inside a <tr class="TableRow">
    for row in soup.select("tbody.JobsListings__tableBody tr.TableRow"):
        # Extract link and title
        link_tag = row.select_one("a.JobsListings__link")
        if not link_tag:
            continue
        link = link_tag.get("href")
        if not link:
            continue
        if not link.startswith("http"):
            link = f"https://stripe.com{link}"
        title = link_tag.get_text(strip=True)

        # Filter out unwanted keywords
        if any(k.lower() in title.lower() for k in FILTER_KEYWORDS):
            continue

        # Extract team (category)
        team_cell = row.select_one(".JobsListings__tableCell--departments li")
        category = team_cell.get_text(strip=True) if team_cell else "Unknown"

        # Extract location
        location_span = row.select_one(".JobsListings__locationDisplayName")
        location = location_span.get_text(strip=True) if location_span else "Unknown"

        # Avoid duplicates
        if not any(link == j.get("link") for j in jobs):
            jobs.append({
                "title": title,
                "link": link,
                "site": "stripe",
                "location": location,
                "category": category
            })

    logger.debug(f"[Stripe] job listings found: {len(jobs)}")
    return jobs

