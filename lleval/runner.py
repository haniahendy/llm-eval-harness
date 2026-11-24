"""Run JSONL cases through scorers and summarize pass rates."""
from __future__ import annotations

import json
from pathlib import Path

from .scorers import score_case


def run_cases(path: str | Path) -> list[dict]:
    results = []
    with Path(path).open() as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            case = json.loads(line)
            try:
                score = score_case(case)
                error = None
            except Exception as exc:  # keep one bad case from killing the run
                score, error = 0.0, f"{type(exc).__name__}: {exc}"
            results.append({"line": line_no, "name": case.get("name", f"line-{line_no}"),
                            "scorer": case.get("scorer"), "score": score, "error": error})
    return results


def summarize(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r["score"] == 1.0)
    errored = sum(1 for r in results if r["error"])
    by_scorer: dict[str, list[float]] = {}
    for r in results:
        by_scorer.setdefault(r["scorer"], []).append(r["score"])
    return {
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "errored": errored,
        "by_scorer": {k: round(sum(v) / len(v), 4) for k, v in sorted(by_scorer.items())},
    }
