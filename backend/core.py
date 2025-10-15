# backend/jobs.py
from backend.utils import load_seen, save_seen
from backend.scrapers import SCRAPERS
from backend.logger import logger
from backend.alert import alert, find_new_jobs_for_site

def run_check_once():
    logger.debug("Starting job check")
    seen = load_seen()
    all_new = {}
    any_error = False

    for site, fn in SCRAPERS.items():
        try:
            jobs = fn()
            newjobs = find_new_jobs_for_site(site, jobs, seen)
            all_new[site] = newjobs
            logger.info(f"[{site}] total found {len(jobs)}, new {len(newjobs)}")
        except Exception as e:
            logger.exception(f"[Scrape] Error scraping {site}: {e}")
            all_new[site] = []
            any_error = True

    try:
        alert(all_new)
    except Exception as e:
        logger.exception(f"[Email] Error sending alert: {e}")

    try:
        save_seen(seen)
    except Exception as e:
        logger.exception(f"[State] Failed to save seen state: {e}")

    if any_error:
        logger.warning("[Scrape] Some scrapes failed this run; check logs.")
