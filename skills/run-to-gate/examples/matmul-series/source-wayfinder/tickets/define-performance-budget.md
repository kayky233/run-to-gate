# Define per-stage performance budgets against A100 acceptance targets

Label: `wayfinder:research`
Mode: AFK
Status: blocked
Blocked by: Establish the Atlas A2 complex64 compute capability envelope; Choose the shared operator architecture boundary; Settle triangular, symmetric, and Hermitian dataflow strategy

## Question

For each task-book benchmark case, what end-to-end NPU time budget and internal stage budget (layout/reconstruction, real GEMM work, alpha/beta postprocess, triangular writeback, launch overhead) must the chosen architecture meet to satisfy `NPU <= A100 / 0.8`, and which cases are likely to be performance-critical first?

## Required output

A benchmark matrix containing all official A100 reference cases, calculated NPU limits, estimated stage ceilings, and profiling metrics to capture with `msprof`.
