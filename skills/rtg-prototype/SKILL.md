---
name: rtg-prototype
description: "Build a cheap reversible prototype to reduce a Run to Gate product, behavior, architecture, or performance uncertainty before a material human decision."
license: MIT
metadata:
  version: "1.0.0"
  family: "run-to-gate-companion"
---

# RTG Prototype

A prototype produces decision evidence, not production delivery.

1. State the exact uncertainty and the alternatives being compared.
2. Choose the cheapest artifact that makes the difference observable: UI mock, interface stub, state machine, microbenchmark, data sample, or throwaway harness.
3. Define the observation/measurement before building.
4. Keep the prototype isolated, reversible, and clearly marked as throwaway.
5. Exercise representative and edge scenarios.
6. Record what the prototype proves, what it does not prove, and any environment limitations.
7. Summarize option trade-offs and recommend the option that best matches the recorded destination.
8. Link the artifact and evidence into the decision ticket/state. Delete or quarantine it after the decision unless the specification explicitly promotes part of it.

Do not silently turn a prototype into production code. A human is needed only to choose when multiple materially different valid options remain.
