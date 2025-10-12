#!/usr/bin/env python3

from __future__ import annotations
import argparse
import json
import time
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import schedule
import sys
from typing import List, Dict, Any
from loguru import logger
import unicodedata
import smtplib
from dotenv import load_dotenv
import os

# config
DESCRIPTION = """
milestone1.py

Scrapes the following careers pages:
Stripe, Plaid, and DigitalOcean 

Keeps track of previously seen jobs in jobs_seen.json 
Alerts three times daily when new jobs appear.

Dependencies:
    pip install requests beautifulsoup4 schedule dotenv

Usage:
    python milestone1.py         # Runs continuously and checks 8AM, 12PM and 5PM local time
    python milestone1.py --once  # Runs a single check immediately and quits 
"""

DATA_FILE = Path("jobs_seen.json")

PLAID_URL = "https://plaid.com/careers/?department=Engineering#search"
DIGITALOCEAN_URL = "https://api.greenhouse.io/v1/boards/digitalocean98/embed/departments" # Greenhouse API that returns a JSON with their job postings.
STRIPE_URL = "https://stripe.com/jobs/search?teams=Infrastructure+%26+Corporate+Tech&teams=University&office_locations=North+America--Atlanta&office_locations=North+America--Chicago&office_locations=North+America--New+York&office_locations=North+America--New+York+Privy+HQ&office_locations=North+America--San+Francisco+Bridge+HQ&office_locations=North+America--Seattle&office_locations=North+America--South+San+Francisco&office_locations=North+America--Washington+DC"
ATLASSIAN_URL = "https://www.atlassian.com/endpoint/careers/listings"

FILTER_KEYWORDS = ["PhD", "Senior", "Staff", "Product", "Program", "Manager", "Principal", "Director", "Principle", "Head", "Distinguished"]


GMAIL_SENDER = os.getenv("GMAIL_SENDER")
GMAIL_PASSWD = os.getenv("GMAIL_PASSWD")
ALERT_RECIPIENT = os.getenv("ALERT_RECIPIENT")

REQUEST_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (compatible; JobAlertBot/1.0; +https://example.com/)"

# logging config
logger.remove()  # clear default
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")

# state handling
def load_seen():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception as ex:
            logger.warning(f"Failed to read jobs_seen.json; starting fresh {ex}")
    return {}

def save_seen(data: Dict[str, List[str]]) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    logger.debug(f"Saved seen state to {DATA_FILE}")

# HTTP & parsing
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

def safe_get(url: str, **kwargs):
    try:
        r = session.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
        r.raise_for_status()
        return r
    except Exception as e:
        logger.error(f"Request failed for {url}: {e}")
        return None

# scrapers (one per site)
def scrape_stripe():
    logger.info(f"Scraping Stripe: {STRIPE_URL}")

    r = safe_get(STRIPE_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    jobs: List[Dict[str, Any]] = []

    # Use CSS selector for job links
    for a in soup.select("a.JobsListings__link"):
        href = a.get("href")
        if not href:
            continue
        title = a.get_text(strip=True)
        if not title:
            continue

        # skip jobs that have any of the keywords
        if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
            continue

        link = href if href.startswith("http") else ("https://stripe.com" + href)

        # Stripe gives duplicates so this avoids it
        if not any(link == j.get("link") for j in jobs):
            jobs.append({"title": title, "link": link, "site": "stripe"})

    logger.info(f"[Stripe] job listings found: {len(jobs)}")
    return jobs

def scrape_plaid():
    url = PLAID_URL
    logger.info(f"Scraping Plaid: {url}")
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
            jobs.append({"title": title, "location": location, "link": link, "site": "plaid"})

    logger.info(f"[Plaid] job listings found: {len(jobs)}")
    return jobs

def scrape_digitalocean():
    url = DIGITALOCEAN_URL # Found an embedded API and using my requests info for my session to get the JSON from it.
    logger.info(f"Scraping DigitalOcean (Greenhouse embed API): {url}")

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

            # Only include Denver jobs
            if "denver" not in location_name.lower():
                continue

            # Only include jobs in AI, Engineering & Technology
            department_name = ""
            for meta in job.get("metadata", []):
                if meta.get("name") == "Career Page Grouping":
                    department_name = meta.get("value", "")
                    break

            if "AI, Engineering & Technology" not in department_name:
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
                    "department": department_name,
                    "site": "digitalocean"
                })

    logger.info(f"[DigitalOcean] job listings found: {len(jobs)}")
    return jobs

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
        loc_ok = any(("united states" in loc.lower()) or ("remote" in loc.lower()) for loc in locations)
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


SCRAPERS = {
    "stripe": scrape_stripe,
    "plaid": scrape_plaid,
    "digitalocean": scrape_digitalocean,
    "atlassian": scrape_atlassian
}

# comparison
def find_new_jobs_for_site(site: str, jobs: List[Dict[str, Any]], seen_store: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    seen_links = set(seen_store.get(site, []))
    new: List[Dict[str, Any]] = []
    for j in jobs:
        link = (j.get("link") or "").strip()
        title = (j.get("title") or "").strip()
        unique_id = link or title
        if not unique_id:
            continue
        if unique_id not in seen_links:
            new.append(j)
    if new:
        seen_store.setdefault(site, [])
        for j in new:
            uid = (j.get("link") or j.get("title") or "").strip()
            if uid and uid not in seen_store[site]:
                seen_store[site].append(uid)
    return new


def emailer(recpt, subject, mesg):
    def to_ascii(s: str) -> str:
        # Normalize and strip any non-ASCII characters
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")

    TO = to_ascii(recpt)
    SUBJECT = to_ascii(subject)
    TEXT = to_ascii(mesg)
    BODY = f"To: {TO}\r\nFrom: {GMAIL_SENDER}\r\nSubject: {SUBJECT}\r\n{TEXT}"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        server.ehlo()
        server.starttls()
        server.login(GMAIL_SENDER, GMAIL_PASSWD)

        server.sendmail(GMAIL_SENDER, TO, BODY)
        logger.info(f"Email sent to {ALERT_RECIPIENT}")
    except Exception as e:
        logger.exception(f"Error sending email: {e}")
    finally:
        try:
            server.quit()
        except Exception:
            pass

def alert(all_new: Dict[str, List[Dict[str, Any]]]):
    if not any(all_new.values()):
        logger.info("No new jobs to email.")
        return

    # Count totals
    total_new = sum(len(jobs) for jobs in all_new.values() if jobs)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Build email content
    lines: List[str] = []
    lines.append("=" * 50)
    lines.append(f"Total new jobs found: {total_new}")
    lines.append("=" * 50)
    lines.append("")  # spacer line before details

    # Add job details by site
    for site, jobs in all_new.items():
        if not jobs:
            continue
        lines.append(f"{site.title()} - {len(jobs)} new job(s)")
        for j in jobs:
            title = j.get("title", "Untitled")
            link = j.get("link", "")
            lines.append(f"- {title} -> {link}")
        lines.append("")  # blank line between sections

    # Join all lines
    message = "\n".join(lines)

    # Subject line includes total
    subject = f"Job Alert ({total_new} new job{'s' if total_new != 1 else ''}) - {timestamp}"

    # Send email
    emailer(ALERT_RECIPIENT, subject, message)
    logger.info(f"Sent email with {total_new} total new jobs.")

# check routine
def run_check_once() -> None:
    logger.info("Starting job check")
    seen = load_seen()
    all_new: Dict[str, List[Dict[str, Any]]] = {}
    any_error = False

    for site, fn in SCRAPERS.items():
        try:
            jobs = fn()
            newjobs = find_new_jobs_for_site(site, jobs, seen)
            all_new[site] = newjobs
            logger.info(f"Site {site}: total found {len(jobs)}, new {len(newjobs)}", site, len(jobs), len(newjobs))
        except Exception as e:
            logger.exception(f"Error scraping {site}: {e}")
            all_new[site] = []
            any_error = True

    try:
        alert(all_new)
    except Exception as e:
        logger.exception(f"Error sending alert: {e}")

    try:
        save_seen(seen)
    except Exception as e:
        logger.exception(f"Failed to save seen state: {e}")

    if any_error:
        logger.warning("Some scrapes failed this run; check logs.")

def start_scheduler():
    schedule.every().day.at("08:00").do(run_check_once)
    schedule.every().day.at("12:00").do(run_check_once)
    schedule.every().day.at("17:00").do(run_check_once)
    logger.info("Scheduler started. Will run at 8AM, 12PM and 7PM local time.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Shutting down on user interrupt.")

# entrypoint
def main():
    load_dotenv()  # Loads from .env by default
    parser = argparse.ArgumentParser(description=DESCRIPTION,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--once", action="store_true", help="Run one check immediately and exit (useful for testing)")
    args = parser.parse_args()

    if args.once:
        run_check_once()
        return

    run_check_once()
    start_scheduler()

if __name__ == "__main__":
    main()
