#!/usr/bin/env python3
from __future__ import annotations
import argparse
import uvicorn
from loguru import logger

from backend.core import run_check_once
from backend.api import app
from backend.config import DESCRIPTION

def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the API (default 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (useful for development)"
    )
    args = parser.parse_args()

    logger.info(f"Starting Job Scraper API on {args.host}:{args.port} (reload={args.reload})")
    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload, log_level="info")


if __name__ == "__main__":
    main()
