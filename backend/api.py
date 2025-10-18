#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse
from pathlib import Path
import json
import time
import uvicorn
from datetime import datetime
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
# Prometheus metrics
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, REGISTRY
# run_check_once
from backend.core import run_check_once
from backend.config import DATA_FILE, LOG_FILE

app = FastAPI(title="Job Scraper API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://jobwatch.dev.homelab",
        "https://jobwatch.homelab",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus custom metrics
scrape_counter = Counter("job_scrapes_total", "Total number of scrapes triggered via API")
scrape_duration = Histogram("job_scrape_duration_seconds", "Duration of job scrapes triggered via API (seconds)")
last_scrape_time = None  # global variable to store last scrape

# Metrics endpoint
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Healthcheck endpoint
@app.get("/health")
def health():
    return {"status": "ok", "time": time.strftime("%Y-%m-%d %H:%M:%S")}

# Jobs JSON endpoint
@app.get("/jobs", response_class=JSONResponse)
def jobs():
    """
    Triggers run_check_once() and then returns the JSONfile that run_check_once updates.
    """
    global last_scrape_time 
    if run_check_once is None:
        raise HTTPException(status_code=500, detail="run_check_once not importable")

    logger.info("[Scrape] API /jobs called, starting scrape")

    start = time.time()
    try:
        run_check_once()
        scrape_counter.inc()
        last_scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # now updates the global
    except Exception as e:
        logger.exception(f"[Scrape] Error while running scrape: {e}")

    duration = time.time() - start
    scrape_duration.observe(duration)
    logger.info(f"[Scrape] finished in {duration:.2f}s")

    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail=f"{DATA_FILE} not found")

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.exception(f"[State] Error reading {DATA_FILE}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content=data)

# Top Jobs Endpoint
@app.get("/top_jobs", response_class=JSONResponse)
def top_jobs():
    """
    Returns a filtered list of jobs that match user-preferred keywords,
    including which keywords matched for each job.
    """
    KEYWORDS = ["devops", "site reliability", "sre", "platform", "infrastructure"]
    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail=f"{DATA_FILE} not found")

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.exception(f"[State] Error reading {DATA_FILE}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    top_jobs_list = []

    for company, jobs_list in data.items():
        for job in jobs_list:
            title = job.get("title", "").lower()
            description = job.get("description", "").lower()

            # Find which keywords matched
            matched_keywords = [kw for kw in KEYWORDS if kw in title or kw in description]
            if matched_keywords:
                top_jobs_list.append({
                    "company": company.capitalize(),
                    "title": job.get("title"),
                    "location": job.get("location"),
                    "link": job.get("link"),
                    "logo": job.get("logo") or f"/logos/{company.lower().replace(' ', '-')}.svg",
                    "filters": matched_keywords  # <-- new field
                })

    # Sort by company name or title for consistency
    top_jobs_list.sort(key=lambda x: (x["company"].lower(), x["title"].lower()))
    return JSONResponse(content={
        "count": len(top_jobs_list),
        "jobs": top_jobs_list,
        "keywords": KEYWORDS  # optional: include full filter list
    })

# Log endpoint
@app.get("/logs", response_class=PlainTextResponse)
def logs(lines: int = 500):
    """
    Return last N lines of the log file. Example: /logs?lines=200
    """
    if not LOG_FILE.exists():
        raise HTTPException(status_code=404, detail=f"{LOG_FILE} not found")

    try:
        with LOG_FILE.open("r", encoding="utf-8") as f:
            all_lines = f.readlines()
        return "".join(all_lines[-lines:])
    except Exception as e:
        logger.exception(f"[Logs] Error reading log file {LOG_FILE}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Homepage Dashboard endpoint
@app.get("/stats")
def stats():
    num_companies = 0
    total_jobs = 0

    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                num_companies = len(data.keys())
                total_jobs = sum(len(v) for v in data.values())
        except Exception as e:
            logger.error(f"[State] Failed to read {DATA_FILE}: {e}")

    # Directly read the counter value
    total_scrapes = int(scrape_counter._value.get())

    # Compute average from histogram samples
    avg_duration = 0.0
    for metric in scrape_duration.collect():
        # metric.samples is a list of tuples: (name, labels, value)
        sum_val = None
        count_val = None
        for sample in metric.samples:
            if sample.name.endswith("_sum"):
                sum_val = sample.value
            elif sample.name.endswith("_count"):
                count_val = sample.value
        if sum_val is not None and count_val:
            avg_duration = sum_val / count_val

    return {
        "total_jobs": total_jobs,
        "companies": num_companies,
        "total_scrapes": total_scrapes,
        "scrape_durations_seconds": round(avg_duration, 2),
        "last_scrape": last_scrape_time or "N/A"
    }

if __name__ == "__main__":
    logger.info("[Start] Starting Job Scraper API")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
