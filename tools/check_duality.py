#!/usr/bin/env python3
"""Check DD Tech Lab companion script and notebook parity."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAIR_ROOTS = [
    ROOT / "stochastic_markov",
    ROOT / "medicaid_public_data_screening",
    ROOT / "forensic_numeric_techniques",
    ROOT / "medicare_outlier_screen",
    ROOT / "national_security_diligence" / "notebooks",
]


def stems(paths: list[Path]) -> set[str]:
    return {p.stem for p in paths if not p.name.startswith(".")}


def main() -> int:
    failures: list[str] = []
    for folder in PAIR_ROOTS:
        if not folder.exists():
            failures.append(f"missing folder: {folder.relative_to(ROOT)}")
            continue
        py_stems = stems(list(folder.glob("*.py")))
        nb_stems = stems(list(folder.glob("*.ipynb")))
        missing_notebooks = sorted(py_stems - nb_stems)
        missing_scripts = sorted(nb_stems - py_stems)
        for stem in missing_notebooks:
            failures.append(f"{folder.relative_to(ROOT)}/{stem}.py has no paired notebook")
        for stem in missing_scripts:
            failures.append(f"{folder.relative_to(ROOT)}/{stem}.ipynb has no paired script")

    if failures:
        print("DD Tech Lab duality check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("DD Tech Lab duality check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
