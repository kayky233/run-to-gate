# Lock the five public API and edge-case semantics

Label: `wayfinder:research`
Mode: AFK
Status: blocked
Blocked by: Freeze the delivery baseline and repository contract

## Question

For the frozen ops-blas baseline, what are the exact public signatures, enum values, pointer/value conventions, quick-return behavior, leading-dimension validation, null-pointer precedence, and triangular-storage semantics for CHEMM, CHER2K, CHERK, CSYMM, and CSYRK so they align with BLAS/cuBLAS and current repository conventions?

The answer must be explicit enough to derive host-side validation tests without interpretation.
