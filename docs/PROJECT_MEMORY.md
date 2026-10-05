# Project Memory — Goals & Race Status

Persistent memory for the gaochi (COROS) training project. Machine- and
agent-readable summary. Canonical goal source is `GOALS.md`; this file mirrors
it plus current race-registration status for quick recall.

Last updated: 2026-10-05 (Asia/Shanghai)

## Progressive Goal Ladder (increasing difficulty)

| # | Goal | Target | Required pace | Status |
|---|------|--------|---------------|--------|
| 0 | Half Marathon sub-1:43 | 1:43:00 | 4:52.9/km | ✅ Achieved 2026-09-13 (official 1:38:23) |
| 1 | Half Marathon sub-1:35 | 1:35:00 | 4:30.2/km | Active — very close (~3.6 s/km gap; best 4:33.8/km @ 怀柔 09-27) |
| 2 | Half Marathon sub-1:30 | 1:30:00 | 4:16.0/km | Active — stretch |
| 3 | Marathon sub-3:30 | 3:30:00 | 4:58.6/km | Active — first full milestone, none completed yet |
| 4 | Marathon sub-3:10 | 3:10:00 | 4:30.2/km | Active — intermediate |
| 5 | Marathon sub-3:00 | 2:59:59 | 4:15.0/km | Active — long-term (break 3h) |

Pace alignment: Half 1:35 ≈ Full 3:10 (both 4:30/km); Half 1:30 ≈ Full sub-3:00 (~4:15/km).

Ordering note: user's original list numbered sub-1:30 as #1 and sub-1:35 as #2;
ladder reorders by difficulty (1:43 → 1:35 → 1:30). Confirm if a different
priority is intended.

## Current Baseline (2026-09-27 怀柔 HM — current best)

- 21.22 km in 1:36:51 moving time, ~4:33.8/km, avg HR 170, max HR 181, TL 442.
  New HM PR, ~92 s faster than the 2026-09-13 Aoson official 1:38:23 (4:39/km),
  on a harder (more climbing) course. (Device moving time; not an official
  net/gun time.)
- Capability trend (2026-07 → 2026-10, verified): threshold pace (LTSP)
  4:35 → 4:18/km with LTHR stable 168-169; same-HR (146 bpm) aerobic pace
  5:52 → ~5:20/km (~30 s/km gain); VO2max 56 → 57; longest run 30.4 km.
- Recent quality-session threshold paces ~4:18-4:30.

## Race Registration Status (as of 2026-10-05)

| Race | Date | Distance | Status |
|------|------|----------|--------|
| 奥森 K马半程 | 2026-09-13 Sun | Half | ✅ Completed, official 1:38:23 (4:39/km) |
| 怀柔长城半马 | 2026-09-27 Sun | Half | ✅ Completed, 1:36:51 (4:33.8/km) — HM PR |
| 天津宝坻半马 | 2026-10-01 Thu | Half | ❌ DNS (弃赛) — did not start |
| 天津武清半马 | 2026-10-06 Tue | Half | ❌ DNS (弃赛) — will not start |
| 北京海淀全马 | 2026-10-11 Sun | Full | Not selected |
| 北京马拉松 (full) | 2026-10-18 Sun | Full | Newly registered, result pending |
| 天津半马 | 2026-10-25 Sun | Half | Not selected |
| 杭州半马 | 2026-11-01 Sun | Half | Not selected |
| 昌平马拉松 | TBD | — | Not selected |
| 朝阳区滨河半马 | 2026-11-01 Sun | Half | 🆕 Registered + will race. Start 07:30/07:38 (wave). 起点 北中轴景观大道（鸟巢与水立方之间）→ 终点 北京温榆河公园东岸草坪 |
| 南京全马 | 2026-11-22 Sun | Full | Not selected, on waitlist (候补中) |

Scheduling flag: 北京马拉松 (full) on 10-18 is only 13 days before the 10-31
half-marathon window and adjacent to other October races — a full marathon here
conflicts with an HM peak. The two cannot both be "all-out" races.

11-01 note: two half marathons fall on 2026-11-01 (Sun). 杭州半马 was not
selected; the race actually being run that day is 朝阳区滨河半马 (registered via
数字心动). Start 07:30/07:38 (wave starts); start line 北中轴景观大道 (between
鸟巢 and 水立方), finish at 北京温榆河公园东岸草坪. This is 14 days after the
10-18 北马 full — plan recovery/taper accordingly if targeting a strong result
(potential sub-1:35 attempt venue; course is riverside/park, likely flat).

## Compliance Rules (from GOALS.md + AGENTS.md)

- Do not mark a goal achieved from device estimates or short workouts; require an
  official race result at the required distance. Goal 0 is confirmed by the
  2026-09-13 official half marathon.
- Full-marathon goals additionally require completing a full marathon to validate
  endurance and fueling.
- Training calcs use activity-detail `workoutTime` (moving time).
- Verify full Gregorian-year dates and weekdays programmatically before use.
- Weekly comparisons use Monday–Sunday calendar weeks; keep partial current weeks
  separate.

## Report Artifacts

- `report/2026-10-05-capability-improvement-deep-analysis.html` — capability
  improvement assessment (threshold pace, same-HR aerobic efficiency, HM PR,
  volume/load, physiology). Confirms clear fitness gains Jul→Oct.
- `report/2026-09-17-multidimensional-training-analysis.html` — deep analysis;
  section 8 holds the goal ladder, section 10 the current-week training advice.
- `report/2026-09-17-race-registration-tracker.html` — race-status snapshot.
