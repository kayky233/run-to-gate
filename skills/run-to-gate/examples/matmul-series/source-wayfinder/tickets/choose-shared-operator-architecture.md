# Choose the shared operator architecture boundary

Label: `wayfinder:grilling`
Mode: HITL
Status: blocked
Blocked by: Lock the five public API and edge-case semantics; Establish the Atlas A2 complex64 compute capability envelope

## Question

Given the settled semantics and A2 compute envelope, should the implementation use one shared internal complex-matrix engine, two shared families (HEMM/SYMM and HERK/HER2K/SYRK), or predominantly operator-specific kernels — and what is the acceptable tradeoff between code reuse, reviewability, workspace/memory traffic, and achieving the performance target?

This is a design-policy decision, not a request to implement the engine.
