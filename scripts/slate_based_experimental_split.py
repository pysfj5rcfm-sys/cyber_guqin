#!/usr/bin/env python3
"""Deprecated legacy energy split entrypoint.

The RS_XWC_001_MVP_PILOT proved that this pure energy sequential alignment
approach is not reliable enough for guqin sample extraction. Keep this file as
a compatibility notice only; use the reusable slate-based framework helpers
instead.
"""

from __future__ import annotations

import argparse


REPLACEMENT_STEPS = [
    "scripts/slate_number_recognizer.py",
    "scripts/finalize_reviewed_unit_previews.py",
    "scripts/trim_clean_experimental_segments.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--explain", action="store_true", help="Print the replacement workflow and exit 0.")
    return parser.parse_args()


def replacement_message() -> str:
    return "\n".join(
        [
            "slate_based_experimental_split.py is deprecated.",
            "",
            "Reason:",
            "- pure energy sequential alignment was deprecated after the failed MVP pilot",
            "- old clean/candidate outputs must not be used as active inputs",
            "",
            "Use the explicit-input reusable framework helpers instead:",
            *[f"- {step}" for step in REPLACEMENT_STEPS],
            "",
            "All replacement helpers default to dry-run and label outputs as:",
            "- experimental_only=true",
            "- production_grade=false",
            "- not_standard_sample_library=true",
        ]
    )


def run(args: argparse.Namespace) -> int:
    print(replacement_message())
    return 0 if args.explain else 2


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
