---
name: rtg-research
description: "Resolve a Run to Gate research ticket autonomously using repository evidence and authoritative primary sources, then return a durable finding with confidence, contradictions, and decision impact."
license: MIT
metadata:
  version: "1.0.0"
  family: "run-to-gate-companion"
---

# RTG Research

Resolve one precise research question. Do not broaden into implementation.

1. Restate the question and the decision/ticket it unblocks.
2. Search repository instructions, code, tests, issues, history, and primary external documentation before secondary commentary.
3. Separate facts, measured evidence, and inference. Mark unstable facts with source date/version.
4. Reconcile contradictions explicitly; identify which source is authoritative for the frozen contract.
5. Run reversible experiments when documentation is insufficient.
6. Write a durable artifact containing:
   - answer;
   - evidence and citations/pointers;
   - confidence and remaining uncertainty;
   - rejected interpretations;
   - effect on blockers, map/spec, and next frontier.
7. Return the artifact pointer to the canonical Run to Gate state.

Done when the ticket has an evidence-backed answer or a precisely scoped missing-access action. Never ask the human for a fact tools can establish.
