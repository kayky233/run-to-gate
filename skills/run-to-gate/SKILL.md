---
name: run-to-gate
description: "Continue a software delivery effort autonomously from a task, issue, specification, plan, or Wayfinder map. Persist state; research, resolve decision fog, specify, create tracer-bullet tickets, implement, test, diagnose, review, repair CI, and prepare a pull request. Stop only at a genuine human decision or action gate, then resume automatically after the gate is cleared."
license: MIT
compatibility: "Requires project read access. Implementation requires write and command execution. Pull-request delivery additionally requires git remote, CI, and pull-request access."
metadata:
  version: "1.0.0"
  family: "engineering-orchestrator"
  mode: "run-to-gate"
---

# Run to Gate

**人类负责关键决策，AI 负责持续推进。**

One invocation starts a durable delivery loop. Continue across research, planning, specification, ticketing, implementation, verification, review, and pull-request preparation. A phase boundary is never a reason to stop. Stop only when:

1. a genuine human decision is required;
2. a human-only action is required and no independent work remains;
3. the recorded outcome is complete;
4. the user cancels the run.

Read only the reference needed by the current branch:

- [workflow.md](references/workflow.md) — phase state machine and exit criteria.
- [decision-mapping.md](references/decision-mapping.md) — destination, fog, decision tickets, blockers, and frontier.
- [decision-gates.md](references/decision-gates.md) — what belongs to the human and how to ask.
- [execution-policy.md](references/execution-policy.md) — authority, repository discipline, security, and evidence.
- [test-and-proof.md](references/test-and-proof.md) — seams, TDD, acceptance evidence, and performance proof.
- [diagnosis.md](references/diagnosis.md) — tight feedback loops, hypotheses, instrumentation, and regression tests.
- [review-and-integration.md](references/review-and-integration.md) — two-axis review, merge conflicts, PR, and CI.
- [failure-routing.md](references/failure-routing.md) — deterministic routing for failures and missing capability.
- [state-schema.md](references/state-schema.md) — durable state and `flowctl.py` usage.
- [companion-skills.md](references/companion-skills.md) — optional modular helpers bundled with this package.

## Operating contract

1. **Outcome over ceremony.** Drive toward observable acceptance criteria. Do not pause to announce that a phase finished.
2. **Investigate before asking.** Read the task, repository instructions, ADRs, issue history, tests, CI, and authoritative documentation. Never ask for a fact available through tools.
3. **Human judgment is scarce.** Escalate only choices that materially change product behavior, public contract, architecture, scope, acceptance, security, committed cost, irreversible effects, or merge/release authority.
4. **Reversible engineering is delegated.** Choose implementation details, ticket shape, test cases at established seams, diagnostics, refactors, commit grouping, PR wording, and deterministic review fixes autonomously.
5. **One durable truth.** Persist the run under `.agent-flow/<flow-slug>/`. A fresh session must resume from state and artifacts, not from conversation memory.
6. **Evidence before claims.** Record exact commands, environments, outputs, artifacts, commits, and URLs. Plausible code is not completed code.
7. **Safe delivery.** Work on an isolated branch or worktree. Do not force-push, merge, release, deploy to production, rotate credentials, delete durable data, or expand security boundaries without the corresponding gate.
8. **Automatic resumption.** After a gate answer or manual-action result is recorded, recompute the frontier and continue without asking the user to invoke another phase or skill.

## Bootstrap

Before modifying project files:

1. Locate the project and task source. Read project-local agent instructions, contributing rules, ADRs, build scripts, tests, CI, and issue-tracker conventions when present.
2. Inspect repository status, current branch, base ref, remotes, and unrelated work. Preserve user changes.
3. Classify available capability:
   - **Planning:** read/search only.
   - **Implementation:** read/write/run plus local git.
   - **Delivery:** implementation plus push, CI, and pull-request tools.
4. Initialize `.agent-flow/<flow-slug>/` with state, map, spec, decisions, tickets, evidence, and completion report. Use `scripts/flowctl.py` when executable.
5. Establish an isolated feature branch or worktree. An ambiguous dirty tree is a gate only when safe isolation cannot be established.
6. Record the stop condition. Default: green pull request ready for human merge; never merge or release by default.

Bootstrap is complete when the task source, outcome, repository contract, baseline, capability tier, and safe mutation boundary are recorded.

## Run-to-gate loop

Repeat until complete or cancelled:

1. Load `state.json`; orient to outcome, phase, open gates, current frontier, and latest evidence.
2. Reconcile state with the actual repository and remote status. State is durable, not infallible.
3. Execute every safe, unblocked action available in the current phase. Parallelize independent read-only work; parallelize mutations only with isolated ownership and a safe integration plan.
4. Record phase transitions, decisions, commands, artifacts, ticket status, commits, and evidence immediately.
5. Route failures through [failure-routing.md](references/failure-routing.md). Repeating an unchanged failed action is not progress.
6. Recompute blockers and frontier.
7. If independent work remains, continue even when another branch is waiting on a gate.
8. Present one consolidated gate only when all remaining progress is blocked. Use [decision-request.template.md](assets/decision-request.template.md) or [manual-action.template.md](assets/manual-action.template.md), then stop.
9. After the gate clears, record it and resume at step 1.

## Phase router

Use [workflow.md](references/workflow.md) for full exit criteria.

### Intake

Extract the outcome, in-scope behavior, constraints, acceptance criteria, frozen baseline, target environment, and delivery stop. Mark assumptions and verify unstable facts. If material decision fog remains or the effort exceeds one fresh context, enter decision mapping; otherwise proceed to specification.

### Decision mapping

Use the semantics in [decision-mapping.md](references/decision-mapping.md): name the destination, create precise decision tickets, distinguish autonomous work from human judgment, wire blockers, and retain only genuinely unformulated questions as fog.

Resolve research, analysis, repository archaeology, benchmarks, and throwaway prototypes autonomously. Human participation is required only to select among materially different valid options. The map is clear when implementation no longer depends on an unresolved product-, contract-, architecture-, scope-, acceptance-, security-, or delivery-level decision.

### Specification

Synthesize settled decisions into a testable specification. Do not reopen decisions without new contradicting evidence. Define behavior, public interfaces, invariants, error handling, compatibility/migration, observability, resource requirements, acceptance criteria, and test seams.

Choose existing public seams autonomously. Open a gate only when the work creates or moves a public seam, changes the contract, or trades materially different proof strength against cost/risk.

### Ticketing

Create dependency-aware **tracer-bullet vertical slices**. Each ticket must:

- fit a fresh agent context;
- deliver one narrow but complete behavior;
- be independently demonstrable or verifiable;
- declare genuine blockers;
- contain acceptance criteria and context pointers;
- avoid hidden product or architecture decisions.

Ticket granularity and ordering are delegated. Do not ask for routine approval. Wide mechanical refactors use expand–migrate–contract when a vertical slice cannot stay green.

### Execution

Work the frontier until empty:

1. Claim one ticket and record ownership.
2. Load only its relevant spec, decisions, prior art, and code.
3. Prefer one behavioral red → green slice at a time at an established seam.
4. Implement the smallest coherent change that satisfies the ticket.
5. Run narrow checks frequently and project-required checks before completion.
6. Commit a coherent green slice with traceability.
7. Attach evidence, mark done, recompute frontier, and continue.

Never weaken the spec or acceptance criteria to make implementation easier. A required behavior change returns to a decision gate.

### Verification and diagnosis

Run the full acceptance matrix and record exact evidence. On failure, build a fast deterministic command that catches the exact symptom, minimize it, rank falsifiable hypotheses, instrument one prediction at a time, fix, add a regression test at the correct seam, remove instrumentation, and rerun the original scenario.

Performance work starts with a reproducible benchmark and profiler evidence. Simulated or partial environments may produce a candidate, but may not be represented as final target-environment acceptance.

### Review

Review the complete diff independently against:

- **Spec:** missing, partial, wrong, or unrequested behavior.
- **Standards:** repository rules, security, maintainability, and relevant code smells.

Fix deterministic findings autonomously and rerun checks. Escalate only findings that require product, architecture, scope, acceptance, security, or irreversible judgment.

### Pull request and CI

Safely update from the frozen base, resolve conflicts by preserving source intent, rerun checks, push the feature branch, and create or update the pull request with traceable decisions, tickets, tests, benchmarks, risks, and residual limitations. Monitor CI when tools permit and repair failures within policy budgets.

Preparing a green reviewable pull request is autonomous. Merge, release, and production deployment remain human gates unless explicitly delegated by recorded policy.

## Completion contract

The run may be marked complete only when all applicable conditions hold:

- every in-scope ticket is done or explicitly ruled out by a recorded decision;
- acceptance criteria pass on the recorded target environment, or the state is explicitly a partial-environment handoff rather than final acceptance;
- required static checks, tests, and benchmarks pass;
- no unresolved blocking review finding remains;
- temporary instrumentation and throwaway artifacts are removed or quarantined;
- commits are coherent and the branch is pushed when delivery access exists;
- the pull request or handoff package contains reproducible evidence;
- `.agent-flow/<flow-slug>/completion.md` is written from the completion template;
- state validation passes;
- state becomes `completed`, or `waiting_for_merge` when human merge is deliberately outside the outcome.

When tools cannot reach the required capability tier, complete everything independently possible, produce an exact handoff with a resume condition, and state the missing action without claiming it occurred.
