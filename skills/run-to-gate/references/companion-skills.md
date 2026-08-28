# Companion skills

`run-to-gate` is self-contained and must never stop merely because a companion is unavailable. This bundle also includes optional modular skills for clients that support multiple installed skills.

| Branch | Optional skill | Use |
|---|---|---|
| source-first investigation | `rtg-research` | gather facts and produce a durable evidence artifact |
| cheap decision evidence | `rtg-prototype` | build a reversible prototype, not production code |
| behavioral implementation | `rtg-tdd` | test at stable seams with red → green slices |
| hard failures/performance | `rtg-diagnose` | build a tight loop, test hypotheses, fix and regress |
| final diff review | `rtg-review` | independent Spec and Standards axes |
| conflict resolution | `rtg-merge-conflicts` | preserve source intents and finish merge/rebase |
| human-only operation | `rtg-manual-action` | produce a precise safe action wizard/checklist |

When an optional skill is installed and callable, use it for that branch and return its evidence to the canonical `.agent-flow` state. Otherwise follow the equivalent built-in reference in this skill.

The decision-mapping phase incorporates Wayfinder-style destination, fog, decision tickets, blockers, and frontier semantics directly. A separate Wayfinder installation is therefore not required for the end-to-end loop.
