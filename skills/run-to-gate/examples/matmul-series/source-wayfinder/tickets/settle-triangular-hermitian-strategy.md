# Settle triangular, symmetric, and Hermitian dataflow strategy

Label: `wayfinder:prototype`
Mode: HITL
Status: blocked
Blocked by: Establish the Atlas A2 complex64 compute capability envelope; Lock the five public API and edge-case semantics

## Question

What dataflow should reconstruct/read only the declared triangle of A or update only the declared triangle of C while preserving correctness and minimizing A2 memory traffic?

The prototype must compare at least:

- full materialization of symmetric/Hermitian matrices before GEMM;
- on-the-fly mirrored/conjugated tile generation;
- triangular-aware output filtering/fused writeback;
- handling Hermitian diagonal imaginary parts.

The artifact is throwaway evidence to choose the behavior, not production code.
