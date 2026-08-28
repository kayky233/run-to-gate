#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "flowctl.py"


class FlowCtlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.state = self.root / ".agent-flow" / "demo" / "state.json"
        self.cli(
            "init",
            "--slug", "demo",
            "--title", "Demo",
            "--source", "test",
            "--outcome", "green PR",
            "--root", str(self.root / ".agent-flow"),
            "--repo-root", str(self.root),
            "--base-ref", "origin/main",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def cli(self, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(
            proc.returncode,
            expect,
            msg=f"command failed: {args}\nstdout={proc.stdout}\nstderr={proc.stderr}",
        )
        return proc

    def load(self) -> dict:
        return json.loads(self.state.read_text(encoding="utf-8"))

    def test_ticket_frontier_and_gate_routing(self) -> None:
        self.cli("set-phase", "--state", str(self.state), "--phase", "intake")
        self.cli("set-phase", "--state", str(self.state), "--phase", "decision_mapping")
        self.cli(
            "add-ticket", "--state", str(self.state), "--id", "T-001",
            "--title", "Independent research",
        )
        self.cli(
            "add-ticket", "--state", str(self.state), "--id", "T-002",
            "--title", "Architecture-dependent research",
        )
        self.cli(
            "open-gate", "--state", str(self.state), "--kind", "architecture",
            "--question", "Choose A or B", "--option", "A", "--option", "B",
            "--blocks", "T-002",
        )
        state = self.load()
        self.assertEqual(state["run_status"], "active")
        frontier = json.loads(self.cli("frontier", "--state", str(self.state)).stdout)
        self.assertEqual([item["id"] for item in frontier], ["T-001"])

        self.cli(
            "ticket-status", "--state", str(self.state), "--id", "T-001",
            "--status", "done", "--commit", "abc123",
        )
        # A later mutation refreshes the status according to the now-empty frontier.
        self.cli(
            "set-run-status", "--state", str(self.state),
            "--status", "waiting_for_human", "--force",
        )
        state = self.load()
        self.assertEqual(state["run_status"], "waiting_for_human")

        gate_id = state["gates"][0]["id"]
        self.assertTrue(gate_id.startswith("D-"))
        self.cli(
            "resolve-gate", "--state", str(self.state), "--id", gate_id,
            "--answer", "A", "--selected-option", "A",
        )
        state = self.load()
        self.assertEqual(state["run_status"], "active")
        frontier = json.loads(self.cli("frontier", "--state", str(self.state)).stdout)
        self.assertEqual([item["id"] for item in frontier], ["T-002"])
        self.cli("validate", "--state", str(self.state))

    def test_action_gate_prefix_and_status(self) -> None:
        self.cli(
            "open-gate", "--state", str(self.state), "--kind", "credentials",
            "--question", "Enter token in private dashboard", "--blocks", "bootstrap",
        )
        state = self.load()
        self.assertTrue(state["gates"][0]["id"].startswith("A-"))
        self.assertEqual(state["run_status"], "waiting_for_action")
        self.cli("validate", "--state", str(self.state))

    def test_revision_guard(self) -> None:
        revision = self.load()["revision"]
        self.cli(
            "set-phase", "--state", str(self.state), "--phase", "intake",
            "--expected-revision", str(revision),
        )
        self.cli(
            "set-phase", "--state", str(self.state), "--phase", "decision_mapping",
            "--expected-revision", str(revision), expect=2,
        )

    def test_cycle_is_rejected_by_validation(self) -> None:
        self.cli(
            "add-ticket", "--state", str(self.state), "--id", "T-001",
            "--title", "one", "--blocked-by", "T-002",
        )
        self.cli(
            "add-ticket", "--state", str(self.state), "--id", "T-002",
            "--title", "two", "--blocked-by", "T-001",
        )
        self.cli("validate", "--state", str(self.state), expect=1)

    def test_completed_requires_finished_tickets(self) -> None:
        self.cli("set-phase", "--state", str(self.state), "--phase", "intake")
        self.cli("set-phase", "--state", str(self.state), "--phase", "specification")
        self.cli("set-phase", "--state", str(self.state), "--phase", "ticketing")
        self.cli(
            "add-ticket", "--state", str(self.state), "--id", "T-001",
            "--title", "unfinished",
        )
        self.cli("set-phase", "--state", str(self.state), "--phase", "execution")
        self.cli("set-phase", "--state", str(self.state), "--phase", "verification")
        self.cli("set-phase", "--state", str(self.state), "--phase", "review")
        self.cli("set-phase", "--state", str(self.state), "--phase", "pull_request")
        self.cli("set-phase", "--state", str(self.state), "--phase", "completed")
        self.cli("validate", "--state", str(self.state), expect=1)


if __name__ == "__main__":
    unittest.main()
