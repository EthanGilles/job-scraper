# JobWatch &nbsp;![Version](https://img.shields.io/badge/version-0.8.6-blue?style=for-the-badge)
> Automated job scraper and monitoring dashboard 
for tracking new software roles at select companies.

---
## Frontend Screenshots
#### Dashboard View                                
![Dashboard Screenshot](https://github.com/EthanGilles/EthanGilles/blob/6e1a3fea0e881e49888331ece1bfaa0ae46db1ce/pics/jobwatchhome.png) 

#### Job Cards
![Job Cards Screenshot](https://github.com/EthanGilles/EthanGilles/blob/6e1a3fea0e881e49888331ece1bfaa0ae46db1ce/pics/jobwatchjobs.png)

---
## Overview
JobWatch is a full-stack automated job monitoring system that scrapes multiple 
company career pages for new software related roles and provides real-time 
visibility through both email alerts and a web dashboard.

The backend service scrapes and stores job listings, logs activity, and 
exposes an API. The frontend dashboard visualizes current job postings, logs, 
and metrics, enabling users to track scrapes and view company-specific
listings in a clean, interactive interface.

---
## Features
**Scraper**
- Gathers jobs from multiple companies:
    - Stripe
    - Plaid
    - DigitalOcean
    - Atlassian
- Filters out roles containing unwanted keywords like “Senior,” “Manager,” or “PhD.”
- Maintains a record of seen jobs in jobs_seen.json
- Runs continuously or manually, scraping 3× daily (8AM, 12PM, 5PM)
- Sends summary emails for newly discovered jobs only
- Uses .env for secure credential management
**Backend (FastAPI)**
- Exposes endpoints for:
    - /jobs → Retrieve current job data (JSON)
    - /logs → Retrieve recent scrape logs
    - Provides Prometheus metrics (scrape count, duration, job totals)
    - Supports integration with monitoring dashboards (Grafana, Prometheus)
**Frontend (React + Vite)**
- Dynamic dashboard showing:
    - Job listings organized by company
    - Real-time logs from backend
    - Scraping metrics and statistics
    - Smooth carousel view for company cards
- Built with React Query, Framer Motion, and Tailwind CSS

---
## Tech Stack
| Layer | Technologies |
|-------|---------------|
| **Frontend** | React, Vite, Tailwind CSS, React Query |
| **Backend** | FastAPI, Uvicorn, BeautifulSoup, Loguru, Requests |
| **Email** | Gmail SMTP, python-dotenv |
| **Monitoring** | Prometheus metric endpoint |

---
## Requirements

**Python Backend:**

Python Version:
- Python 3.9+

**Dependencies**:
```
pip install -r requirements.txt
```

**Frontend**:

Node.js Version:
- Node 18+

**Dependencies**:
```bash
npm install react react-dom @tanstack/react-query framer-motion lucide-react tailwindcss @fontsource/rubik
```

---
## Setup

1. Clone the repo

```bash
git clone https://github.com/EthanGilles/job-scraper.git
cd job-scraper
```

2. Create environment variables

Create a .env file in the backend folder (this keeps your credentials out of Git)
```bash
touch ./backend/.env
```

Add the following:
```
GMAIL_SENDER="youremail@gmail.com"
GMAIL_PASSWD="yourapppassword"
ALERT_RECIPIENT="youremail@gmail.com"
```
> You must create an App Password in your Google Account if you use 2FA.

3. Run the backend
```bash
python -m backend.main
```

4. Run the frontend
```bash
cd frontend
npm start
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
## Monitoring and metrics
JobWatch exposes Prometheus metrics such as:
- job_scrapes_total → Total scrapes executed
- job_scrape_duration_seconds → Scrape duration histogram
- job_scrapes_created → Latest scrape timestamp
Integrate with Prometheus or Grafana for real-time monitoring.

---
