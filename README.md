# Job Scraper
milestone1.py is an automated job alert script that scrapes multiple company 
career pages new engineering-related roles and sends you an email notification 
when new jobs appear.

It runs either once for testing or continuously, checking three times a 
day (8AM, 12PM, and 5PM local time).

---
## Features
- Scrapes jobs from:
    - Stripe
    - Plaid
    - DigitalOcean
    - Atlassian
- Filters out roles containing unwanted keywords like “Senior”, “Manager”, or “PhD”.
- Keeps track of previously seen jobs in a local jobs_seen.json file.
- Sends a summary email listing only new roles since the last run.
- Supports manual runs or scheduled runs 3× daily.
- Uses .env for secure email credentials.

---
## Requirements

**Python Version:**
- Python 3.9+

**Dependencies**
Install all required packages with:

```bash
pip install requests beautifulsoup4 schedule python-dotenv loguru
```

