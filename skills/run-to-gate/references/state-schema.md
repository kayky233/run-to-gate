# Durable state

The canonical local state is `.agent-flow/<slug>/state.json` with supporting artifacts:

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

An issue tracker may mirror maps and tickets, but state retains stable IDs/URLs so a fresh context can resume.

## Required concepts

- flow identity, source, outcome, phase, run status, revision, timestamps;
- repository root, base ref, feature branch/worktree, head commit;
- capability tier and available tools;
- policy and loop budgets;
- decision/action gates with blockers, status, answer/evidence, and resume condition;
- tickets with blockers, owner, status, acceptance, commits, and evidence;
- evidence ledger;
- event history and current frontier.

## `flowctl.py`

The bundled standard-library script writes atomically and appends events.

```bash
python scripts/flowctl.py init \
  --slug my-feature \
  --title "My feature" \
  --source "issue #123" \
  --outcome "green PR ready for human merge" \
  --repo-root . \
  --base-ref origin/main

python scripts/flowctl.py status --state .agent-flow/my-feature/state.json
python scripts/flowctl.py set-phase --state ... --phase decision_mapping

python scripts/flowctl.py open-gate --state ... \
  --kind architecture \
  --question "Which compatibility contract is authoritative?" \
  --recommendation "Freeze release/2.1 because it matches acceptance." \
  --blocks "T-004,T-005"

python scripts/flowctl.py resolve-gate --state ... \
  --id D-001 --answer "Use release/2.1" --selected-option release-2.1

python scripts/flowctl.py add-ticket --state ... \
  --id T-001 --title "Deliver one end-to-end slice" \
  --acceptance "Public call returns expected result" \
  --acceptance "Focused and project checks pass"

python scripts/flowctl.py ticket-status --state ... \
  --id T-001 --status done --commit abc123

python scripts/flowctl.py frontier --state ...
python scripts/flowctl.py add-evidence --state ... \
  --kind test --summary "Focused and full suite pass" \
  --command "pytest tests/test_feature.py && pytest" --exit-code 0
python scripts/flowctl.py validate --state ...
```

Every mutation increments `revision`. Use `--expected-revision` for optimistic concurrency.

## Resume protocol

A fresh session loads only:

1. compact `state.json` status and frontier;
2. the current ticket or blocking gate;
3. linked spec/decision sections and relevant project files;
4. evidence needed for the next transition.

Do not replay the entire conversation. Durable artifacts are the context pointers. Reconcile the stored branch/head/remote status with reality before mutating.
