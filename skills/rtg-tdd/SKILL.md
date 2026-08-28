---
name: rtg-tdd
description: "Implement a Run to Gate ticket through behavioral red-to-green slices at stable public seams, with independent oracles and project-level verification."
license: MIT
metadata:
  version: "1.0.0"
  family: "run-to-gate-companion"
---

# RTG TDD

1. Identify the highest existing stable seam that proves the ticket's observable behavior.
2. Use repository precedent. A new or moved public seam is a decision, not a testing convenience.
3. Write one failing behavioral test with an independent expected value.
4. Run it and record red evidence.
5. Implement only enough to pass.
6. Run it and record green evidence.
7. Repeat as narrow vertical slices; keep refactors green.
8. Run affected package/module checks and required project checks before completing the ticket.

Avoid implementation-coupled mocks, private-method tests, tautological expected values, speculative cases, and horizontal “all tests first” plans. Never weaken mandatory acceptance to obtain green.
