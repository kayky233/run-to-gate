# Wayfinder trial — matrix multiply series task

This folder is a local-Markdown Wayfinder tracker for the attached CANN matrix-multiply-series task.

## What this is

Wayfinder is intentionally a planning flow. This charting pass creates a destination, initial frontier, decision tickets, blocking edges, fog, and scope boundaries. It does **not** implement production Ascend C code.

## How to continue correctly

In the next Wayfinder invocation, load `map.md` and resolve **one frontier ticket** (except research tickets, which may run in parallel). After resolving a ticket:

1. record the resolution in that ticket;
2. mark it closed;
3. append a one-line pointer under `map.md -> Decisions so far`;
4. graduate newly specifiable fog into new tickets and wire dependencies;
5. stop after one non-research ticket.

When no open tickets and no in-scope fog remain, hand the cleared map to `/to-spec`, then `/to-tickets`, then implementation.

## Recommended next move

Resolve the three AFK research tickets in parallel while the human settles **Freeze the delivery baseline and repository contract**:

- Reconcile the supplied acceptance bundle with the current precision standard
- Establish the Atlas A2 complex64 compute capability envelope
- Confirm community-task deliverables and upstream submission path
