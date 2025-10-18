from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

DESCRIPTION = """
Job Scraper

Scrapes the following careers pages:
Stripe, Plaid, DigitalOcean, Atlassian

Keeps track of previously seen jobs in jobs-seen.json
Alerts three times daily when new jobs appear.
"""

DATA_FILE = Path("/app/data/jobs-seen.json")
LOG_FILE = Path("/app/data/logs/job-scraper.log")

PLAID_URL = "https://plaid.com/careers/?department=Engineering#search"
DIGITALOCEAN_URL = "https://api.greenhouse.io/v1/boards/digitalocean98/embed/departments"
STRIPE_URL = "https://stripe.com/jobs/search?teams=Infrastructure+%26+Corporate+Tech&teams=University&office_locations=North+America--Atlanta&office_locations=North+America--Chicago&office_locations=North+America--New+York&office_locations=North+America--New+York+Privy+HQ&office_locations=North+America--San+Francisco+Bridge+HQ&office_locations=North+America--Seattle&office_locations=North+America--South+San+Francisco&office_locations=North+America--Washington+DC"
ATLASSIAN_URL = "https://www.atlassian.com/endpoint/careers/listings"
DATADOG_URL = "https://api.greenhouse.io/v1/boards/datadog/jobs"

FILTER_KEYWORDS = ["PhD", "Senior", "Staff", "Product", "Program", "Manager", 
                   "Principal", "Director", "Principle", "Head", "Distinguished",
                   "Marketing", "Accounting", "Salesforce", "Account", "CTO",
                   "Sr", ]

GMAIL_SENDER = os.getenv("GMAIL_SENDER")
GMAIL_PASSWD = os.getenv("GMAIL_PASSWD")
ALERT_RECIPIENT = os.getenv("ALERT_RECIPIENT")

USER_AGENT = "Mozilla/5.0 (compatible; JobAlertBot/1.0; +https://example.com/)"

