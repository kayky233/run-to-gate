# Reconcile the supplied acceptance bundle with the current precision standard

Label: `wayfinder:research`
Mode: AFK
Status: open / unclaimed

## Question

Which parts of the supplied five-operator CSV/verification bundle are still authoritative as-is, and which must be adapted to the current ops-blas test framework and ecological mixed-tolerance precision standard without weakening the task-book acceptance intent?

The reconciliation must explicitly cover:

- CSV schema and case counts for all five operators;
- old vs current test directory layout;
- precision mode and FP32 complex real/imag comparison rules;
- triangular-output preservation semantics for HERK/HER2K/SYRK;
- Hermitian diagonal imaginary-part handling;
- null-pointer / quick-return expectations;
- `cher2k` documentation inconsistency: task book says `beta` is real float, bundled README says alpha/beta are both complex, while the CSV schema uses a single real `beta` field;
- whether arch35 commands in the bundled README are merely portability notes or intended acceptance scope.

## Resolution evidence required

A table of “keep / adapt / reject” decisions, linked to the exact frozen repo baseline and current precision standard.
