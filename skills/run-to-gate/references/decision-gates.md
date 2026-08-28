# Human gates

## Gate test

Escalate a choice only when all are true:

1. It is not already fixed by the task, repository contract, ADR, standard, or recorded decision.
2. Investigation and reversible experiments cannot collapse the options to one valid answer.
3. The options materially differ in observable behavior, public contract, architecture, scope, acceptance, security/privacy, committed cost, irreversible effect, or ownership.
4. Choosing a default without consent would be difficult or expensive to reverse.

Otherwise choose the best reversible option, record the rationale, and continue.

## Human-owned decisions

- destination and in/out-of-scope boundary;
- user-visible behavior;
- public API, schema, compatibility, migration semantics, or externally committed protocol;
- architecture with material performance, operability, complexity, ownership, or long-term cost trade-offs;
- acceptance thresholds and evidence policy;
- security/privacy boundaries, permission expansion, credentials, paid-resource commitments;
- repository-policy exceptions;
- destructive or irreversible production actions;
- merge, release, or production deployment unless explicitly delegated.

## Agent-owned choices

- repository exploration and source-first research;
- exact internal file layout within established conventions;
- ticket granularity and dependency ordering;
- internal naming and reversible refactoring;
- test cases and fixtures at an established seam;
- implementation technique within a settled architecture;
- instrumentation, profiling, and debugging method;
- deterministic review fixes;
- commit grouping, PR drafting, push, and CI repair within policy.

## Human action is not human judgment

Credentials, browser-only setup, device access, physical validation, platform confirmation, or inaccessible private systems may require a person without requiring a design decision. Classify these as action gates:

- minimize the human steps;
- give exact commands/URLs and expected evidence;
- never request a secret in chat;
- continue independent work first;
- stop only when all remaining progress depends on the action;
- resume automatically when evidence is supplied.

## Gate request quality

A decision request contains:

- stable ID and exact blockers;
- one independently answerable question;
- evidence already gathered;
- 2–4 genuinely distinct options;
- effects on behavior, performance/cost, risk, schedule, and reversibility;
- one recommended option;
- compact reply syntax.

Batch independent gates in one message only when each remains separately answerable. Never hide several decisions in one compound choice. Never include questions the agent can answer.

## After a gate clears

1. Record the verbatim response and normalized result.
2. Update invalidated or unlocked map/spec/tickets.
3. Reconcile state with the repository.
4. Recompute the frontier.
5. Resume immediately; do not ask for another invocation.
