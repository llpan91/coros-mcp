"""Open-Meteo weather integration for activity enrichment.

Fetches historical weather (temperature, humidity, wind speed) for activity
locations and times.  Results are cached in SQLite to avoid redundant API calls.
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx

from cache.store import get_cached_weather, get_cached_weather_batch, upsert_weather
from models import WeatherData

logger = logging.getLogger(__name__)

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY_VARS = "temperature_2m,relative_humidity_2m,wind_speed_10m"
_SEMAPHORE = asyncio.Semaphore(5)


def _default_location() -> Optional[tuple[float, float]]:
    lat = os.getenv("COROS_DEFAULT_LAT")
    lon = os.getenv("COROS_DEFAULT_LON")
    if lat and lon:
        try:
            return float(lat), float(lon)
        except ValueError:
            return None
    return None


def get_location_for_activity(
    start_lat: Optional[float],
    start_lon: Optional[float],
) -> tuple[Optional[tuple[float, float]], str]:
    """Return ((lat, lon), source) for an activity.

    Returns GPS coords if valid, else falls back to COROS_DEFAULT_LAT/LON.
    source is "gps" or "default_location".
    Returns (None, "") if neither is available.
    """
    if (
        start_lat is not None
        and start_lon is not None
        and start_lat != 0
        and start_lon != 0
    ):
        return (start_lat, start_lon), "gps"
    default = _default_location()
    if default:
        return default, "default_location"
    return None, ""


def _cache_key(lat: float, lon: float, dt: datetime) -> str:
    utc_dt = dt.astimezone(timezone.utc)
    return f"{lat:.2f}_{lon:.2f}_{utc_dt.strftime('%Y%m%d')}_{utc_dt.strftime('%H')}"


def _group_key(lat: float, lon: float, dt: datetime) -> str:
    """Key for grouping requests that can share one API call (same location+date)."""
    utc_dt = dt.astimezone(timezone.utc)
    return f"{lat:.2f}_{lon:.2f}_{utc_dt.strftime('%Y%m%d')}"


def _pick_url(dt: datetime) -> str:
    age = datetime.now(timezone.utc) - dt.astimezone(timezone.utc)
    return ARCHIVE_URL if age > timedelta(days=5) else FORECAST_URL


def _extract_hourly(data: dict, target_hour: int) -> Optional[WeatherData]:
    """Extract weather for the target UTC hour from Open-Meteo hourly response."""
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    humids = hourly.get("relative_humidity_2m", [])
    winds = hourly.get("wind_speed_10m", [])

    if not times:
        return None

    best_idx = 0
    best_diff = 999
    for i, t in enumerate(times):
        try:
            h = int(t[11:13])
        except (ValueError, IndexError):
            continue
        diff = abs(h - target_hour)
        if diff < best_diff:
            best_diff = diff
            best_idx = i

    return WeatherData(
        temperature_c=temps[best_idx] if best_idx < len(temps) else None,
        relative_humidity_pct=humids[best_idx] if best_idx < len(humids) else None,
        wind_speed_kmh=winds[best_idx] if best_idx < len(winds) else None,
    )


async def _call_open_meteo(
    lat: float, lon: float, date_str: str, url: str
) -> Optional[dict]:
    params = {
        "latitude": round(lat, 2),
        "longitude": round(lon, 2),
        "start_date": date_str,
        "end_date": date_str,
        "hourly": HOURLY_VARS,
        "timezone": "UTC",
    }
    async with _SEMAPHORE:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except Exception as exc:
            logger.warning("Open-Meteo request failed: %s", exc)
            return None


async def fetch_weather(
    lat: float,
    lon: float,
    dt: datetime,
    source: str = "gps",
) -> Optional[WeatherData]:
    """Fetch weather for a single location+time. Returns None on failure."""
    utc_dt = dt.astimezone(timezone.utc)
    key = _cache_key(lat, lon, utc_dt)

    cached = get_cached_weather(key)
    if cached:
        w = WeatherData.model_validate_json(cached)
        w.source = source
        return w

    date_str = utc_dt.strftime("%Y-%m-%d")
    url = _pick_url(utc_dt)
    data = await _call_open_meteo(lat, lon, date_str, url)
    if data is None:
        return None

    weather = _extract_hourly(data, utc_dt.hour)
    if weather is None:
        return None

    weather.source = source
    upsert_weather(key, weather.model_dump_json())
    return weather


async def fetch_weather_batch(
    requests: list[tuple[float, float, datetime, str]],
) -> list[Optional[WeatherData]]:
    """Fetch weather for multiple (lat, lon, dt, source) tuples efficiently.

    Groups by (rounded location, date) to minimize API calls.
    """
    if not requests:
        return []

    cache_keys = [_cache_key(lat, lon, dt) for lat, lon, dt, _ in requests]
    cached = get_cached_weather_batch(cache_keys)

    results: list[Optional[WeatherData]] = [None] * len(requests)
    to_fetch: dict[str, list[int]] = {}

    for i, (lat, lon, dt, source) in enumerate(requests):
        key = cache_keys[i]
        if key in cached:
            w = WeatherData.model_validate_json(cached[key])
            w.source = source
            results[i] = w
        else:
            gk = _group_key(lat, lon, dt)
            to_fetch.setdefault(gk, []).append(i)

    groups: dict[str, tuple[float, float, str, str]] = {}
    for gk, indices in to_fetch.items():
        idx = indices[0]
        lat, lon, dt, _ = requests[idx]
        utc_dt = dt.astimezone(timezone.utc)
        date_str = utc_dt.strftime("%Y-%m-%d")
        url = _pick_url(utc_dt)
        groups[gk] = (round(lat, 2), round(lon, 2), date_str, url)

    async def _fetch_group(gk: str) -> Optional[dict]:
        lat, lon, date_str, url = groups[gk]
        return await _call_open_meteo(lat, lon, date_str, url)

    group_keys = list(groups.keys())
    api_results = await asyncio.gather(
        *[_fetch_group(gk) for gk in group_keys],
        return_exceptions=True,
    )
    group_data: dict[str, Optional[dict]] = {}
    for gk, res in zip(group_keys, api_results):
        group_data[gk] = res if not isinstance(res, Exception) else None

    for gk, indices in to_fetch.items():
        data = group_data.get(gk)
        if data is None:
            continue
        for idx in indices:
            lat, lon, dt, source = requests[idx]
            utc_dt = dt.astimezone(timezone.utc)
            weather = _extract_hourly(data, utc_dt.hour)
            if weather:
                weather.source = source
                key = cache_keys[idx]
                upsert_weather(key, weather.model_dump_json())
                results[idx] = weather

    return results
