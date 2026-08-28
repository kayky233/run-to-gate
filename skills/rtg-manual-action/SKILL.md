---
name: rtg-manual-action
description: "Turn a human-only Run to Gate action—credential entry, private dashboard setup, device validation, physical step, or platform confirmation—into a minimal safe wizard/checklist with exact resume evidence."
license: MIT
metadata:
  version: "1.0.0"
  family: "run-to-gate-companion"
---

# RTG Manual Action

Use only for actions the agent cannot perform. It is not a substitute for agent research or execution.

1. Read project configuration and determine the exact missing action and values.
2. Minimize the human steps and continue all independent work first.
3. Provide ordered commands/URLs, expected screen/response, verification, and rollback where relevant.
4. Mark secrets; request hidden/private entry and never ask the human to paste secrets into chat.
5. Require confirmation before destructive, paid, security-sensitive, or irreversible actions.
6. Define the exact redacted evidence/file that should be returned and the observable resume condition.
7. Prefer idempotent steps and safe re-runs.

The output is complete when a person unfamiliar with prior conversation can perform the action safely and return enough evidence for automatic resumption.
