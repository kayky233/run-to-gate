# Lock the implementation proof and acceptance-test plan

Label: `wayfinder:grilling`
Mode: HITL
Status: blocked
Blocked by: Reconcile the supplied acceptance bundle with the current precision standard; Lock the five public API and edge-case semantics; Define per-stage performance budgets against A100 acceptance targets

## Question

What exact test matrix and evidence package will constitute “ready for acceptance” for all five operators on the frozen A2 baseline?

The decision must settle:

- mandatory smoke, functional, boundary, generalized-shape, leading-dimension, triangular-preservation, and null-pointer cases;
- mixed-tolerance handling of real/imag components;
- kernel-only vs end-to-end performance measurements and which one is used for the official comparison;
- minimum repeat/warm-up methodology;
- required logs/screenshots/tables for the self-test report.
