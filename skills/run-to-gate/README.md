# Run to Gate

**Run to Gate：人类负责关键决策，AI 负责持续推进。**

`run-to-gate` turns a task, issue, specification, plan, or Wayfinder map into a durable end-to-end engineering run:

```text
Task / Issue / Plan / Wayfinder Map
                │
                ▼
      Research + Decision Map
                │
      Material human choice? ── yes ──> concise gate
                │ no                         │
                ▼                            └── answer → automatic resume
              Spec
                ▼
       Tracer-bullet tickets
                ▼
       Implement + test
                ▼
  Verify / diagnose / benchmark
                ▼
       Two-axis review
                ▼
       PR + CI repair
                ▼
       Human merge/release gate
```

## Key behavior

- does not stop at phase boundaries;
- investigates before asking;
- delegates reversible engineering choices to AI;
- asks humans only for material decisions or unavoidable human-only actions;
- persists map, state, spec, tickets, decisions, evidence, and completion report;
- resumes automatically after a gate clears;
- never represents simulated/partial evidence as final target-environment acceptance;
- stops before merge, release, or production deployment by default.

## Install the main skill

The distribution bundle contains:

```text
install/run-to-gate.zip
```

Upload that ZIP to a client that accepts one Agent Skill archive, or copy `skills/run-to-gate/` into an Agent Skills-compatible skill directory.

The main skill is self-contained. Optional companion skills are included for clients that support modular multi-skill installation, but the run must never fail because a companion is missing.

## Start a run

```text
@Run to Gate

Use this task and repository.
Outcome: prepare a green pull request ready for human merge.
Ask me only for product behavior, public contract, architecture trade-offs,
scope/acceptance changes, security/credentials, irreversible actions, and merge/release.
Choose reversible implementation details, ticket breakdown, tests at existing seams,
debugging methods, review fixes, commits, push, PR, and CI repairs autonomously.
Persist state and resume from it. Do not stop at phase boundaries.
```

## Continue an existing decision map

```text
@Run to Gate

Continue the existing Wayfinder map and durable state.
Preserve recorded decisions and blockers.
Run all autonomous frontier work, stop only at a true gate, and after the map clears
continue through spec, tickets, implementation, verification, review, and PR.
```

## Capability tiers

| Tier | Available capability | Maximum honest outcome |
|---|---|---|
| Planning | project/file read and search | decision map, specification, tickets, exact handoff |
| Implementation | read, write, command execution, local git | tested commits on an isolated branch |
| Delivery | implementation plus push, CI, and PR access | green pull request ready for human merge |

When a required environment is unavailable, the skill continues everything independent of it and records a precise resume action. A candidate produced in simulation remains a candidate until the target acceptance environment passes.

## Durable workspace

```text
.agent-flow/<slug>/
├── state.json
├── map.md
├── spec.md
├── completion.md
├── decisions/
├── tickets/
└── evidence/
```

`scripts/flowctl.py` provides atomic state updates, frontier calculation, gates, tickets, evidence, validation, and optimistic concurrency.

## Package contents

```text
run-to-gate/
├── SKILL.md
├── README.md
├── LICENSE
├── NOTICE.md
├── references/
├── assets/
├── scripts/
├── tests/
└── examples/
```
