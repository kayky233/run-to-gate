#!/usr/bin/env python3
"""Validate a Run to Gate skill folder and optionally regenerate MANIFEST.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FORBIDDEN = tuple(
    "".join(parts)
    for parts in (
        ("ka", "y dev"),
        ("ka", "y server"),
        ("autonomous", "-engineering-flow"),
        ("autonomous", " engineering flow"),
    )
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "MANIFEST.json":
            continue
        try:
            yield path, path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.exists():
        errors.append("SKILL.md is missing")
        return errors
    content = skill.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        errors.append("SKILL.md frontmatter is missing")
    if "\nname: run-to-gate\n" not in content:
        errors.append("SKILL.md name must be run-to-gate")
    if "\ndescription:" not in content:
        errors.append("SKILL.md description is missing")

    for path, text in text_files(root):
        lowered = text.lower()
        for forbidden in FORBIDDEN:
            if forbidden in lowered:
                errors.append(f"forbidden text {forbidden!r} in {path.relative_to(root)}")
        if path.suffix.lower() == ".md":
            for target in LINK_RE.findall(text):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                target_path = (path.parent / target.split("#", 1)[0]).resolve()
                if target.split("#", 1)[0] and not target_path.exists():
                    errors.append(
                        f"broken relative link in {path.relative_to(root)}: {target}"
                    )
    return errors


def manifest(root: Path) -> dict:
    files = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.json" and "__pycache__" not in path.parts:
            files.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    return {"schema_version": 1, "skill": "run-to-gate", "files": files}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    data = manifest(root)
    if args.write_manifest:
        (root / "MANIFEST.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(f"OK: {len(data['files'])} files")


if __name__ == "__main__":
    main()
