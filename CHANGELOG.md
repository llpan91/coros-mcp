# Changelog

## [Unreleased]

### Added
- **Sleep timestamps**: `SleepRecord` now includes `sleep_start` and `sleep_end` fields (Unix timestamps) representing bedtime and wake time.
- Requesting `dataType: [5, 13]` from the COROS mobile API to retrieve the binary sleep timeline (`sleepList`).
- New `_parse_sleep_timestamps()` helper that decodes the base64-encoded `sleepList` entries and extracts start/end timestamps from the binary header (uint32 LE at offsets 15 and 20).

### Changed
- `fetch_sleep()` in `coros_api.py` now requests `dataType: [5, 13]` (previously `[5]` only) and populates the new timestamp fields.

### How it works
The COROS mobile API returns a `sleepList` field (via `dataType=13`) containing base64-encoded binary blobs for each sleep segment (main sleep + naps). Each blob encodes sleep-start and sleep-end as uint32 little-endian Unix timestamps at byte offsets 15 and 20 respectively. The first entry in the list corresponds to the main nighttime sleep.
