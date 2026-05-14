# Changelog

## [Unreleased]

### Fixed

#### Web Token 刷新不再丢失 Mobile 认证 (2026-05-14)
- 修复 `try_auto_login()` 在 Web token 过期自动重新登录时，会覆盖已有的 `mobile_access_token` 和 `mobile_login_payload`，导致 Mobile 认证丢失的问题。
- 修复后：Web token 24 小时过期自动刷新时，保留已有的 Mobile 凭证，不再需要重新执行 Mobile 登录（避免踢掉手机 App 登录态）。
- 更新 README 注意事项，明确 Web/Mobile 认证的独立性。

### Added

#### 睡眠分析：入睡/起床时间展示 (2026-05-14)
- `get_sleep_data` MCP 工具现在返回人类可读的 `sleep_start`（入睡时间）和 `sleep_end`（起床时间）字段，格式为 `"YYYY-MM-DD HH:MM:SS"` 本地时间。
- 底层 `SleepRecord` 模型已包含 `sleep_start`/`sleep_end` Unix 时间戳，此次改动在 `server.py` 中通过 `fmt_local_time()` 转换为可读格式输出。
- 便于 AI 分析入睡规律（如是否晚睡）并给出针对性的睡眠优化建议。

#### 跑步活动：天气数据集成 (2026-05-14)
- **活动详情** (`get_activity_detail`)：解析 Coros API 原生天气数据，返回 `temperature_c`（气温）、`feels_like_c`（体感温度）、`relative_humidity_pct`（湿度）、`wind_speed_kmh`（风速）、`wind_direction_deg`（风向）。
- **活动列表** (`list_activities`)：通过 Open-Meteo API 获取历史天气数据，每条活动附带 `weather` 字段。
- 新增 `weather.py` 模块，封装 Open-Meteo API 调用、SQLite 缓存（按 `lat/lon/date/hour` 缓存避免重复请求）、并发控制（semaphore 限制 5 个并发请求）。
- 新增 `WeatherData` Pydantic 模型和 `weather_cache` SQLite 表。
- `ActivitySummary` 新增 `start_lat`/`start_lon` 字段，从 Coros 活动数据中提取 GPS 坐标。
- 支持 `COROS_DEFAULT_LAT`/`COROS_DEFAULT_LON` 环境变量，室内活动或无 GPS 数据时作为位置回退。
- `weather.source` 字段标识数据来源：`"coros"`（原生详情数据）、`"gps"`（GPS 坐标查询）或 `"default_location"`（环境变量回退）。

### Previous

#### Sleep timestamps (initial)
- `SleepRecord` includes `sleep_start` and `sleep_end` fields (Unix timestamps) representing bedtime and wake time.
- Requesting `dataType: [5, 13]` from the COROS mobile API to retrieve the binary sleep timeline (`sleepList`).
- `_parse_sleep_timestamps()` decodes the base64-encoded `sleepList` entries and extracts start/end timestamps from the binary header (uint32 LE at offsets 15 and 20).
