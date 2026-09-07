print('application running')
"""
app.py
======
Simulated application entry point for the ENVIRONMENT-ACCESS-VALIDATION project.
Demonstrates a minimal Python web application structure used during
environment and pipeline validation checks.
"""

import os
import logging
import datetime

# ── Logging Setup ─────────────────────────────────────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ── App Config ────────────────────────────────────────────────────────────────
APP_NAME = "environment-access-validator"
VERSION = "1.0.0"
ENV = os.environ.get("APP_ENV", "development")


def get_status():
    """Return a health-check dict for the application."""
    return {
        "app": APP_NAME,
        "version": VERSION,
        "env": ENV,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "status": "healthy",
    }


def start():
    """Simulate application startup."""
    logger.info(f"Starting {APP_NAME} v{VERSION} [{ENV}]")
    status = get_status()
    logger.info(f"Health check: {status}")
    print(f"[{APP_NAME}] Running in {ENV} mode — v{VERSION}")
    return status


if __name__ == "__main__":
    start()
