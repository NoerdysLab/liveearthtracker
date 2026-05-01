"""
API Settings management — serves the API key registry and allows updates.
Keys are stored in the backend .env file and loaded via python-dotenv.
"""
import os
import re
from pathlib import Path

# Path to the backend .env file
ENV_PATH = Path(__file__).parent.parent / ".env"

# ---------------------------------------------------------------------------
# API Registry — every external service the dashboard depends on
# ---------------------------------------------------------------------------
API_REGISTRY = [
    {
        "id": "opensky_client_id",
        "env_key": "OPENSKY_CLIENT_ID",
        "name": "OpenSky Network — Client ID",
        "description": "OAuth2 client ID for the OpenSky Network API. Provides global flight state vectors with 400 requests/day.",
        "category": "Aviation",
        "url": "https://opensky-network.org/",
        "required": True,
    },
    {
        "id": "opensky_client_secret",
        "env_key": "OPENSKY_CLIENT_SECRET",
        "name": "OpenSky Network — Client Secret",
        "description": "OAuth2 client secret paired with the Client ID above. Used for authenticated token refresh.",
        "category": "Aviation",
        "url": "https://opensky-network.org/",
        "required": True,
    },
    {
        "id": "ais_api_key",
        "env_key": "AIS_API_KEY",
        "name": "AIS Stream",
        "description": "WebSocket API key for real-time Automatic Identification System (AIS) vessel tracking data worldwide.",
        "category": "Maritime",
        "url": "https://aisstream.io/",
        "required": True,
    },
    {
        "id": "adsb_lol",
        "env_key": None,
        "name": "ADS-B Exchange (adsb.lol)",
        "description": "Community-maintained ADS-B flight tracking API. No key required — public endpoint.",
        "category": "Aviation",
        "url": "https://api.adsb.lol/",
        "required": False,
    },
    {
        "id": "usgs_earthquakes",
        "env_key": None,
        "name": "USGS Earthquake Hazards",
        "description": "Real-time earthquake data feed from the United States Geological Survey. No key required.",
        "category": "Geophysical",
        "url": "https://earthquake.usgs.gov/",
        "required": False,
    },
    {
        "id": "celestrak",
        "env_key": None,
        "name": "CelesTrak (NORAD TLEs)",
        "description": "Satellite orbital element data from CelesTrak. Provides TLE sets for 2,000+ active satellites. No key required.",
        "category": "Space",
        "url": "https://celestrak.org/",
        "required": False,
    },
    {
        "id": "gdelt",
        "env_key": None,
        "name": "GDELT Project",
        "description": "Global Database of Events, Language, and Tone. Monitors news media for geopolitical events worldwide. No key required.",
        "category": "Intelligence",
        "url": "https://www.gdeltproject.org/",
        "required": False,
    },
    {
        "id": "nominatim",
        "env_key": None,
        "name": "Nominatim (OpenStreetMap)",
        "description": "Reverse geocoding service. Converts lat/lng coordinates to human-readable location names. No key required.",
        "category": "Geolocation",
        "url": "https://nominatim.openstreetmap.org/",
        "required": False,
    },
    {
        "id": "rainviewer",
        "env_key": None,
        "name": "RainViewer",
        "description": "Weather radar tile overlay. Provides global precipitation data as map tiles. No key required.",
        "category": "Weather",
        "url": "https://www.rainviewer.com/",
        "required": False,
    },
    {
        "id": "rss_feeds",
        "env_key": None,
        "name": "RSS News Feeds",
        "description": "Aggregates from NPR, BBC, Al Jazeera, NYT, Reuters, and AP for global news coverage. No key required.",
        "category": "Intelligence",
        "url": None,
        "required": False,
    },
    {
        "id": "yfinance",
        "env_key": None,
        "name": "Yahoo Finance (yfinance)",
        "description": "Defense sector stock tickers and commodity prices. Uses the yfinance Python library. No key required.",
        "category": "Markets",
        "url": "https://finance.yahoo.com/",
        "required": False,
    },
    {
        "id": "openmhz",
        "env_key": None,
        "name": "OpenMHz",
        "description": "Public radio scanner feeds for SIGINT interception. Streams police/fire/EMS radio traffic. No key required.",
        "category": "SIGINT",
        "url": "https://openmhz.com/",
        "required": False,
    },
    # ── New key-based services ──
    {
        "id": "ebird",
        "env_key": "EBIRD_API_KEY",
        "name": "eBird (Cornell Lab)",
        "description": "Notable bird sightings worldwide from the Cornell Lab of Ornithology. Real-time citizen-science observations.",
        "category": "Wildlife",
        "url": "https://ebird.org/",
        "required": False,
    },
    {
        "id": "openweathermap",
        "env_key": "OPENWEATHERMAP_API_KEY",
        "name": "OpenWeatherMap",
        "description": "Global weather data, severe weather alerts, and air quality indices for any location.",
        "category": "Weather",
        "url": "https://openweathermap.org/",
        "required": False,
    },
    {
        "id": "purpleair",
        "env_key": "PURPLEAIR_API_KEY",
        "name": "PurpleAir",
        "description": "Crowdsourced real-time air quality sensor network. PM2.5 readings from thousands of outdoor sensors.",
        "category": "Weather",
        "url": "https://www.purpleair.com/",
        "required": False,
    },
    {
        "id": "alienvault_otx",
        "env_key": "ALIENVAULT_OTX_KEY",
        "name": "AlienVault OTX",
        "description": "Open Threat Exchange — crowdsourced cyber threat intelligence. Malicious IPs, domains, and threat pulses.",
        "category": "Cyber",
        "url": "https://otx.alienvault.com/",
        "required": False,
    },
    {
        "id": "virustotal",
        "env_key": "VIRUSTOTAL_API_KEY",
        "name": "VirusTotal",
        "description": "Malware and URL scanning aggregator. Global threat feed for IOC enrichment.",
        "category": "Cyber",
        "url": "https://www.virustotal.com/",
        "required": False,
    },
    {
        "id": "finnhub",
        "env_key": "FINNHUB_API_KEY",
        "name": "Finnhub",
        "description": "Real-time stock prices, forex, and economic data. Supplements yfinance for defense sector monitoring.",
        "category": "Markets",
        "url": "https://finnhub.io/",
        "required": False,
    },
    {
        "id": "newsapi",
        "env_key": "NEWSAPI_KEY",
        "name": "NewsAPI",
        "description": "Structured news aggregation from 150,000+ sources. Headlines and full articles with geo-tagging.",
        "category": "Intelligence",
        "url": "https://newsapi.org/",
        "required": False,
    },
    {
        "id": "ticketmaster",
        "env_key": "TICKETMASTER_KEY",
        "name": "Ticketmaster Discovery",
        "description": "Global event data — concerts, sports, festivals. Shows large public gatherings on the map.",
        "category": "Events",
        "url": "https://developer.ticketmaster.com/",
        "required": False,
    },
    {
        "id": "global_fishing_watch",
        "env_key": "GLOBAL_FISHING_WATCH_TOKEN",
        "name": "Global Fishing Watch",
        "description": "Satellite-derived fishing vessel activity worldwide. Detects illegal, unreported, and unregulated (IUU) fishing.",
        "category": "Maritime",
        "url": "https://globalfishingwatch.org/",
        "required": False,
    },
    # ── New no-key services ──
    {
        "id": "nasa_firms",
        "env_key": None,
        "name": "NASA FIRMS",
        "description": "Active fire/hotspot detections from MODIS and VIIRS satellites. Updated every ~3 hours. No key required.",
        "category": "Geophysical",
        "url": "https://firms.modaps.eosdis.nasa.gov/",
        "required": False,
    },
    {
        "id": "nasa_eonet",
        "env_key": None,
        "name": "NASA EONET",
        "description": "Earth Observatory Natural Event Tracker — volcanoes, storms, icebergs, dust plumes. No key required.",
        "category": "Geophysical",
        "url": "https://eonet.gsfc.nasa.gov/",
        "required": False,
    },
    {
        "id": "open_meteo",
        "env_key": None,
        "name": "Open-Meteo",
        "description": "Free weather API for 40+ major cities. Temperature, wind, humidity, weather codes. No key required.",
        "category": "Weather",
        "url": "https://open-meteo.com/",
        "required": False,
    },
    {
        "id": "open_notify_iss",
        "env_key": None,
        "name": "Open Notify (ISS)",
        "description": "Real-time International Space Station position. Updated every 60 seconds. No key required.",
        "category": "Space",
        "url": "http://open-notify.org/",
        "required": False,
    },
    {
        "id": "noaa_swpc",
        "env_key": None,
        "name": "NOAA SWPC",
        "description": "Space Weather Prediction Center — geomagnetic storm Kp index, solar flare alerts. No key required.",
        "category": "Space",
        "url": "https://www.swpc.noaa.gov/",
        "required": False,
    },
    {
        "id": "uk_carbon_intensity",
        "env_key": None,
        "name": "UK Carbon Intensity",
        "description": "National Grid ESO carbon intensity by region. Forecasts and generation mix. No key required.",
        "category": "Energy",
        "url": "https://carbonintensity.org.uk/",
        "required": False,
    },
    {
        "id": "telegeography",
        "env_key": None,
        "name": "TeleGeography Submarine Cables",
        "description": "Global submarine cable landing points from the Submarine Cable Map. No key required.",
        "category": "Infrastructure",
        "url": "https://www.submarinecablemap.com/",
        "required": False,
    },
]


def _obfuscate(value: str) -> str:
    """Show first 4 chars, mask the rest with bullets."""
    if not value or len(value) <= 4:
        return "••••••••"
    return value[:4] + "•" * (len(value) - 4)


def get_api_keys():
    """Return the full API registry with obfuscated key values."""
    result = []
    for api in API_REGISTRY:
        entry = {
            "id": api["id"],
            "name": api["name"],
            "description": api["description"],
            "category": api["category"],
            "url": api["url"],
            "required": api["required"],
            "has_key": api["env_key"] is not None,
            "env_key": api["env_key"],
            "value_obfuscated": None,
            "is_set": False,
        }
        if api["env_key"]:
            raw = os.environ.get(api["env_key"], "")
            entry["value_obfuscated"] = _obfuscate(raw)
            entry["is_set"] = bool(raw)
        result.append(entry)
    return result


def update_api_key(env_key: str, new_value: str) -> bool:
    """Update a single key in the .env file and in the current process env."""
    if not ENV_PATH.exists():
        return False

    # Update os.environ immediately
    os.environ[env_key] = new_value

    # Update the .env file on disk
    content = ENV_PATH.read_text(encoding="utf-8")
    pattern = re.compile(rf"^{re.escape(env_key)}=.*$", re.MULTILINE)
    if pattern.search(content):
        content = pattern.sub(f"{env_key}={new_value}", content)
    else:
        content = content.rstrip("\n") + f"\n{env_key}={new_value}\n"

    ENV_PATH.write_text(content, encoding="utf-8")
    return True
