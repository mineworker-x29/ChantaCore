# ChantaCore v0.8.8 Restore

## Version

ChantaCore v0.8.8 — Process Job FSM & Queue Conformance

## Purpose

v0.8.8 hardens the local worker queue by treating `ProcessJob` lifecycle as a
ProcessJob-specific finite state machine. It also adds lightweight queue
conformance checks under PIG so worker lifecycle traces can be inspected as
process intelligence evidence.

This is not a generic FSM framework. It does not add external FSM libraries,
daemon execution, async runtime, distributed locking, MissionLoop, GoalLoop, or
formal Petri-net conformance.

## ProcessJob FSM

The worker queue lifecycle is explicit and deterministic:

| From | Event activity | To | Worker required |
| --- | --- | --- | --- |
| `None` | `enqueue_process_job` | `queued` | No |
| `queued` | `claim_process_job` | `claimed` | Yes |
| `claimed` | `start_worker_job` | `running` | Yes |
| `running` | `complete_worker_job` | `completed` | Yes |
| `running` | `fail_worker_job` | `failed` | Yes |
| `queued` | `cancel_process_job` | `cancelled` | No |
| `claimed` | `cancel_process_job` | `cancelled` | No |
| `failed` | `retry_process_job` | `queued` | No |
| `running` | `retry_process_job` | `queued` | Yes |

Invalid transitions are rejected, including:

- `queued -> completed`
- `completed -> running`
- `cancelled -> claimed`
- `failed -> completed`

Retry behavior remains controlled by `WorkerQueueService` using
`retry_count < max_retries`.

## OCEL Trace Shape

FSM transitions are process-mining friendly `event_activity` records:

- `enqueue_process_job`
- `claim_process_job`
- `start_worker_job`
- `complete_worker_job`
- `fail_worker_job`
- `retry_process_job`
- `cancel_process_job`

Transition event attributes include:

- `from_status`
- `to_status`
- `job_id`
- `worker_id`
- `retry_count`
- `max_retries`
- `transition_valid`

When `TraceService` is supplied, worker queue transitions are written through
the existing OCEL worker lifecycle path with `process_job` and `worker` objects
where supported.

## Queue Conformance

`PIGQueueConformanceService` lives under `src/chanta_core/pig/` and provides
advisory queue lifecycle checks:

- `check_job(job_id)`
- `check_recent_jobs(limit)`
- `check_job_sequence(job, activity_sequence)`

The conformance layer checks for examples such as retry count overflow, missing
worker claims for claimed/running jobs, missing failure evidence, cancelled and
completed state conflicts, and basic lifecycle order sanity.

Queue conformance is diagnostic only. It does not block queue execution and does
not mutate worker state.

## Tool Gateway

`tool:worker` adds:

- `check_queue_conformance`

The operation returns a `ToolResult` with a queue conformance report. Existing
worker operations remain:

- `enqueue_process_run`
- `claim_next`
- `run_once`
- `queue_summary`
- `recent_jobs`
- `recent_heartbeats`

## Guardrails

v0.8.8 does not add:

- Generic FSM framework
- External FSM dependency
- Daemon
- Async runtime
- Distributed locking
- Scheduler behavior beyond existing integration
- MissionLoop or GoalLoop
- Mission object type
- Formal Petri-net conformance
- pm4py, ocpa, pandas, numpy, or networkx

## Remaining Limitations

- No generic FSM framework
- No daemon
- No distributed locking
- No formal Petri-net conformance
- No process discovery from queue variants yet
- Queue conformance is lightweight and advisory
