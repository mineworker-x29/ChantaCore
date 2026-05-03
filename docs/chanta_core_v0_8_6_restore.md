# ChantaCore v0.8.6 — Worker Queue / Background Process

## Purpose

v0.8.6 adds a lightweight local worker queue foundation to the Internal Harness Layer. It introduces process jobs, worker claim/run lifecycle, heartbeat records, and a synchronous `WorkerRunner.run_once()` surface.

This is not a scheduler, daemon, MissionLoop, or GoalLoop. Recurring/scheduled process runs remain future v0.8.7 work.

## Implemented Pieces

| Area | Component |
| --- | --- |
| Job model | `ProcessJob` |
| Job state | `ProcessJobStore` with JSONL history and state snapshot |
| Worker model | `Worker` |
| Heartbeats | `WorkerHeartbeat`, `WorkerHeartbeatStore` |
| Queue service | `WorkerQueueService` |
| Runner | `WorkerRunner.run_once()` |
| Tool gateway | `tool:worker` |
| Optional skill | `skill:run_worker_once` |

## Queue Lifecycle

Worker queue operations are local and synchronous:

1. `enqueue_process_run`
2. `claim_next`
3. `mark_running`
4. `mark_completed` or `mark_failed`
5. retry requeue when `retry_count < max_retries`
6. `cancel` when explicitly requested

The queue selects the highest priority queued job, then the earliest `created_at`, then deterministic `job_id` ordering.

## Worker Runner

`WorkerRunner.run_once()`:

- emits heartbeat records
- claims one queued job
- marks it running
- invokes `ProcessRunLoop`
- marks completed on success
- marks failed or requeued on failure

It is intentionally synchronous for unit tests and scripts. There is no async runtime, daemon service, distributed lock, or production supervisor.

## Tool Gateway

`tool:worker` is an `internal_compute` tool with operations:

- `enqueue_process_run`
- `claim_next`
- `run_once`
- `queue_summary`
- `recent_jobs`
- `recent_heartbeats`

It does not provide shell, network, MCP, plugin, scheduler, or recurring run behavior.

## OCEL Trace

Worker operations are traceable through:

- existing tool lifecycle events for `tool:worker`
- worker lifecycle events:
  - `enqueue_process_job` when used through service/tool visibility where available
  - `claim_process_job`
  - `start_worker_job`
  - `complete_worker_job`
  - `fail_worker_job`
  - `emit_worker_heartbeat`

Worker lifecycle events use `worker` and `process_job` OCEL objects when the runner has a `TraceService`.

## Guardrails

v0.8.6 does not add:

- scheduler or recurring process runs
- MissionLoop or GoalLoop
- async daemon
- worker subprocess management
- shell execution
- network/web fetch
- MCP/plugin system
- UI dashboard

## Remaining Limitations

- no daemon
- no async runtime
- no distributed locking
- no scheduler
- no recurring process runs
- no production worker supervisor
- no multi-process queue safety
