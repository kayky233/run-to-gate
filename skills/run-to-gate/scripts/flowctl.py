#!/usr/bin/env python3
"""Durable state helper for Run to Gate.

Uses only the Python standard library. All mutations are atomic and append an
immutable event entry. This is a state helper, not an autonomous scheduler.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

PHASES = [
    "bootstrap", "intake", "decision_mapping", "specification", "ticketing",
    "execution", "verification", "review", "pull_request", "completed",
    "blocked", "cancelled",
]
RUN_STATUSES = [
    "active", "waiting_for_human", "waiting_for_action", "waiting_for_access",
    "waiting_for_external_check", "waiting_for_merge", "completed", "cancelled",
]
TICKET_STATUSES = ["blocked", "ready", "in_progress", "done", "failed", "cancelled"]
GATE_KINDS = [
    "product", "contract", "public_contract", "architecture", "scope",
    "acceptance", "security", "policy_exception", "irreversible",
    "merge_release", "manual_action", "access", "credentials",
    "external_dashboard", "device_validation", "platform_confirmation",
]
ALLOWED_TRANSITIONS = {
    "bootstrap": {"intake", "blocked", "cancelled"},
    "intake": {"decision_mapping", "specification", "blocked", "cancelled"},
    "decision_mapping": {"specification", "blocked", "cancelled"},
    "specification": {"ticketing", "decision_mapping", "blocked", "cancelled"},
    "ticketing": {"execution", "specification", "blocked", "cancelled"},
    "execution": {"verification", "decision_mapping", "blocked", "cancelled"},
    "verification": {"review", "execution", "decision_mapping", "blocked", "cancelled"},
    "review": {"pull_request", "execution", "decision_mapping", "blocked", "cancelled"},
    "pull_request": {"completed", "execution", "verification", "blocked", "cancelled"},
    "blocked": set(PHASES) - {"blocked", "completed"},
    "completed": set(),
    "cancelled": set(),
}
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def fail(message: str, code: int = 2) -> "NoReturn":
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def load(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            state = json.load(f)
    except FileNotFoundError:
        fail(f"state file not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(state, dict):
        fail("state root must be an object")
    # Read legacy state without losing compatibility; the next mutation writes the new status.
    if state.get("run_status") == "waiting_for_access":
        state["run_status"] = "waiting_for_action"
    return state


def atomic_save(path: Path, state: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = now()
    state["revision"] = int(state.get("revision", 0)) + 1
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def check_revision(state: Dict[str, Any], expected: int | None) -> None:
    if expected is not None and int(state.get("revision", 0)) != expected:
        fail(f"revision mismatch: expected {expected}, found {state.get('revision', 0)}")


def event(state: Dict[str, Any], action: str, details: Dict[str, Any] | None = None) -> None:
    state.setdefault("events", []).append({
        "at": now(), "action": action, "details": details or {}
    })


def parse_csv(value: str | None) -> List[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def next_id(items: Iterable[Dict[str, Any]], prefix: str) -> str:
    max_num = 0
    for item in items:
        ident = str(item.get("id", ""))
        if ident.startswith(prefix + "-"):
            try:
                max_num = max(max_num, int(ident.split("-", 1)[1]))
            except ValueError:
                pass
    return f"{prefix}-{max_num + 1:03d}"


def by_id(items: List[Dict[str, Any]], ident: str, kind: str) -> Dict[str, Any]:
    for item in items:
        if item.get("id") == ident:
            return item
    fail(f"unknown {kind} id: {ident}")


def done_ticket_ids(state: Dict[str, Any]) -> set[str]:
    return {t["id"] for t in state.get("tickets", []) if t.get("status") in {"done", "cancelled"}}


ACTION_GATE_KINDS = {
    "manual_action", "access", "credentials", "external_dashboard",
    "device_validation", "platform_confirmation",
}


def open_gates(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [g for g in state.get("gates", []) if g.get("status") == "open"]


def blocked_targets(state: Dict[str, Any]) -> set[str]:
    targets: set[str] = set()
    for gate in open_gates(state):
        targets.update(str(item) for item in gate.get("blocks", []))
    return targets


def refresh_run_status(state: Dict[str, Any]) -> None:
    gates = open_gates(state)
    if gates:
        # A gate pauses the run only when it blocks every remaining frontier item.
        # Independent work must continue.
        if frontier(state):
            state["run_status"] = "active"
        elif any(g.get("kind") not in ACTION_GATE_KINDS for g in gates):
            state["run_status"] = "waiting_for_human"
        else:
            state["run_status"] = "waiting_for_action"
        return
    if state.get("phase") == "completed":
        state["run_status"] = "completed"
    elif state.get("phase") == "cancelled":
        state["run_status"] = "cancelled"
    elif state.get("run_status") in {
        "waiting_for_human", "waiting_for_action", "waiting_for_access"
    }:
        state["run_status"] = "active"


def recompute_ticket_readiness(state: Dict[str, Any]) -> None:
    done = done_ticket_ids(state)
    gate_blocks = blocked_targets(state)
    for ticket in state.get("tickets", []):
        if ticket.get("status") in {"done", "cancelled", "in_progress", "failed"}:
            continue
        if ticket.get("id") in gate_blocks:
            ticket["status"] = "blocked"
        else:
            ticket["status"] = (
                "ready" if set(ticket.get("blocked_by", [])) <= done else "blocked"
            )


def frontier(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    recompute_ticket_readiness(state)
    if state.get("phase") in blocked_targets(state):
        return []
    return [
        t for t in state.get("tickets", [])
        if t.get("status") == "ready" and not t.get("owner")
    ]


def state_path(args: argparse.Namespace) -> Path:
    return Path(args.state).resolve()


def mutate(args: argparse.Namespace) -> tuple[Path, Dict[str, Any]]:
    path = state_path(args)
    state = load(path)
    check_revision(state, getattr(args, "expected_revision", None))
    return path, state


def command_init(args: argparse.Namespace) -> None:
    if not SLUG_RE.fullmatch(args.slug):
        fail("slug must match [a-z0-9][a-z0-9-]{0,62}")
    root = Path(args.root).resolve() / args.slug
    path = root / "state.json"
    if path.exists() and not args.force:
        fail(f"state already exists: {path}; pass --force to replace")
    for directory in ["decisions", "tickets", "evidence"]:
        (root / directory).mkdir(parents=True, exist_ok=True)
    created = now()
    state = {
        "schema_version": 1,
        "flow_id": args.slug,
        "title": args.title,
        "source": args.source,
        "outcome": args.outcome or "",
        "phase": "bootstrap",
        "run_status": "active",
        "revision": -1,
        "created_at": created,
        "updated_at": created,
        "repository": {
            "root": str(Path(args.repo_root).resolve()),
            "base_ref": args.base_ref,
            "feature_branch": args.feature_branch or "",
            "worktree": "",
            "head_commit": "",
        },
        "capabilities": {"tier": "unknown", "tools": [], "limitations": []},
        "policy": {
            "mode": "run_to_gate",
            "stop_before": ["merge", "release", "production_deploy"],
        },
        "gates": [],
        "tickets": [],
        "evidence": [],
        "events": [],
    }
    event(state, "flow_initialized", {"source": args.source})
    atomic_save(path, state)
    for name, content in {
        "map.md": f"# {args.title} — decision map\n\n## Destination\n\n{args.outcome or '<record outcome>'}\n\n## Decisions so far\n\n## Not yet specified\n\n## Out of scope\n",
        "spec.md": f"# {args.title} — specification\n\nStatus: not started\n",
        "completion.md": f"# {args.title} — completion report\n\nStatus: not completed\n",
    }.items():
        target = root / name
        if not target.exists() or args.force:
            target.write_text(content, encoding="utf-8")
    print(path)


def command_status(args: argparse.Namespace) -> None:
    state = load(state_path(args))
    recompute_ticket_readiness(state)
    active_gates = open_gates(state)
    counts: Dict[str, int] = {}
    for t in state.get("tickets", []):
        counts[t.get("status", "unknown")] = counts.get(t.get("status", "unknown"), 0) + 1
    result = {
        "flow_id": state.get("flow_id"),
        "title": state.get("title"),
        "outcome": state.get("outcome"),
        "phase": state.get("phase"),
        "run_status": state.get("run_status"),
        "revision": state.get("revision"),
        "open_gates": [g.get("id") for g in active_gates],
        "ticket_counts": counts,
        "frontier": [t.get("id") for t in frontier(state)],
        "updated_at": state.get("updated_at"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def command_set_phase(args: argparse.Namespace) -> None:
    path, state = mutate(args)
    old = state.get("phase")
    if args.phase not in PHASES:
        fail(f"unknown phase: {args.phase}")
    active_gates = open_gates(state)
    if active_gates and not args.force:
        fail("cannot transition while gates are open; resolve them or pass --force")
    if not args.force and args.phase not in ALLOWED_TRANSITIONS.get(old, set()):
        fail(f"transition not allowed: {old} -> {args.phase}")
    state["phase"] = args.phase
    if args.phase == "completed":
        state["run_status"] = "completed"
    elif args.phase == "cancelled":
        state["run_status"] = "cancelled"
    elif state.get("run_status") in {"completed", "cancelled", "waiting_for_merge"}:
        state["run_status"] = "active"
    refresh_run_status(state)
    event(state, "phase_changed", {"from": old, "to": args.phase})
    atomic_save(path, state)
    print(f"{old} -> {args.phase}")


def command_open_gate(args: argparse.Namespace) -> None:
    path, state = mutate(args)
    if args.kind not in GATE_KINDS:
        fail(f"unknown gate kind: {args.kind}")
    ident = args.id or next_id(state.get("gates", []), "A" if args.kind in ACTION_GATE_KINDS else "D")
    if any(g.get("id") == ident for g in state.get("gates", [])):
        fail(f"gate id already exists: {ident}")
    gate = {
        "id": ident,
        "kind": args.kind,
        "title": args.title or args.question[:80],
        "question": args.question,
        "recommendation": args.recommendation or "",
        "options": args.option or [],
        "blocks": parse_csv(args.blocks),
        "status": "open",
        "opened_at": now(),
        "resolved_at": None,
        "answer": None,
        "selected_option": None,
        "resume_condition": args.resume_condition or "human response recorded",
    }
    state.setdefault("gates", []).append(gate)
    refresh_run_status(state)
    event(state, "gate_opened", {"id": ident, "kind": args.kind})
    atomic_save(path, state)
    print(ident)


def command_resolve_gate(args: argparse.Namespace) -> None:
    path, state = mutate(args)
    gate = by_id(state.get("gates", []), args.id, "gate")
    if gate.get("status") != "open":
        fail(f"gate is not open: {args.id}")
    gate.update({
        "status": "resolved",
        "resolved_at": now(),
        "answer": args.answer,
        "selected_option": args.selected_option,
        "resolved_by": args.by,
    })
    refresh_run_status(state)
    event(state, "gate_resolved", {"id": args.id, "selected_option": args.selected_option})
    atomic_save(path, state)
    print(args.id)


def command_add_ticket(args: argparse.Namespace) -> None:
    path, state = mutate(args)
    ident = args.id or next_id(state.get("tickets", []), "T")
    if any(t.get("id") == ident for t in state.get("tickets", [])):
        fail(f"ticket id already exists: {ident}")
    blockers = parse_csv(args.blocked_by)
    ticket = {
        "id": ident,
        "title": args.title,
        "type": args.type,
        "mode": args.mode,
        "blocked_by": blockers,
        "status": "blocked" if blockers else "ready",
        "owner": None,
        "acceptance": args.acceptance or [],
        "commits": [],
        "evidence_ids": [],
        "created_at": now(),
        "updated_at": now(),
    }
    state.setdefault("tickets", []).append(ticket)
    recompute_ticket_readiness(state)
    event(state, "ticket_added", {"id": ident, "blocked_by": blockers})
    atomic_save(path, state)
    print(ident)


def command_ticket_status(args: argparse.Namespace) -> None:
    path, state = mutate(args)
    if args.status not in TICKET_STATUSES:
        fail(f"unknown ticket status: {args.status}")
    ticket = by_id(state.get("tickets", []), args.id, "ticket")
    old = ticket.get("status")
    ticket["status"] = args.status
    if args.owner is not None:
        ticket["owner"] = args.owner or None
    if args.commit and args.commit not in ticket.setdefault("commits", []):
        ticket["commits"].append(args.commit)
    if args.status in {"done", "cancelled"}:
        ticket["owner"] = None
    ticket["updated_at"] = now()
    recompute_ticket_readiness(state)
    event(state, "ticket_status_changed", {"id": args.id, "from": old, "to": args.status})
    atomic_save(path, state)
    print(f"{args.id}: {old} -> {args.status}")


def command_frontier(args: argparse.Namespace) -> None:
    state = load(state_path(args))
    items = frontier(state)
    print(json.dumps(items, ensure_ascii=False, indent=2))


def command_add_evidence(args: argparse.Namespace) -> None:
    path, state = mutate(args)
    ident = args.id or next_id(state.get("evidence", []), "E")
    if any(e.get("id") == ident for e in state.get("evidence", [])):
        fail(f"evidence id already exists: {ident}")
    evidence = {
        "id": ident,
        "kind": args.kind,
        "summary": args.summary,
        "command": args.command or "",
        "working_directory": args.working_directory or "",
        "exit_code": args.exit_code,
        "artifact": args.artifact or "",
        "ticket_id": args.ticket_id,
        "acceptance_id": args.acceptance_id,
        "commit": args.commit or "",
        "recorded_at": now(),
    }
    state.setdefault("evidence", []).append(evidence)
    if args.ticket_id:
        ticket = by_id(state.get("tickets", []), args.ticket_id, "ticket")
        if ident not in ticket.setdefault("evidence_ids", []):
            ticket["evidence_ids"].append(ident)
    event(state, "evidence_added", {"id": ident, "kind": args.kind})
    atomic_save(path, state)
    print(ident)


def detect_cycle(tickets: List[Dict[str, Any]]) -> List[str] | None:
    graph = {t["id"]: list(t.get("blocked_by", [])) for t in tickets}
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: List[str] = []

    def visit(node: str) -> List[str] | None:
        if node in visiting:
            i = stack.index(node)
            return stack[i:] + [node]
        if node in visited:
            return None
        visiting.add(node)
        stack.append(node)
        for dep in graph.get(node, []):
            cycle = visit(dep)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def validate_state(state: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if state.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if state.get("phase") not in PHASES:
        errors.append(f"invalid phase: {state.get('phase')}")
    if state.get("run_status") not in RUN_STATUSES:
        errors.append(f"invalid run_status: {state.get('run_status')}")
    tickets = state.get("tickets", [])
    ticket_ids = [t.get("id") for t in tickets]
    if len(ticket_ids) != len(set(ticket_ids)):
        errors.append("duplicate ticket id")
    known = set(ticket_ids)
    for ticket in tickets:
        unknown = set(ticket.get("blocked_by", [])) - known
        if unknown:
            errors.append(f"{ticket.get('id')} has unknown blockers: {sorted(unknown)}")
        if ticket.get("status") not in TICKET_STATUSES:
            errors.append(f"{ticket.get('id')} has invalid status: {ticket.get('status')}")
    cycle = detect_cycle(tickets)
    if cycle:
        errors.append("ticket dependency cycle: " + " -> ".join(cycle))
    gate_ids = [g.get("id") for g in state.get("gates", [])]
    if len(gate_ids) != len(set(gate_ids)):
        errors.append("duplicate gate id")
    for gate in state.get("gates", []):
        if gate.get("kind") not in GATE_KINDS:
            errors.append(f"{gate.get('id')} has invalid gate kind: {gate.get('kind')}")
        if gate.get("status") not in {"open", "resolved", "cancelled"}:
            errors.append(f"{gate.get('id')} has invalid gate status: {gate.get('status')}")
        for target in gate.get("blocks", []):
            if target not in known and target not in PHASES:
                errors.append(f"{gate.get('id')} blocks unknown target: {target}")
    active_gates = open_gates(state)
    available_frontier = frontier(state)
    if active_gates and not available_frontier and state.get("run_status") not in {
        "waiting_for_human", "waiting_for_action", "waiting_for_access"
    }:
        errors.append("fully blocking open gates require a waiting run status")
    if active_gates and available_frontier and state.get("run_status") != "active":
        errors.append("independent frontier work requires active run status despite open gates")
    if state.get("phase") == "completed":
        unfinished = [t.get("id") for t in tickets if t.get("status") not in {"done", "cancelled"}]
        if unfinished:
            errors.append(f"completed flow has unfinished tickets: {unfinished}")
        if active_gates:
            errors.append("completed flow has open gates")
    return errors


def command_set_run_status(args: argparse.Namespace) -> None:
    path, state = mutate(args)
    old = state.get("run_status")
    if args.status not in RUN_STATUSES:
        fail(f"unknown run status: {args.status}")
    gates = open_gates(state)
    available_frontier = frontier(state)
    if gates and not available_frontier and args.status not in {
        "waiting_for_human", "waiting_for_action", "waiting_for_access"
    } and not args.force:
        fail("fully blocking open gates require a waiting run status; pass --force to override")
    if gates and available_frontier and args.status != "active" and not args.force:
        fail("independent frontier work remains; run status must stay active")
    state["run_status"] = args.status
    event(state, "run_status_changed", {"from": old, "to": args.status})
    atomic_save(path, state)
    print(f"{old} -> {args.status}")


def command_validate(args: argparse.Namespace) -> None:
    state = load(state_path(args))
    errors = validate_state(state)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    print("OK")


def add_state_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--state", required=True, help="Path to state.json")


def add_mutation_args(parser: argparse.ArgumentParser) -> None:
    add_state_arg(parser)
    parser.add_argument("--expected-revision", type=int)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Initialize a durable flow")
    p.add_argument("--slug", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--outcome")
    p.add_argument("--root", default=".agent-flow")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--base-ref", default="")
    p.add_argument("--feature-branch")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=command_init)

    p = sub.add_parser("status", help="Show compact flow status")
    add_state_arg(p)
    p.set_defaults(func=command_status)

    p = sub.add_parser("set-phase", help="Transition workflow phase")
    add_mutation_args(p)
    p.add_argument("--phase", required=True, choices=PHASES)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=command_set_phase)

    p = sub.add_parser("open-gate", help="Open a human decision or human-only action gate")
    add_mutation_args(p)
    p.add_argument("--id")
    p.add_argument("--kind", required=True, choices=GATE_KINDS)
    p.add_argument("--title")
    p.add_argument("--question", required=True)
    p.add_argument("--recommendation")
    p.add_argument("--option", action="append")
    p.add_argument("--blocks", help="Comma-separated ticket IDs or phase names")
    p.add_argument("--resume-condition")
    p.set_defaults(func=command_open_gate)

    p = sub.add_parser("resolve-gate", help="Resolve an open gate")
    add_mutation_args(p)
    p.add_argument("--id", required=True)
    p.add_argument("--answer", required=True)
    p.add_argument("--selected-option")
    p.add_argument("--by", default="human")
    p.set_defaults(func=command_resolve_gate)

    p = sub.add_parser("add-ticket", help="Add a tracer-bullet or decision ticket")
    add_mutation_args(p)
    p.add_argument("--id")
    p.add_argument("--title", required=True)
    p.add_argument("--type", default="implementation")
    p.add_argument("--mode", default="AFK", choices=["AFK", "HITL"])
    p.add_argument("--blocked-by", help="Comma-separated ticket IDs")
    p.add_argument("--acceptance", action="append")
    p.set_defaults(func=command_add_ticket)

    p = sub.add_parser("ticket-status", help="Update ticket status/owner/commit")
    add_mutation_args(p)
    p.add_argument("--id", required=True)
    p.add_argument("--status", required=True, choices=TICKET_STATUSES)
    p.add_argument("--owner")
    p.add_argument("--commit")
    p.set_defaults(func=command_ticket_status)

    p = sub.add_parser("frontier", help="List unblocked unclaimed tickets")
    add_state_arg(p)
    p.set_defaults(func=command_frontier)

    p = sub.add_parser("add-evidence", help="Append evidence to the ledger")
    add_mutation_args(p)
    p.add_argument("--id")
    p.add_argument("--kind", required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--command")
    p.add_argument("--working-directory")
    p.add_argument("--exit-code", type=int)
    p.add_argument("--artifact")
    p.add_argument("--ticket-id")
    p.add_argument("--acceptance-id")
    p.add_argument("--commit")
    p.set_defaults(func=command_add_evidence)

    p = sub.add_parser("set-run-status", help="Set run status explicitly")
    add_mutation_args(p)
    p.add_argument("--status", required=True, choices=RUN_STATUSES)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=command_set_run_status)

    p = sub.add_parser("validate", help="Validate state invariants")
    add_state_arg(p)
    p.set_defaults(func=command_validate)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
