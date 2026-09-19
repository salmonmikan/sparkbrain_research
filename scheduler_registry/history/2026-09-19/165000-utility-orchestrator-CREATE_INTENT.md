# CREATE_INTENT — SparkBrain Utility Orchestrator

- timestamp: 2026-09-19T16:50:00+09:00
- status: CREATE_INTENT
- requested_by: human
- title: `SparkBrain Utility Orchestrator`
- enabled: true
- timing_mode: `exact_schedule`
- timezone: `Asia/Tokyo`
- default_cadence: hourly (maximum supported scheduler frequency)
- request_bus: `ops/utility-orchestrator-requests`

## Intended schedule

```ical
BEGIN:VEVENT
DTSTART;TZID=Asia/Tokyo:20260919T172500
RRULE:FREQ=HOURLY;BYMINUTE=25;BYSECOND=0
END:VEVENT
```

## Intended architecture

The Utility Orchestrator is the sole dynamically reconfigurable SparkBrain worker.

- All active SparkBrain schedulers may append requests to the request bus.
- Requests never grant execution authority.
- Control Brain aggregates, deduplicates, resolves conflicts, and issues the active assignment.
- Default state is IDLE.
- Default cadence is hourly.
- Assignments should normally be short-lived (1–3 runs).
- Control Brain has exceptional authority to broadly modify ONLY this Utility scheduler's prompt/role/scope/assignment authority/stop conditions and timing (never faster than hourly), with scheduler-registry transaction discipline.
- Utility itself has no authority to mutate schedulers.

## Hard floor

No reconfiguration may bypass consumed-identity/no-rerun, immutable evidence, prospective protocol, preserve-before-read/raw-before-score, held-out/evaluator leakage, or other one-way scientific-integrity constraints.
