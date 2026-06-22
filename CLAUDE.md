# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`coros-mcp` is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes Coros fitness data (sleep, HRV, training metrics, activities, workouts) to AI assistants. It uses the **unofficial** Coros API — no official API key required.

## Setup & Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Commands

```bash
# Run the MCP server
python server.py

# Lint (CI uses this)
ruff check .

# Run all tests
pytest -v

# Run a single test file or test
pytest tests/test_cache_sync.py -v
pytest tests/test_cache_sync.py::test_function_name -v

# CLI
coros-mcp auth           # Authenticate (web + mobile tokens)
coros-mcp auth-status    # Check token status
coros-mcp auth-clear     # Remove stored tokens
```

### Environment Variables

- `COROS_EMAIL` / `COROS_PASSWORD` / `COROS_REGION` — auto-login credentials (or use `.env` file)
- `COROS_TIMEZONE` — override timezone for date formatting (defaults to system)
- `COROS_DEFAULT_LAT` / `COROS_DEFAULT_LON` — fallback location for weather when activity has no GPS
- `COROS_STABLE_DAYS` — days before data is considered immutable in cache (default: 2)

## Architecture

The project wraps two separate Coros APIs behind a unified MCP interface, with a SQLite caching layer in between.

### Dual API Design
- **Training Hub web API** (`teameuapi.coros.com` / `teamapi.coros.com`): HRV, daily metrics, activities, workouts. Auth via MD5-hashed password → `accessToken` header. Token TTL: 24 hours.
- **Mobile API** (`apieu.coros.com` / `apius.coros.com`): Sleep stage data (deep/light/REM/awake). Auth via AES-128-CBC encrypted credentials (key reverse-engineered from Coros APK). Token TTL: ~1 hour, **auto-refreshes** by replaying the stored encrypted login payload.

### Data Flow

```
MCP tool (server.py)
  → cache/sync.py (check SQLite, fetch only missing tail)
    → coros_api.py (HTTP calls to Coros)
    → cache/store.py (persist to SQLite)
  → return merged results
```

### Caching Layer (`cache/`)
- **`cache/store.py`**: SQLite DB at `~/.config/coros-mcp/cache.db`. Three data tables (`daily_records`, `sleep_records`, `activities`) + `weather_cache`. Records stored as JSON blobs keyed by date or activity_id.
- **`cache/sync.py`**: Smart fetch logic — compares requested range against cached range, only fetches the uncached tail from the API. Data within `STABLE_AFTER_DAYS` (default 2) is always re-fetched to capture delayed syncs. Full backfill done in 12-week chunks.
- **`cache/utils.py`**: Timezone-aware date formatting (`COROS_TIMEZONE` env var → `LOCAL_TZ`).

### Token Storage (`auth/`)
Priority chain for retrieval: `COROS_ACCESS_TOKEN` env var → encrypted local file → system keyring. On write, both keyring and encrypted file are updated. The entire `StoredAuth` object (web token + mobile token + mobile login payload for replay) is serialized as JSON and stored as a single credential.

### Weather Enrichment (`weather.py`)
Activity list responses are enriched with Open-Meteo historical weather data. GPS coords from the activity (or `COROS_DEFAULT_LAT/LON` fallback) are used. Results cached in SQLite `weather_cache` table. Activity detail uses native Coros weather (values scaled by 10, e.g. temperature=232 → 23.2°C).

### Key Files
- **`server.py`**: FastMCP tool definitions. Each `@mcp.tool()` validates auth, delegates to cache/sync or coros_api, and returns a dict. The `_run_with_auth()` wrapper retries once with re-login on auth failure.
- **`coros_api.py`**: All HTTP logic. Two sets of endpoints (Training Hub + mobile), AES encryption for mobile auth, auto-refresh logic, and response parsers. `fetch_daily_records()` merges `/analyse/dayDetail/query` (long range) + `/analyse/query` (last 28 days, has VO2max/fitness).
- **`models.py`**: Pydantic v2 models: `StoredAuth`, `DailyRecord`, `SleepRecord`/`SleepPhases`, `HRVRecord`, `ActivitySummary`, `WeatherData`.
- **`cli.py`**: CLI entry point registered as `coros-mcp` script.

### API Response Pattern
All Coros API responses return `result: "0000"` on success. Any other value → error (check `message` field). Large time-series fields (`graphList`, `frequencyList`, `gpsLightDuration`) are stripped from activity detail responses.

### Region Handling
Regions (`eu`, `us`) map to different base URLs for both APIs. EU tokens only work on EU endpoints — mixing regions causes auth failures.
