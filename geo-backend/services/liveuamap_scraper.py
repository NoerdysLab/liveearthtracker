"""
LiveUAMap scraper — DISABLED.
Playwright/Chromium removed to reduce memory usage on Railway (512 MB limit).
"""

import logging

logger = logging.getLogger(__name__)


def fetch_liveuamap():
    """Stub — returns empty list. Playwright has been removed."""
    logger.info("Liveuamap scraper disabled (Playwright removed for memory savings)")
    return []
