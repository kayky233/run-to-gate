# Establish the Atlas A2 complex64 compute capability envelope

Label: `wayfinder:research`
Mode: AFK
Status: open / unclaimed

## Question

On Atlas A2 / arch22, what is the viable high-performance implementation envelope for complex64 Level-3 matrix products required by CHEMM/CHER2K/CHERK/CSYMM/CSYRK?

Resolve, with current Ascend C/API evidence and nearby ops-blas implementations:

- whether A2 Cube can be used directly for the needed FP32 real GEMMs and what data-layout transforms are required;
- whether complex multiplication should be decomposed into 4 real GEMMs, 3 real GEMMs, or another fused strategy;
- where conjugation, symmetric/Hermitian reconstruction, alpha/beta scaling, and triangular writeback should execute (AIC/Cube vs AIV/SIMD);
- workspace requirements and whether task shapes up to large dimensions fit the repo's handle-workspace model;
- which existing arch22 operators are the best implementation references.

## Resolution evidence required

A capability/constraint table plus one recommended architecture family and rejected alternatives with reasons. No production implementation in this ticket.
