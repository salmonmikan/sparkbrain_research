# APPLIED — temporary hourly methodology calibration cadence

- timestamp: 2026-09-19T15:13:00+09:00
- status: APPLIED
- title: `SparkBrain Methodology Calibration Auditor`
- requested_by: human
- temporary: true
- automatic_revert: none specified

## Before

```ical
BEGIN:VEVENT
DTSTART;TZID=Asia/Tokyo:20260919T172020
RRULE:FREQ=DAILY;BYHOUR=5,11,17,23;BYMINUTE=20;BYSECOND=0
END:VEVENT
```

## After

```ical
BEGIN:VEVENT
DTSTART;TZID=Asia/Tokyo:20260919T162020
RRULE:FREQ=HOURLY;BYMINUTE=20;BYSECOND=0
END:VEVENT
```

The task now runs once per hour at minute :20 JST. Prompt, scientific role, permissions, enabled state, and evidence boundaries are unchanged.

- live_updated_at: `2026-09-19T06:12:30.601902Z`
- current_definition_commit: `887abc5306fa356be84a7192938461fa4cd81a4e`
- manifest_commit: `b91f13fcc235b43d51f1484923e400cb59ee175c`
