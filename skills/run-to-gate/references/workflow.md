# Workflow state machine

## Phases

```text
bootstrap → intake → decision_mapping → specification → ticketing
          → execution → verification → review → pull_request → completed
```

Verification and review may route back to execution. Pull-request CI may route back to execution or verification. Any active phase may be paused by a blocking decision/action gate or cancelled by explicit instruction.

A phase says **where the work is**. `run_status` says **whether the agent may proceed**. Phase completion never implies a pause.

## Run statuses

- `active`
- `waiting_for_human`
- `waiting_for_action`
- `waiting_for_external_check`
- `waiting_for_merge`
- `completed`
- `cancelled`

Legacy states may use `waiting_for_access`; treat it as `waiting_for_action` and migrate on the next write.

## Phase artifacts and exits

### bootstrap

**Artifacts:** capability inventory, repository contract, base ref, isolated branch/worktree, initialized durable state.

**Exit:** task source, outcome, baseline, project rules, mutation boundary, and delivery stop are known. Safe isolation exists or an exact action gate explains why it cannot.

### intake

**Artifacts:** outcome, scope, constraints, acceptance criteria, assumptions, target environment, delivery stop.

**Exit to decision mapping:** at least one material decision remains, or the effort spans more than one fresh context.

**Exit to specification:** the route is already clear and no material pre-implementation decision remains.

### decision_mapping

**Artifacts:** destination, decision map, autonomous/human ticket types, blockers, decisions so far, fog, out-of-scope list, evidence.

**Rules:**

- a decision ticket asks a precise question; it is not an implementation slice;
- a precise but blocked question is still a ticket;
- a question that cannot yet be stated precisely remains fog;
- independent autonomous research can run concurrently;
- prototypes exist to produce decision evidence, not production deliverables;
- continue independent frontier work even while another ticket awaits a gate.

**Exit:** no unresolved material decision is required before specification and implementation.

### specification

**Artifacts:** `spec.md`; traceability from each requirement and acceptance criterion to decisions and sources.

**Exit:** behavior and non-functional requirements are testable; domain terms and invariants are explicit; public interfaces and compatibility are settled; test seams and proof criteria are defined; out-of-scope is explicit.

### ticketing

**Artifacts:** one file/issue per tracer-bullet ticket, blocker graph, acceptance criteria, context pointers, current frontier.

**Quality test:**

- vertical, not layer-by-layer;
- independently demonstrable or verifiable;
- fits a fresh context;
- no hidden material decision;
- blockers are genuine gates, not ordering preferences;
- every spec requirement maps to tickets and every ticket maps to the spec;
- wide mechanical refactors use expand–migrate–contract when slices cannot stay green.

**Exit:** a complete executable graph exists and at least one frontier ticket is ready, unless a recorded gate blocks all work.

### execution

**Artifacts per ticket:** claim/owner, context pointers, failing test or repro when applicable, implementation, narrow/full checks, commit, evidence, final status.

**Exit:** no ready ticket and no ticket blocked by incomplete work remains. A failed ticket must have a diagnosis artifact or open gate; it may not disappear from the graph.

### verification

**Artifacts:** acceptance matrix, exact commands, environment/tool versions, logs, reports, benchmarks/profiles, deviations.

**Exit to review:** all mandatory criteria pass in the recorded target environment.

**Route to execution:** a defect has a reproducible fix path that does not alter a settled decision.

**Open gate:** satisfying the criterion requires changing contract, architecture, scope, target, risk, or acceptance threshold.

**Partial environment:** record a candidate/handoff status; never label simulation or incomplete hardware evidence as final acceptance.

### review

Run independent Spec and Standards axes. Add security/performance review when material.

**Exit to pull request:** no unresolved blocking finding; deterministic findings are fixed and reverified.

**Route to execution:** code-only fix.

**Open gate:** the finding contradicts settled decisions or requires material judgment.

### pull_request

**Artifacts:** updated branch, conflict-resolution evidence, pushed commits, PR body, CI status, review handoff.

**Exit to completed:** the requested stop is a green review-ready PR and all required checks are green.

**Open gate:** merge, release, production deployment, or another reserved irreversible action.

### completed

The completion report and evidence ledger are final, state validates, and no in-scope ticket or gate remains unresolved. Use `waiting_for_merge` instead when the engineering outcome is complete but human merge is intentionally outstanding.
