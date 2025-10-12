from typing import Dict, List
from datetime import datetime
import unicodedata
import smtplib
from backend.config import GMAIL_SENDER, GMAIL_PASSWD, ALERT_RECIPIENT
from backend.logger import logger

def find_new_jobs_for_site(site: str, jobs: List[Dict], seen_store: Dict[str, List[Dict]]) -> List[Dict]:
    seen_jobs = seen_store.get(site, [])
    seen_links = set(j.get("link") for j in seen_jobs if "link" in j)
    new: List[Dict] = []

    for j in jobs:
        link = (j.get("link") or "").strip()
        if not link:
            continue
        if link not in seen_links:
            new.append(j)

    if new:
        seen_store.setdefault(site, [])
        for j in new:
            if not any(j.get("link") == existing.get("link") for existing in seen_store[site]):
                seen_store[site].append(j)
    return new

def emailer(recpt, subject, mesg):
    def to_ascii(s: str) -> str:
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")

    TO = to_ascii(recpt)
    BODY = f"To: {TO}\r\nFrom: {GMAIL_SENDER}\r\nSubject: {to_ascii(subject)}\r\n{to_ascii(mesg)}"
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
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

def alert(all_new: Dict[str, List[Dict]]):
    if not any(all_new.values()):
        logger.info("No new jobs to email.")
        return
    total_new = sum(len(jobs) for jobs in all_new.values() if jobs)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = ["="*50, f"Total new jobs found: {total_new}", "="*50, ""]
    for site, jobs in all_new.items():
        if not jobs:
            continue
        lines.append(f"{site.title()} - {len(jobs)} new job(s)")
        for j in jobs:
            lines.append(f"- {j.get('title','Untitled')} -> {j.get('link','')}")
        lines.append("")
    message = "\n".join(lines)
    subject = f"Job Alert ({total_new} new job{'s' if total_new != 1 else ''}) - {timestamp}"
    emailer(ALERT_RECIPIENT, subject, message)
    logger.info(f"Sent email with {total_new} total new jobs.")
