import json
import requests
from typing import Dict, List

from backend.config import DATA_FILE, USER_AGENT
from backend.logger import logger

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

def safe_get(url: str, **kwargs):
    try:
        r = session.get(url, timeout=15, **kwargs)
        r.raise_for_status()
        return r
    except Exception as e:
        logger.error(f"Request failed for {url}: {e}")
        return None

def load_seen() -> Dict[str, List[Dict]]:
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception as ex:
            logger.warning(f"Failed to read {DATA_FILE}; starting fresh {ex}")
    return {}

def save_seen(data: Dict[str, List[Dict]]) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    logger.debug(f"Saved seen state to {DATA_FILE}")
