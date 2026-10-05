# Project Analysis Rules

These rules are persistent project requirements and apply to every fitness-data analysis and generated report.

1. Use active exercise time only. For duration, pace, training load, and related calculations, fetch activity detail and use `workoutTime` (moving time), excluding manual pauses, auto-pauses, and stopped time. Do not use the activity-summary `totalTime` for these calculations and do not silently fall back to it when detail is unavailable. Use elapsed/total time only when the user explicitly requests it, and label it clearly.
2. Align all dates and times before analysis. Interpret them using the full actual Gregorian year and the project timezone (`COROS_TIMEZONE`, falling back to the system timezone). Derive and verify the weekday programmatically from the full date before presenting or comparing results. Never infer a weekday from an unchecked example or reuse a date/weekday mapping from another year.
3. When the user's stated weekday conflicts with the calendar, use the calendar-correct value and point out the correction briefly instead of silently propagating the mismatch.
4. Weekly comparisons use calendar weeks from Monday through Sunday. Keep an incomplete current week separate and label its cutoff date; never extend the previous full week or compare a partial week as if it were complete.
