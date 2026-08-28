# Freeze the delivery baseline and repository contract

Label: `wayfinder:grilling`
Mode: HITL
Status: open / unclaimed

## Question

Which exact `ops-blas` source baseline must this effort target for final delivery — the CANN version/tag bound to the community task environment, a specific fork/branch already owned by the developer, or current `master` — and therefore which directory layout, public API conventions, build workflow, and agent/repo rules are normative for the implementation?

## Why this blocks the map

The upstream repository has changed its operator directory layout, complex BLAS interface conventions, handle/scalar signatures, test precision mode, and agent workflow recently. Implementing before freezing the baseline risks creating code and tests against a moving or wrong contract.

## Resolution evidence required

- exact repository URL/fork;
- branch or tag/commit;
- target CANN package version;
- confirmed SoC (`ascend910b3` / arch22);
- authoritative repo-local workflow/rules to follow on that baseline.
