from bs4 import BeautifulSoup
from typing import List, Dict, Any
from backend.utils import safe_get
from backend.config import PLAID_URL, FILTER_KEYWORDS
from backend.logger import logger

def scrape_plaid():
    url = PLAID_URL
    logger.debug(f"Scraping Plaid: {url}")
    r = safe_get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    jobs: List[Dict[str, str]] = []

    # Each job container
    for job_div in soup.find_all("div", class_="MuiStack-root"):
        # Use CSS tags on the page to find the title and loction
        title_tag = job_div.find("p", class_="css-kluxnl")
        loc_tag = job_div.find("p", class_="css-kj1jcl")

        a_tag = job_div.find("a", href=True)

        if not title_tag or not loc_tag or not a_tag:
            continue

        title = title_tag.get_text(strip=True)
        location = loc_tag.get_text(strip=True)
        href = a_tag["href"]

        # Filter for engineering roles
        if "engineering" not in href.lower():
            continue

        # Filter out unwanted keywords
        if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
            continue

        link = href if href.startswith("http") else f"https://plaid.com{href}"

        # filter dupes
        if not any(link == j.get("link") for j in jobs):
            jobs.append({"title": title, "location": location, "link": link, "category": "Engineering", "site": "plaid"})

    logger.debug(f"[Plaid] job listings found: {len(jobs)}")
    return jobs
