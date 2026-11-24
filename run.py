"""CLI: score a JSONL file of cases and print a summary.

Usage:
    python run.py cases.jsonl [--show-failures]
"""
from __future__ import annotations

import argparse
import json

from lleval import run_cases, summarize


def main() -> None:
    parser = argparse.ArgumentParser(description="Score text outputs against expectations")
    parser.add_argument("cases_jsonl")
    parser.add_argument("--show-failures", action="store_true")
    args = parser.parse_args()

    results = run_cases(args.cases_jsonl)
    print(json.dumps(summarize(results), indent=2))
    if args.show_failures:
        for r in results:
            if r["score"] < 1.0:
                print(f"FAIL line {r['line']} [{r['scorer']}] {r['name']}" +
                      (f" ({r['error']})" if r["error"] else ""))


if __name__ == "__main__":
    main()
