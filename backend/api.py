#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse
import json
import time
import uvicorn
import redis
import os
from datetime import datetime
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
# Prometheus metrics
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, REGISTRY
# run_check_once
from backend.core import run_check_once
from backend.config import DATA_FILE, LOG_FILE

# Redis config
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
JOBS_CACHE_KEY = "jobs_cache"
TOP_JOBS_CACHE_KEY = "top_jobs_cache"
STATS_CACHE_KEY = "stats_cache"
CACHE_TTL_SECONDS = 30 * 60  # 30 minutes

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

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
    Returns jobs JSON, caching results in Redis for 30 minutes
    """
    global last_scrape_time
    # Try to get cached data
    cached = r.get(JOBS_CACHE_KEY)
    if cached:
        logger.info("[Cache] Returning jobs from Redis cache")
        return JSONResponse(content=json.loads(cached))

    # Delete our other cached info so its updates on a scrape
    r.delete(TOP_JOBS_CACHE_KEY)
    r.delete(STATS_CACHE_KEY)

    logger.info("[Scrape] No cache found, running scrape")
    start = time.time()
    try:
        run_check_once()
        scrape_counter.inc()
        last_scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.exception(f"[Scrape] Error while running scrape: {e}")

    duration = time.time() - start
    scrape_duration.observe(duration)
    logger.info(f"[Scrape] finished in {duration:.2f}s")

    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail=f"{DATA_FILE} not found")

    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Add to cache
    r.setex(JOBS_CACHE_KEY, CACHE_TTL_SECONDS, json.dumps(data))
    return JSONResponse(content=data)


# Top Jobs Endpoint
@app.get("/top_jobs", response_class=JSONResponse)
def top_jobs():
    cached = r.get(TOP_JOBS_CACHE_KEY)
    if cached:
        logger.info("[Cache] Returning top jobs from Redis cache")
        return JSONResponse(content=json.loads(cached))

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
            matched_keywords = [kw for kw in KEYWORDS if kw in title or kw in description]
            if matched_keywords:
                top_jobs_list.append({
                    "company": company.capitalize(),
                    "title": job.get("title"),
                    "location": job.get("location"),
                    "link": job.get("link"),
                    "logo": job.get("logo") or f"/logos/{company.lower().replace(' ', '-')}.svg",
                    "filters": matched_keywords
                })

    top_jobs_list.sort(key=lambda x: (x["company"].lower(), x["title"].lower()))
    result = {
        "count": len(top_jobs_list),
        "jobs": top_jobs_list,
        "keywords": KEYWORDS
    }

    r.setex(TOP_JOBS_CACHE_KEY, CACHE_TTL_SECONDS, json.dumps(result))
    return JSONResponse(content=result)

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
    """
    Returns stats used on the homepage dashboard of the app
    """
    cached = r.get(STATS_CACHE_KEY)
    if cached:
        logger.info("[Cache] Returning stats from Redis cache")
        return JSONResponse(content=json.loads(cached))

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

    total_scrapes = int(scrape_counter._value.get())

    avg_duration = 0.0
    for metric in scrape_duration.collect():
        sum_val = None
        count_val = None
        for sample in metric.samples:
            if sample.name.endswith("_sum"):
                sum_val = sample.value
            elif sample.name.endswith("_count"):
                count_val = sample.value
        if sum_val is not None and count_val:
            avg_duration = sum_val / count_val

    result = {
        "total_jobs": total_jobs,
        "companies": num_companies,
        "total_scrapes": total_scrapes,
        "scrape_durations_seconds": round(avg_duration, 2),
        "last_scrape": last_scrape_time or "N/A"
    }

    # Cache the result
    r.setex(STATS_CACHE_KEY, CACHE_TTL_SECONDS, json.dumps(result))
    return JSONResponse(content=result)

if __name__ == "__main__":
    logger.info("[Start] Starting Job Scraper API")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
