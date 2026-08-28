# Wayfinder blocking graph

```text
Freeze delivery baseline ───────────────┬─> Lock public API semantics ────────┐
                                        │                                     │
                                        └─────────────────────────────────────┼──────────────┐
                                                                              │              │
A2 complex compute envelope ────────────┬─> Choose shared architecture ───────┤              │
                                        │                                     │              │
                                        └─> Settle triangular/Hermitian ──────┘              │
                                                                                              v
Reconcile acceptance bundle ─────────────────────────────────────────────────────> Lock test/proof plan
                                                                                              ^
Choose shared architecture + triangular strategy ─> Define performance budget ───────────────┘

Confirm delivery path ───────────────────────────────────────────────────────────────┐
Freeze delivery baseline ────────────────────────────────────────────────────────────┤
Choose shared architecture ──────────────────────────────────────────────────────────┤
Lock test/proof plan ─────────────────────────────────────────────────────────────────┴─> Decide upstream integration shape
```

## Initial frontier

- Freeze the delivery baseline and repository contract — grilling / HITL
- Reconcile the supplied acceptance bundle with the current precision standard — research / AFK
- Establish the Atlas A2 complex64 compute capability envelope — research / AFK
- Confirm community-task deliverables and upstream submission path — research / AFK

## Blocked

- Lock the five public API and edge-case semantics
- Choose the shared operator architecture boundary
- Settle triangular, symmetric, and Hermitian dataflow strategy
- Define per-stage performance budgets against A100 acceptance targets
- Lock the implementation proof and acceptance-test plan
- Decide upstream integration and PR shape
