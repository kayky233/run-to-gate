---
name: rtg-review
description: "Review a Run to Gate diff independently against the settled specification and repository standards, fix deterministic findings, and return separate evidence for both axes."
license: MIT
metadata:
  version: "1.0.0"
  family: "run-to-gate-companion"
---

# RTG Review

Pin the fixed point/merge-base and inspect the complete diff and commit list.

## Spec axis

Find missing, partial, wrong, or unrequested behavior; acceptance without proof; compatibility/migration errors. Cite the originating requirement or decision.

## Standards axis

Find violations of repository rules, security/reliability defects, and maintainability issues not already enforced by tooling. Generic smells are judgment calls; repository standards override them.

Keep the two reports separate. Fix deterministic findings autonomously, rerun narrow and full checks, then review the resulting diff again. Escalate only findings that require product, public contract, architecture, scope, acceptance, security, or irreversible judgment.

Done when both axes have explicit results, blocking findings are resolved or gated, and evidence is attached to the canonical state.
