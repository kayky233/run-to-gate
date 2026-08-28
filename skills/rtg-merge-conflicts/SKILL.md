---
name: rtg-merge-conflicts
description: "Resolve an in-progress merge or rebase for Run to Gate by preserving the primary source intents, completing the operation, and re-verifying affected behavior."
license: MIT
metadata:
  version: "1.0.0"
  family: "run-to-gate-companion"
---

# RTG Merge Conflicts

1. Inspect merge/rebase state, history, and every conflicting file.
2. Read primary sources for both sides: commits, issues, specs, decisions, and tests.
3. Resolve each hunk by preserving both intents where compatible.
4. Where incompatible, choose the intent matching the recorded destination, frozen contract, and later authoritative decision.
5. Do not invent unrelated new behavior during resolution.
6. Stage changes, run affected checks and required project checks, then continue until the merge/rebase is finished.
7. Record trade-offs and verification evidence.

Do not abort merely because conflicts are difficult. Open a human gate only when two settled human decisions genuinely conflict.
