#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse
from pathlib import Path
import json
import time
import uvicorn
from loguru import logger
# Prometheus metrics
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
# jobscraper's run_check_once
from jobscraper import run_check_once

DATA_FILE = Path("jobs-seen.json")
LOG_FILE = Path("job-scraper.log")

app = FastAPI(title="Job Scraper API", version="1.0")

# Prometheus custom metrics
scrape_counter = Counter("job_scrapes_total", "Total number of scrapes triggered via API")
scrape_duration = Histogram("job_scrape_duration_seconds", "Duration of job scrapes triggered via API (seconds)")

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
    if run_check_once is None:
        raise HTTPException(status_code=500, detail="run_check_once not importable")

    logger.info("API /jobs called, starting run_check_once()")

    start = time.time()
    try:
        run_check_once()
        scrape_counter.inc()
    except Exception as e:
        logger.exception(f"Error while running run_check_once(): {e}")
    duration = time.time() - start
    scrape_duration.observe(duration)
    logger.info(f"Scrape finished in {duration:.2f}s")

    if not DATA_FILE.exists():
        raise HTTPException(status_code=404, detail=f"{DATA_FILE} not found")

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.exception(f"Error reading {DATA_FILE}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content=data)

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
        logger.exception(f"Error reading log file {LOG_FILE}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting Job Scraper API")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
