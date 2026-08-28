# Test and proof discipline

## Seams

A seam is the stable public boundary through which behavior is observed. Test the highest existing seam that proves the requirement without coupling to internals.

Choose the seam autonomously when repository precedent and the public interface make it unambiguous. Open a gate only when the work creates/moves a public seam or materially trades proof strength against cost/risk.

## Good tests

- verify observable behavior rather than private implementation;
- read like specifications;
- use independent expected values from a standard, task vector, known-good implementation, recorded fixture, or worked example;
- survive internal refactors;
- cover contract-relevant errors, boundaries, invariants, and state transitions;
- avoid tautological assertions and implementation-coupled mocks.

## Red → green

For a reproducible behavior change or defect:

1. write one failing behavioral test at the selected seam;
2. run it and record the red evidence;
3. implement only enough to make it pass;
4. run it and record green evidence;
5. repeat in narrow vertical slices;
6. refactor only while tests stay green.

Bulk “all tests first, all code later” is discouraged because it commits to imagined interfaces. Use tracer bullets that learn from each cycle.

## Check cadence

- run the narrowest relevant command frequently;
- run package/module checks before completing a ticket;
- run all project-mandated checks before completing the flow;
- do not weaken, skip, quarantine, or rewrite mandatory acceptance simply to obtain green without a recorded decision.

## Acceptance matrix

Every requirement maps to:

| Requirement | Environment | Seam/oracle | Command/benchmark | Pass criterion | Evidence |
|---|---|---|---|---|---|

No criterion is complete without executable or inspectable evidence.

## Performance proof

1. reproduce the official method and record variance;
2. separate setup, warm-up, measurement, validation, and teardown;
3. profile before optimizing;
4. identify the dominant stage and theoretical budget;
5. change one bottleneck at a time;
6. compare against the same baseline;
7. record resource use, target hardware/runtime, and profiler artifacts.

Simulation, CPU twins, mocks, or partial hardware may validate logic and direction, but cannot be reported as final target-environment performance unless the acceptance contract explicitly permits it.
