#!/usr/bin/env python3
"""Check the structure of an Org execution plan."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

TODO_STATES = {"TODO", "NEXT", "BLOCKED", "REVIEW", "DONE", "CANCELLED"}
HEADING_RE = re.compile(
    r"^(?P<stars>\*+)\s+"
    r"(?:(?P<state>TODO|NEXT|BLOCKED|REVIEW|DONE|CANCELLED)\s+)?"
    r"(?P<title>.*?)(?:\s+:[A-Za-z0-9_@#%:]+:)?\s*$"
)
PROPERTY_RE = re.compile(r"^:(?P<key>[A-Z_]+):\s*(?P<value>.*?)\s*$")


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    state: str | None
    title: str
    body: tuple[str, ...]
    properties: dict[str, str]

    @property
    def task_id(self) -> str | None:
        return self.properties.get("ID")

    @property
    def dependencies(self) -> tuple[str, ...]:
        value = self.properties.get("DEPENDS", "")
        return tuple(value.split()) if value else ()

    @property
    def is_phase(self) -> bool:
        return self.level == 1 and self.title.lower().startswith("phase ")

    @property
    def is_gate(self) -> bool:
        title = self.title.lower()
        return title.startswith("phase ") and title.endswith(" check")

    @property
    def is_final_audit(self) -> bool:
        return self.title.lower() == "final check"


def parse_headings(lines: list[str]) -> list[Heading]:
    raw: list[tuple[int, int, str | None, str]] = []
    in_block = False
    for index, line in enumerate(lines):
        stripped = line.strip().lower()
        if in_block:
            if stripped.startswith("#+end_"):
                in_block = False
            continue
        if stripped.startswith("#+begin_"):
            in_block = True
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        raw.append(
            (
                index,
                len(match.group("stars")),
                match.group("state"),
                match.group("title").strip(),
            )
        )

    headings: list[Heading] = []
    for position, (index, level, state, title) in enumerate(raw):
        end = raw[position + 1][0] if position + 1 < len(raw) else len(lines)
        body = tuple(lines[index + 1 : end])
        properties: dict[str, str] = {}
        in_drawer = False
        for body_line in body:
            body_line = body_line.strip()
            if body_line == ":PROPERTIES:":
                in_drawer = True
                continue
            if body_line == ":END:" and in_drawer:
                break
            if not in_drawer:
                continue
            match = PROPERTY_RE.match(body_line)
            if match:
                properties[match.group("key")] = match.group("value")
        headings.append(
            Heading(
                line=index + 1,
                level=level,
                state=state,
                title=title,
                body=body,
                properties=properties,
            )
        )
    return headings


def find_cycle(graph: dict[str, tuple[str, ...]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visiting:
            start = stack.index(node)
            return [*stack[start:], node]
        if node in visited:
            return None
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, ()):
            cycle = visit(dependency)
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


def has_field(heading: Heading, field: str) -> bool:
    pattern = re.compile(rf"^[ \t]*{re.escape(field)}:\s*$", re.MULTILINE)
    return bool(pattern.search("\n".join(heading.body)))


def field_text(heading: Heading, field: str) -> str:
    start = re.compile(rf"^[ \t]*{re.escape(field)}:\s*$")
    next_field = re.compile(r"^[ \t]*[A-Z][A-Za-z ]+:\s*$")
    collecting = False
    collected: list[str] = []
    for line in heading.body:
        if not collecting:
            collecting = bool(start.match(line))
            continue
        if next_field.match(line):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def child_headings(headings: list[Heading], parent_index: int) -> list[Heading]:
    parent = headings[parent_index]
    children: list[Heading] = []
    for heading in headings[parent_index + 1 :]:
        if heading.level <= parent.level:
            break
        children.append(heading)
    return children


def validate(path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []

    if path.suffix.lower() != ".org":
        errors.append("plan must use the .org extension")

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [f"cannot read UTF-8 plan: {error}"], warnings, {}

    lines = text.splitlines()
    headings = parse_headings(lines)
    actionable = [heading for heading in headings if heading.state in TODO_STATES]
    ids = [heading.task_id for heading in actionable if heading.task_id]
    id_set = set(ids)

    if not re.search(r"^#\+TODO:.*TODO.*\|.*DONE", text, re.MULTILINE):
        errors.append("missing a #+TODO sequence with active and completed states")

    required_sections = (
        "How to use this plan",
        "Goal and rules",
        "What is true now",
        "Open questions",
        "Order of work",
    )
    titles = {heading.title.lower() for heading in headings}
    for section in required_sections:
        if section.lower() not in titles:
            errors.append(f"missing required section: {section}")

    if not any(heading.is_final_audit for heading in actionable):
        errors.append("missing a TODO Final check heading")

    trailing = [index + 1 for index, line in enumerate(lines) if line != line.rstrip()]
    if trailing:
        errors.append(
            "trailing whitespace on line(s): " + ", ".join(map(str, trailing[:20]))
        )

    missing_ids = [heading for heading in actionable if not heading.task_id]
    for heading in missing_ids:
        errors.append(
            f"line {heading.line}: task has no ID: {heading.title}"
        )

    duplicates = sorted({task_id for task_id in ids if ids.count(task_id) > 1})
    for task_id in duplicates:
        errors.append(f"duplicate ID: {task_id}")

    for heading in actionable:
        for dependency in heading.dependencies:
            if dependency not in id_set:
                errors.append(
                    f"line {heading.line}: {heading.task_id} depends on missing "
                    f"ID {dependency}"
                )
            if dependency == heading.task_id:
                errors.append(
                    f"line {heading.line}: {heading.task_id} depends on itself"
                )

    graph = {
        heading.task_id: heading.dependencies
        for heading in actionable
        if heading.task_id
    }
    cycle = find_cycle(graph)
    if cycle:
        errors.append("task links form a loop: " + " -> ".join(cycle))

    phases = [
        (index, heading)
        for index, heading in enumerate(headings)
        if heading.state in TODO_STATES and heading.is_phase
    ]
    for index, phase in phases:
        descendants = child_headings(headings, index)
        if not any(
            child.state in TODO_STATES and child.is_gate for child in descendants
        ):
            errors.append(
                f"line {phase.line}: phase has no TODO phase check: {phase.title}"
            )

    for heading in actionable:
        if heading.is_phase:
            continue
        required_fields = ["Result", "Steps", "Proof", "Done when"]
        if heading.is_gate:
            review_fields = ["Expected", "Feedback", "Replan"]
        elif heading.is_final_audit:
            review_fields = ["Feedback"]
        else:
            review_fields = []
        required_fields.extend(review_fields)
        missing_fields = [
            field
            for field in required_fields
            if not has_field(heading, field)
        ]
        if missing_fields:
            warnings.append(
                f"line {heading.line}: {heading.task_id or heading.title} is "
                "missing " + ", ".join(missing_fields)
            )
        for field in review_fields:
            if not has_field(heading, field):
                continue
            text = field_text(heading, field)
            if not text:
                message = (
                    f"line {heading.line}: "
                    f"{heading.task_id or heading.title} has empty {field}"
                )
                if heading.state == "DONE":
                    errors.append(message)
                else:
                    warnings.append(message)
            elif heading.state == "DONE" and "{{" in text:
                errors.append(
                    f"line {heading.line}: completed check still has "
                    f"placeholder {field}"
                )

    metrics = {
        "headings": len(headings),
        "tasks": len(actionable),
        "ids": len(ids),
        "links": sum(len(heading.dependencies) for heading in actionable),
        "phases": len(phases),
        "feedback": sum(
            1
            for heading in actionable
            if (heading.is_gate or heading.is_final_audit)
            and has_field(heading, "Feedback")
        ),
        "replans": sum(
            1
            for heading in actionable
            if heading.is_gate and has_field(heading, "Replan")
        ),
        "warnings": len(warnings),
        "errors": len(errors),
    }
    return errors, warnings, metrics


def run_emacs_lint(path: Path) -> tuple[bool, str]:
    emacs = shutil.which("emacs")
    if not emacs:
        return False, "Emacs is not installed or not on PATH"

    expression = (
        "(progn "
        "(require 'org) "
        "(org-mode) "
        "(let ((issues (org-lint))) "
        "(if issues (progn (prin1 issues) (kill-emacs 1)) "
        "(princ \"org-lint: clean\"))))"
    )
    result = subprocess.run(
        [emacs, "--batch", "-Q", str(path), "--eval", expression],
        check=False,
        capture_output=True,
        text=True,
    )
    output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    return result.returncode == 0, output


def main() -> int:
    parser = argparse.ArgumentParser(description="Check an Org execution plan.")
    parser.add_argument("plan", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat quality warnings as validation failures",
    )
    parser.add_argument(
        "--emacs-lint",
        action="store_true",
        help="also run Emacs org-lint; fail when Emacs is unavailable",
    )
    args = parser.parse_args()

    if not args.plan.is_file():
        print(f"ERROR: plan does not exist: {args.plan}", file=sys.stderr)
        return 2

    errors, warnings, metrics = validate(args.plan)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if args.emacs_lint:
        passed, output = run_emacs_lint(args.plan)
        if output:
            stream = sys.stdout if passed else sys.stderr
            print(output, file=stream)
        if not passed:
            errors.append("Emacs org-lint failed")

    print(
        "summary: "
        + ", ".join(f"{key}={value}" for key, value in metrics.items())
    )

    if errors or (args.strict and warnings):
        return 1
    print("validation: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
