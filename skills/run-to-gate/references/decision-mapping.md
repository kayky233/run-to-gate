# Decision mapping

This phase adapts Wayfinder's core idea: **find the route before charging at the destination**. It is planning evidence, not a disguised implementation backlog.

## Destination

Write one or two lines describing what becomes true when the map is clear. The destination fixes the scope. Examples:

- a specification with no unresolved architecture or acceptance decisions;
- a migration decision and proof plan;
- a delivery route to a green pull request.

## Canonical map

```markdown
## Destination

## Notes

## Decisions so far

- `Decision title → <artifact-or-issue-pointer>: one-line gist`

## Not yet specified

## Out of scope
```

The map is an index. Detailed evidence and rationale live in the decision ticket/artifact; the map links to them rather than duplicating them.

## Decision tickets

Each ticket resolves one question sized to one fresh context.

Types:

- **Research — autonomous:** external documentation, repository archaeology, standards, issue history, data, benchmarks, or experiments needed to establish facts.
- **Prototype — autonomous evidence, human choice only when material:** a cheap reversible artifact that makes alternatives concrete.
- **Grilling — human decision:** a live choice only the responsible human can make.
- **Manual action — human action:** credentials, browser-only setup, device/physical validation, or platform confirmation that unblocks evidence. It is not a design decision.

## Frontier and blockers

A ticket is unblocked when every ticket or gate that genuinely prevents it is resolved. The **frontier** is the open, unblocked, unclaimed work.

Rules:

- claim before mutating shared state;
- execute autonomous frontier work without asking;
- keep independent work moving even when another branch waits for a gate;
- create tickets first, then wire dependencies after stable IDs exist;
- do not encode mere preference/order as a blocker.

## Fog of war

Use **Not yet specified** only when a future question is visible but cannot yet be stated precisely. Graduate fog into one or more tickets as evidence makes the question sharp. Never keep the same concern in both fog and a live ticket.

## Out of scope

Work beyond the destination is not fog. Record it with the reason. If an existing ticket is discovered to sit beyond the destination, close/cancel it as out-of-scope and do not count it as a decision made along the route.

## Resolve a ticket

1. Load the low-resolution map and the selected ticket.
2. Claim it.
3. Gather only the context needed to answer it.
4. Produce a decision, evidence artifact, or completed manual action.
5. Record the resolution in one authoritative place.
6. Append a one-line pointer to Decisions so far when it is a route decision.
7. Add newly visible tickets, update blockers, and clear graduated fog.
8. Recompute the frontier and continue.

## Map-clear criterion

The map is clear when no unresolved product, public contract, architecture, scope, acceptance, security, irreversible, or delivery decision is required before specification and implementation. Unknown implementation details that are reversible and testable do not keep the map open.
