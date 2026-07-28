#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "self-replanning-mode"
VALIDATOR = SKILL / "scripts" / "validate_org_plan.py"
CASES = Path(__file__).resolve().parent / "cases"


def validate(plan: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--strict", str(plan)],
        capture_output=True,
        text=True,
    )
    return result.stderr + result.stdout + f"exit: {result.returncode}\n"


def case_output(stdin_file: Path) -> str:
    with tempfile.TemporaryDirectory() as directory:
        plan = Path(directory) / "plan.org"
        plan.write_text(stdin_file.read_text(encoding="utf-8"), encoding="utf-8")
        return validate(plan)


def main() -> int:
    update = "--update" in sys.argv[1:]
    outputs = [
        (stdin_file.stem, case_output(stdin_file))
        for stdin_file in sorted(CASES.glob("*.stdin"))
    ]
    outputs.append(("template", validate(SKILL / "assets" / "execution-plan.org")))

    failures = 0
    for name, actual in outputs:
        stdout_file = CASES / f"{name}.stdout"
        if update:
            stdout_file.write_text(actual, encoding="utf-8")
            print(f"updated {name}")
            continue
        if not stdout_file.is_file():
            failures += 1
            print(f"FAIL {name}: missing {stdout_file.name}")
            continue
        expected = stdout_file.read_text(encoding="utf-8")
        if actual == expected:
            print(f"ok   {name}")
        else:
            failures += 1
            print(f"FAIL {name}")
            for line in expected.splitlines():
                print(f"  - {line}")
            for line in actual.splitlines():
                print(f"  + {line}")

    if update:
        return 0
    print(f"{len(outputs) - failures}/{len(outputs)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
