# Diagnosis loop

The core of diagnosis is a **tight red-capable feedback loop**: one fast deterministic command that catches the user's exact symptom and goes green after the fix.

## 1. Build the loop before theorizing

Prefer, in order:

1. failing test at the correct seam;
2. HTTP/CLI script with a fixture and assertion;
3. headless browser script;
4. replayed trace/event payload;
5. throwaway harness;
6. property/fuzz loop;
7. differential or bisection harness;
8. a structured human-in-the-loop script only as a last resort.

Tighten speed, determinism, and signal specificity. For flaky bugs, raise reproduction probability rather than waiting for a clean deterministic single run.

If no valid loop can be built, record attempts and request the smallest missing artifact or access. Do not invent a root cause.

## 2. Reproduce and minimize

Confirm the loop catches the exact reported symptom. Remove inputs, callers, config, data, and steps one at a time. Keep only load-bearing elements.

## 3. Rank falsifiable hypotheses

Generate 3–5 hypotheses. Each must predict an observable result:

> If X is the cause, changing Y will remove or amplify the failure.

Use domain knowledge to rerank; proceed autonomously when the human is absent.

## 4. Instrument one prediction at a time

Prefer debugger/REPL, then targeted logs/metrics. Tag temporary instrumentation for guaranteed cleanup. For performance, measure/profiling replaces broad logging.

## 5. Regression test and fix

At a correct seam:

1. turn the minimized repro into a failing test;
2. observe red;
3. apply the smallest fix;
4. observe green;
5. rerun the original unminimized loop;
6. run affected and project-wide checks.

If no correct seam exists, record that architectural limitation rather than adding a false-confidence test.

## 6. Cleanup

- original symptom no longer reproduces;
- regression test passes or seam absence is documented;
- temporary logs and harnesses removed/quarantined;
- root cause and evidence recorded in commit/PR context;
- no acceptance criterion was silently weakened.
