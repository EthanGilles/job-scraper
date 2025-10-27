# JobWatch &nbsp;![Version](https://img.shields.io/badge/version-0.9.9-blue?style=for-the-badge)
> Automated job scraper and monitoring dashboard 
for tracking new software roles at select companies.

[My Self Hosted Instance](https://jobwatch.ethan-fullstack.dev/)

---
## Frontend Screenshots
#### Dashboard View                                
![Dashboard Screenshot](https://github.com/EthanGilles/EthanGilles/blob/578a52d47ece3e59ee4f7f5a846b31b728556cdc/pics/jobwatchhome.png) 

#### Job Cards
![Job Cards Screenshot](https://github.com/EthanGilles/EthanGilles/blob/578a52d47ece3e59ee4f7f5a846b31b728556cdc/pics/jobwatchjobs.png)

---
## Overview
JobWatch is a full-stack automated job monitoring system that scrapes multiple 
company career pages for new software related roles and provides real-time 
visibility through both email alerts and a web dashboard.

The backend service scrapes and stores job listings, logs activity, and 
exposes an API. The frontend dashboard visualizes current job postings, logs, 
and metrics, enabling users to track scrapes and view company-specific
listings in a clean, interactive interface.

Currently I have this application deployed on my Kubernetes homelab. 
All of my [deployment manifests](https://github.com/EthanGilles/kube-homelab/tree/main/clusters/home/apps/jobwatch) are managed by FluxCD.
In my cluster, JobWatch is monitored by Prometheus using a ServiceMonitor. 
A Grafana dashboard for this application is a WIP.

---
## Features
**Scraper**
- Gathers jobs from multiple companies:
    - Stripe
    - Plaid
    - DigitalOcean
    - Atlassian
    - Datadog
    - Databricks
    - Visa
- Filters out roles containing unwanted keywords like “Senior,” “Manager,” or “PhD.”
- Maintains a record of seen jobs in jobs_seen.json
- Runs continuously or manually, scraping 3× daily (8AM, 12PM, 5PM)
- Sends summary emails for newly discovered jobs only
- Uses .env for secure credential management
**Backend (FastAPI)**
- Exposes endpoints for:
    - /jobs →  Retrieve current job data (JSON)
    - /logs →  Retrieve recent scrape logs
    - /metrics -> Provides Prometheus metrics (scrape count, duration, job totals, API metrics)
    - /top_jobs-> Retrieve current jobs with an even more strict filter
    - /health -> Provides an endpoint for Kubernetes liveness probes
**Frontend (React + Vite)**
- Dynamic dashboard showing:
    - Job listings organized by company
    - Real-time logs from backend
    - Scraping metrics and statistics
- Built with React Query, Framer Motion, and Tailwind CSS

---
## Tech Stack
| Layer | Technologies |
|-------|---------------|
| **Frontend** | React, Vite, Tailwind CSS, React Query |
| **Backend** | FastAPI, Uvicorn, BeautifulSoup, Loguru, Requests |
| **Email** | Gmail SMTP, python-dotenv |
| **Monitoring** | Prometheus metrics endpoint |
| **Deployment** | Dockerfiles and dockercompose for local containerized testing. Kubernetes for the actual deployment |


---
## Local Testing/Setup

1. Clone the repo

```bash
git clone https://github.com/EthanGilles/job-scraper.git
cd job-scraper
```

2. Create environment variables

Create a .env file in the backend folder (this keeps your credentials out of Git)
```bash
touch backend/.env
```

Add the following:
```
GMAIL_SENDER="youremail@gmail.com"
GMAIL_PASSWD="yourapppassword"
ALERT_RECIPIENT="youremail@gmail.com"
```
> You must create an App Password in your Google Account if you use 2FA.

3. Dependencies

**Python Backend:**
- Python 3.9+
```
cd backend
python -m venv venv && source ./venv/bin/activate
./venv/bin/pip install -r requirements.txt
```

**React Frontend**:
- Node 18+
```bash
cd frontend
npm install
```

4. Run the docker compose file
```bash
docker compose up --build
```

5. Access the application:

The front end is exposed at `localhost:3000` and the API is at `localhost:8000`

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
