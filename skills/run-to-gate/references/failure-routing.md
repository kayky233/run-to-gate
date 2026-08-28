# Failure routing

A retry is useful only when the next attempt changes information or method. Repeating the same failed action is not progress.

## Build, typecheck, lint, or test failure

1. capture the narrowest failing command and exact symptom;
2. classify current diff, frozen-baseline drift, environment/setup, dependency/API drift, or flaky infrastructure;
3. route code defects into the diagnosis loop;
4. verify official setup and pin versions for environment/baseline drift;
5. open a gate only if the repair changes a settled contract or policy.

## Hard bug

Build a tight red-capable loop, minimize, rank hypotheses, instrument, add the regression test at the correct seam, fix, clean up, and rerun the original scenario. If no loop is possible, request the smallest missing artifact/access and stop guessing.

## Performance miss

1. reproduce the official benchmark and variance;
2. profile before optimizing;
3. identify the dominant stage and budget;
4. rank interventions by expected gain, risk, and reversibility;
5. change one bottleneck at a time;
6. after the configured budget, open a gate only if meeting the target requires changing architecture, numerical behavior, scope, target, or acceptance.

## Flaky check

Increase reproduction rate; pin time, randomness, resources, and external services. A mandatory flaky check remains unresolved unless project policy explicitly says otherwise.

## CI-only failure

Fetch steps/logs, reproduce locally or in the closest container, and repair. Escalate with the exact environmental delta or missing permission, never a generic “CI failed”.

## Dependency/API drift

Prefer adapting to the frozen baseline. Updating the baseline is a human decision because it can change API, tests, performance, and delivery evidence. Security-critical upgrades still require reproducible evidence and repository-policy compliance.

## Tool or access failure

Try an equivalent permitted route once. Then:

1. record the missing capability and why it is required;
2. continue every independent task possible at the current capability tier;
3. produce an exact action request with commands/URLs, expected output, and resume condition;
4. never claim a push, CI run, target-device benchmark, dashboard change, or PR occurred when access was absent.

## External service unavailable

Record timestamp, endpoint/service, error, and retry policy. Continue local work. Use `waiting_for_external_check` only when all remaining work depends on the service.

## Loop budgets

Defaults from the policy template:

- implementation attempts before formal diagnosis: 2;
- review-fix cycles: 2;
- CI-repair cycles: 3;
- performance interventions: 6.

Reaching a budget changes method or opens a well-evidenced gate. It never justifies abandoning a requirement or silently lowering quality.
