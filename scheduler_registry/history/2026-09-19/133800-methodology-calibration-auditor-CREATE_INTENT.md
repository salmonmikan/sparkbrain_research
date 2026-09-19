# CREATE_INTENT — SparkBrain Methodology Calibration Auditor

- timestamp: 2026-09-19T13:38:00+09:00
- status: PRE_CHANGE / CREATE_INTENT
- requested_by: human
- purpose: independently audit whether SparkBrain's increasingly strict research-validation criteria are themselves scientifically well calibrated.
- proposed_title: `SparkBrain Methodology Calibration Auditor`
- proposed_timing_mode: `exact_schedule`
- timezone: `Asia/Tokyo`

## Proposed schedule

Four runs per day, intentionally offset from Evidence Analyst (:00), MAIN (:15), literature/audit (:30), SUB (:35), Relay (:45), and Control/Steward (:50).

```ical
BEGIN:VEVENT
DTSTART;TZID=Asia/Tokyo:20260919T172000
RRULE:FREQ=DAILY;BYHOUR=5,11,17,23;BYMINUTE=20;BYSECOND=0
END:VEVENT
```

## Proposed authority

Read-only methodology/governance audit. It may recommend prospective tightening, relaxation, separation, or redesign of research gates, but may not itself modify scientific criteria, scheduler definitions, experiments, identities, evidence, branches, tags, PRs, or formal outcomes.

## Required audit dimensions

- historical gate/novelty-bar drift;
- evidence supporting each newly added gate;
- false-positive versus false-negative tradeoff;
- duplicated or overlapping safeguards;
- moving-goalpost/post-outcome risk;
- whether PASS has become practically unreachable;
- whether comparator matching is scientifically appropriate rather than merely maximally restrictive;
- separation of novelty, mechanistic distinctness, engineering value, and research-worthiness;
- whether architecture/testbed questions are being rejected merely because they do not establish a new computational principle;
- calibration against current external literature and prior SparkBrain outcomes.

The created task ID must be obtained from the live scheduler service after creation; no ID is preassigned here.
