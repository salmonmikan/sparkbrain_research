# CREATED / APPLIED — SparkBrain Methodology Calibration Auditor

- timestamp: 2026-09-19T13:41:00+09:00
- status: CREATED
- title: `SparkBrain Methodology Calibration Auditor`
- create-intent commit: `e94d2509b651eb966315439fe69d1834502bbd82`
- live verification: successful
- enabled: `true`
- timing_mode: `exact_schedule`
- timezone: `Asia/Tokyo`

## Schedule

```ical
BEGIN:VEVENT
DTSTART;TZID=Asia/Tokyo:20260919T172020
RRULE:FREQ=DAILY;BYHOUR=5,11,17,23;BYMINUTE=20;BYSECOND=0
END:VEVENT
```

Runs four times per day at 05:20, 11:20, 17:20, and 23:20 JST.

## Purpose

Independently audit calibration of SparkBrain's admission criteria, novelty bar, reduction requirements, comparator requirements, stop/reframe rules, and evidence thresholds.

The task is read-only and prospective-only. It may recommend tightening, relaxing, splitting, merging, or clarifying methodology gates, but it cannot itself modify science, evidence, research criteria, scheduler definitions, or consumed/frozen results.

## Durable persistence

- scheduler current definition registered under `scheduler_registry/current/`
- fleet manifest updated to eight active SparkBrain schedulers
- methodology output mailbox: `ops/methodology-calibration-audit`
- initial mailbox commit: `97c2d17c3e6b097311626cce1058e2d56e889cef`

## Registry synchronization

- current-definition commit: `c2dde59a25e1d06245dd1cd462372f92fda9590e`
- manifest commit: `1ddecce368976f4ebc6dd1a07c56b86091105fec`
- registry_status: `IN_SYNC`
