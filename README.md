# Job Scraper
Assignment for CSCI 5020: Fundementals of Network Engineering at the 
University of Colorado Boulder Network Engineering Masters.

job-scraper.py is an automated job alert script that scrapes multiple company 
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

Or install using the requirements file 
```
pip install requirements.txt
```
---
## Setup
Clone or copy this script

```bash
git clone https://github.com/EthanGilles/job-alert-scraper.git
cd job-alert-scraper
```

Create a .env file (this keeps your credentials out of Git)
```bash
touch .env
```

Add the following:
```
GMAIL_SENDER="youremail@gmail.com"
GMAIL_PASSWD="yourapppassword"
ALERT_RECIPIENT="youremail@gmail.com"
```

**Important:**
You must create an App Password in your Google Account if you use 2FA.

---
## Usage

**Run continuously**
Checks at 8 AM, 12 PM, and 5 PM local time every day:
```bash
python job-scraper.py
```

**Run once**
Checks immediately and exits (useful for testing):
```bash
python job-scraper.py --once
```
---
## Emails
When new jobs are found, you’ll receive an email like:

```
==================================================
Total new jobs found: 5
==================================================

Stripe - 2 new job(s)
- Backend Engineer, Core Technology -> https://stripe.com/jobs/listing/backend-engineer-core-technology/6042172
- Infrastructure Engineer -> https://stripe.com/jobs/listing/infrastructure-engineer/6210391

Plaid - 3 new job(s)
- Software Engineer, Systems -> https://plaid.com/careers/openings/software-engineer-systems
- ...
```

---

