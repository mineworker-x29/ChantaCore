# ChantaCore v0.8.7 — Scheduler / Mission-like Recurring Process Runs

## Purpose

v0.8.7 adds a local scheduler foundation for one-time and interval process runs. The scheduler evaluates schedules and enqueues due work as `ProcessJob` records through `WorkerQueueService`.

This is not a daemon scheduler and it is not a MissionLoop or GoalLoop. It does not introduce a mission object type. Worker execution remains separate: `SchedulerRunner` enqueues jobs, and `WorkerRunner` executes jobs later.

## Implemented Pieces

| Area | Component |
| --- | --- |
| Schedule model | `ProcessSchedule` |
| Schedule state | `ProcessScheduleStore` with JSONL history and state snapshot |
| Evaluation | `ScheduleEvaluator`, `ScheduleEvaluation` |
| Service facade | `SchedulerService` |
| Runner | `SchedulerRunner.run_once()` |
| Tool gateway | `tool:scheduler` |
| Optional skill | `skill:run_scheduler_once` |

## Supported Schedule Types

- `once`: due at or after `run_at`, then marked `completed` after enqueue.
- `interval`: due at or after `next_run_at`, then `next_run_at` advances by `interval_seconds` after enqueue.

Cron expressions are not implemented.

## Runtime Flow

The intended flow is:

1. `ProcessSchedule` is created.
2. `SchedulerRunner.run_once()` evaluates active schedules.
3. Due schedules enqueue `ProcessJob` through `WorkerQueueService`.
4. `WorkerRunner.run_once()` may later claim and execute queued jobs through `ProcessRunLoop`.

The scheduler does not execute `ProcessRunLoop` directly.

## Tool Gateway

`tool:scheduler` is an `internal_compute` gateway with operations:

- `create_once_schedule`
- `create_interval_schedule`
- `pause_schedule`
- `resume_schedule`
- `cancel_schedule`
- `list_active`
- `evaluate_due`
- `enqueue_due`
- `run_once`
- `recent_schedules`

It does not provide shell, network, MCP, plugins, cron, async, or daemon behavior.

## OCEL Trace

Scheduler actions are traceable through:

- existing `tool:scheduler` lifecycle events
- scheduler lifecycle events:
  - `create_process_schedule`
  - `evaluate_process_schedule`
  - `enqueue_scheduled_process`
  - `pause_process_schedule`
  - `resume_process_schedule`
  - `cancel_process_schedule`
  - `run_scheduler_once`

When available, schedule objects use object type `process_schedule`.

## Guardrails

v0.8.7 does not add:

- MissionLoop
- GoalLoop
- mission object type
- daemon scheduler
- async runtime
- cron dependency
- APScheduler or other external scheduler package
- shell execution
- network/web fetch
- MCP/plugin system

## Remaining Limitations

- no daemon
- no cron expression support
- no distributed locking
- no external scheduler integration
- no mission object type
- no UI
