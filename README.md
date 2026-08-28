# Run to Gate Skill Bundle

**Run to Gate：人类负责关键决策，AI 负责持续推进。**

This distribution contains one self-contained orchestration skill and seven optional modular companion skills.

## Recommended install

For a client that accepts one skill ZIP, upload:

```text
install/run-to-gate.zip
```

The main skill is self-contained. It includes decision mapping, specification, tracer-bullet ticketing, implementation, test/proof, diagnosis, review, failure routing, durable state, PR, and CI behavior. It does not require the optional companions.

## Optional companion skills

Clients that support multiple skill folders may install any or all of:

| Skill | Purpose |
|---|---|
| `rtg-research` | source-first autonomous research |
| `rtg-prototype` | cheap reversible decision evidence |
| `rtg-tdd` | behavioral red → green implementation |
| `rtg-diagnose` | tight-loop debugging and performance diagnosis |
| `rtg-review` | independent Spec and Standards review |
| `rtg-merge-conflicts` | source-intent-preserving conflict resolution |
| `rtg-manual-action` | safe human-only action wizard/checklist |

Individual archives are in `install/optional/`; editable source folders are in `skills/`.

## Why the main skill remains self-contained

A run must not stall because another skill is missing, cannot be invoked by the current client, or is configured as a human-only entry point. The main skill therefore owns the complete state machine. Optional companions only deepen a branch and return evidence to the same `.agent-flow/<slug>/` state.

## Decision mapping

The main skill directly incorporates Wayfinder-style destination, fog, decision tickets, blockers, frontier, and autonomous-versus-human work semantics. A separate Wayfinder installation is not required for the end-to-end path.

## Distribution layout

```text
run-to-gate-bundle/
├── README.md
├── BUNDLE-MANIFEST.json
├── install/
│   ├── run-to-gate.zip
│   └── optional/*.zip
├── skills/
│   ├── run-to-gate/
│   └── rtg-*/
└── licenses/
```

## Suggested invocation

```text
@Run to Gate

Continue this engineering task from durable state.
Ask me only for material product, public contract, architecture, scope,
acceptance, security, irreversible, or merge/release decisions.
Continue all reversible research, planning, ticketing, implementation,
testing, diagnosis, review, commits, PR, and CI work autonomously.
Stop only when every remaining path is blocked by a real gate.
```
