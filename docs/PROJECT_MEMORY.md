# Project Memory — Goals & Race Status

Persistent memory for the gaochi (COROS) training project. Machine- and
agent-readable summary. Canonical goal source is `GOALS.md`; this file mirrors
it plus current race-registration status for quick recall.

Last updated: 2026-09-17 (Asia/Shanghai)

## Progressive Goal Ladder (increasing difficulty)

| # | Goal | Target | Required pace | Status |
|---|------|--------|---------------|--------|
| 0 | Half Marathon sub-1:43 | 1:43:00 | 4:52.9/km | ✅ Achieved 2026-09-13 (official 1:38:23) |
| 1 | Half Marathon sub-1:35 | 1:35:00 | 4:30.2/km | Active — nearest next target (~9 s/km gap) |
| 2 | Half Marathon sub-1:30 | 1:30:00 | 4:16.0/km | Active — stretch |
| 3 | Marathon sub-3:30 | 3:30:00 | 4:58.6/km | Active — first full milestone, none completed yet |
| 4 | Marathon sub-3:10 | 3:10:00 | 4:30.2/km | Active — intermediate |
| 5 | Marathon sub-3:00 | 2:59:59 | 4:15.0/km | Active — long-term (break 3h) |

Pace alignment: Half 1:35 ≈ Full 3:10 (both 4:30/km); Half 1:30 ≈ Full sub-3:00 (~4:15/km).

Ordering note: user's original list numbered sub-1:30 as #1 and sub-1:35 as #2;
ladder reorders by difficulty (1:43 → 1:35 → 1:30). Confirm if a different
priority is intended.

## Current Baseline (2026-09-13 official HM)

- 21.16 km in 1:38:23 moving time, ~4:39/km, avg HR 169.
- Recent quality-session threshold paces ~4:26–4:35.

## Race Registration Status (as of 2026-09-17)

| Race | Date | Distance | Status |
|------|------|----------|--------|
| 奥森 K马半程 | 2026-09-13 Sun | Half | ✅ Registered + completed, 1:38:23 |
| 怀柔长城半马 | 2026-09-27 Sun | Half | Won (sponsor slot) / secured |
| 天津宝坻半马 | 2026-10-01 Thu | Half | Secured (no lottery) |
| 天津武清半马 | 2026-10-06 Tue | Half | Won lottery |
| 北京海淀全马 | 2026-10-11 Sun | Full | Not selected |
| 北京马拉松 (full) | 2026-10-18 Sun | Full | Newly registered, result pending |
| 天津半马 | 2026-10-25 Sun | Half | Not selected |
| 杭州半马 | 2026-11-01 Sun | Half | Not selected |
| 昌平马拉松 | TBD | — | Not selected |
| 南京全马 | 2026-11-22 Sun | Full | Not selected, on waitlist (候补中) |

Scheduling flag: 北京马拉松 (full) on 10-18 is only 13 days before the 10-31
half-marathon window and adjacent to other October races — a full marathon here
conflicts with an HM peak. The two cannot both be "all-out" races.

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

- `report/2026-09-17-multidimensional-training-analysis.html` — deep analysis;
  section 8 holds the goal ladder, section 10 the current-week training advice.
- `report/2026-09-17-race-registration-tracker.html` — race-status snapshot.
