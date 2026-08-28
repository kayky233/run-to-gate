# Review and integration

## Two independent review axes

### Spec

Find:

- missing or partial requirements;
- behavior implemented incorrectly;
- unrequested behavior or scope creep;
- acceptance criteria without proof;
- compatibility/migration mistakes.

Cite the originating requirement/decision for each finding.

### Standards

Find:

- violations of repository-local rules;
- security and reliability defects;
- maintainability issues not enforced by tooling;
- relevant smells such as mysterious names, duplication, feature envy, data clumps, primitive obsession, repeated switches, shotgun surgery, divergent change, speculative generality, message chains, middle men, or misused inheritance.

Repository-documented standards override generic heuristics. Label smell findings as judgment calls, not automatic violations.

## Fix policy

Fix deterministic findings autonomously. Rerun the narrow and full checks. Escalate only when a finding requires product, public contract, architecture, scope, acceptance, security, or irreversible judgment.

Keep Spec and Standards reports separate so passing one axis cannot hide failure in the other.

## Merge/rebase conflicts

1. inspect current merge/rebase state and conflicting files;
2. read the primary sources for each side: commits, issues, decisions, specs;
3. preserve both intents where compatible;
4. where incompatible, choose the intent matching the recorded destination and contract;
5. never invent unrelated new behavior during conflict resolution;
6. run affected checks and the required full suite;
7. finish the merge/rebase rather than aborting because it is difficult;
8. open a gate only when two settled human decisions genuinely conflict.

## Pull request

The PR/handoff includes:

- outcome and user-visible behavior;
- base/head and important commits;
- decision and ticket traceability;
- verification matrix and exact environments;
- performance evidence when applicable;
- review results and fixed findings;
- known limitations/residual risks;
- manual validation or reserved merge/release steps.

## CI

Monitor checks when tools permit. For failures:

- fetch exact job/step/log evidence;
- reproduce in the closest available environment;
- classify code, baseline, dependency, environment, permission, or infrastructure cause;
- fix and rerun within policy budgets;
- never rerun flaky checks until lucky.
