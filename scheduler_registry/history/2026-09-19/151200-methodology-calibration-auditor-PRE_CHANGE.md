# PRE_CHANGE — temporary hourly methodology calibration cadence

- timestamp: 2026-09-19T15:12:00+09:00
- status: PRE_CHANGE
- title: `SparkBrain Methodology Calibration Auditor`
- requested_by: human
- reason: temporarily increase methodology-calibration audit frequency to once per hour.
- temporary: true
- revert_condition: no automatic end time was specified; retain hourly cadence until a later explicit instruction or an authorized prospective scheduler decision changes it.

## Before

```ical
BEGIN:VEVENT
DTSTART;TZID=Asia/Tokyo:20260919T172020
RRULE:FREQ=DAILY;BYHOUR=5,11,17,23;BYMINUTE=20;BYSECOND=0
END:VEVENT
```

## Intended after

```ical
BEGIN:VEVENT
DTSTART;TZID=Asia/Tokyo:20260919T162000
RRULE:FREQ=HOURLY;BYMINUTE=20;BYSECOND=0
END:VEVENT
```

Prompt, title, enabled state, timezone, role semantics, and scientific authority remain unchanged.
