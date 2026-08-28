---
name: rtg-diagnose
description: "Diagnose a hard bug, flaky failure, CI-only failure, or performance regression for Run to Gate by building a tight red-capable loop, testing falsifiable hypotheses, and locking the fix with evidence."
license: MIT
metadata:
  version: "1.0.0"
  family: "run-to-gate-companion"
---

# RTG Diagnose

1. Build one fast deterministic command that catches the exact symptom. Do this before theorizing.
2. Raise reproduction probability for flaky failures; do not rerun until lucky.
3. Minimize the scenario until every remaining element is load-bearing.
4. Rank 3–5 falsifiable hypotheses, each with an observable prediction.
5. Instrument one prediction at a time. Prefer debugger/profiler to broad logging; tag temporary instrumentation.
6. Add a regression test at the correct seam before the fix when such a seam exists.
7. Apply the smallest fix, observe green, and rerun the original unminimized scenario.
8. Run affected and project checks; remove instrumentation and throwaway harnesses.
9. Record root cause, evidence, command, environment, commit, and residual risk.

If no valid loop can be built, report attempts and request the smallest missing artifact/access. Do not guess a cause.
